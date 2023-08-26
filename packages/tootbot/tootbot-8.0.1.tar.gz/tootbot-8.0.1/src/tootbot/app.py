"""Main logic for tootbot."""
import argparse
import asyncio
import logging
import math
import sys
import time

import aiohttp
import arrow
import asyncprawcore
from imgurpython.helpers.error import ImgurClientError
from minimal_activitypub.client_2_server import ActivityPubError
from minimal_activitypub.client_2_server import ApiError
from outdated import check_outdated
from tqdm import tqdm

from . import FATAL_TOOTBOT_ERROR
from . import PROGRESS_BAR_FORMAT
from . import VERSION_DEBUG
from . import __display_name__
from . import __package_name__
from . import __version__
from .collect import LinkedMediaHelper
from .collect import RedditHelper
from .collect import get_secrets
from .control import Configuration
from .control import PostRecorder
from .monitoring import HealthChecks
from .publish import MastodonPublisher

logger = logging.getLogger(__display_name__)
logger.setLevel(logging.DEBUG)


async def main() -> None:  # noqa: C901, PLR0915, PLR0912
    """Start tootbot.

    :param: None
    :return: None
    """
    # pylint: disable-msg=too-many-locals
    # pylint: disable-msg=too-many-statements
    parser = argparse.ArgumentParser(description="Post toots from reddit posts.")
    parser.add_argument(
        "-c",
        "--config-dir",
        action="store",
        default=".",
        dest="config_dir",
        help="Name of directory containing configuration files to use",
    )
    parser.add_argument(
        "-l",
        "--debug-log-file",
        action="store",
        dest="debug_log_file",
        help="Path of filename to save DEBUG log messages to",
    )
    args = parser.parse_args()
    config_dir = args.config_dir.rstrip("/")

    config: Configuration = await Configuration.load_config(
        config_dir=config_dir,
        debug_log=args.debug_log_file,
    )

    print(f"Welcome to {__display_name__} ({__version__})")
    logger.debug("Welcome to %s (%s)", __display_name__, VERSION_DEBUG)
    check_updates()

    if len(config.redditors) == 0 and len(config.subreddits) == 0:
        logger.error(
            "Nothing to do! Please configure at least one subreddit or redditor to follow."
        )
        await config.bot.post_recorder.close_db()
        sys.exit(1)

    try:
        secrets = await get_secrets(config_dir=config_dir)
    except ImgurClientError as imgur_error:
        logger.error("Error on creating ImgurClient: %s", imgur_error)
        logger.error(FATAL_TOOTBOT_ERROR)
        await config.bot.post_recorder.close_db()
        sys.exit(1)
    except asyncprawcore.AsyncPrawcoreException as reddit_exception:
        logger.error("Error while logging into Reddit: %s", reddit_exception)
        logger.error(FATAL_TOOTBOT_ERROR)
        await config.bot.post_recorder.close_db()
        sys.exit(1)

    try:
        secrets["mastodon"] = await MastodonPublisher.get_secrets(
            mastodon_domain=config.mastodon_config.domain,
            config_dir=config_dir,
        )
    except (ActivityPubError, ApiError) as error:
        logger.error("Error while logging into Mastodon: %s", error)
        logger.error("Tootbot cannot continue, now shutting down")
        await config.bot.post_recorder.close_db()
        sys.exit(1)

    session = aiohttp.ClientSession()

    try:
        mastodon_publisher = await MastodonPublisher.initialise(
            config=config,
            session=session,
            secrets=secrets["mastodon"],
        )
    except (ActivityPubError, ApiError) as error:
        logger.error("Error while logging into Mastodon: %s", error)
        logger.error("Tootbot cannot continue, now shutting down")
        await session.close()
        await config.bot.post_recorder.close_db()
        sys.exit(1)

    title = "Setting up shop "
    with tqdm(
        desc=f"{title:.<60}",
        total=1,
        unit="s",
        ncols=120,
        bar_format=PROGRESS_BAR_FORMAT,
    ) as progress_bar:
        healthcheck = HealthChecks(config=config)
        progress_bar.update(0.0002)

        reddit = RedditHelper(config=config, api_secret=secrets["reddit"])
        progress_bar.update(0.0008)

        try:
            media_helper = LinkedMediaHelper(
                imgur_secrets=secrets["imgur"],
            )
            progress_bar.update(0.999)
        except ImgurClientError as imgur_error:
            logger.error("Error on creating ImgurClient: %s", imgur_error)
            logger.error(FATAL_TOOTBOT_ERROR)
            await config.bot.post_recorder.close_db()
            sys.exit(1)

    now_timestamp = arrow.now().timestamp()
    last_post_ts = await config.bot.post_recorder.get_setting(PostRecorder.LAST_POST_TS)

    if now_timestamp - last_post_ts < config.bot.delay_between_posts:
        sleep_time = last_post_ts + config.bot.delay_between_posts - now_timestamp
        bar_title = "Sleeping until next toot"
        sleep_before_next_toot(bar_title, math.ceil(sleep_time))

    # Run the main script
    while True:
        if config.health.enabled:
            await healthcheck.check_start()

        await reddit.get_all_reddit_posts()
        await reddit.winnow_reddit_posts()
        reddit.remove_posts_by_ignored_users()
        await mastodon_publisher.make_post(reddit.posts, reddit, media_helper)

        if config.health.enabled:
            await healthcheck.check_ok()

        await config.bot.post_recorder.save_setting(
            PostRecorder.LAST_POST_TS,
            arrow.now().timestamp(),
        )

        if config.bot.run_once_only:
            logger.debug(
                "Exiting because RunOnceOnly is set to %s", config.bot.run_once_only
            )
            await config.bot.post_recorder.close_db()
            break

        sleep_time = config.bot.delay_between_posts

        # Determine how long to sleep before posting again
        if (
            config.mastodon_config.throttling_enabled
            and config.mastodon_config.number_of_errors
        ):
            sleep_time = (
                config.bot.delay_between_posts * config.mastodon_config.number_of_errors
            )
            if sleep_time > config.mastodon_config.throttling_max_delay:
                sleep_time = config.mastodon_config.throttling_max_delay

        logger.debug("Sleeping for %s seconds", sleep_time)
        print(" ")
        bar_title = "Sleeping before next toot"
        sleep_before_next_toot(bar_title, sleep_time)

        print(" ")
        logger.debug("Restarting main process...")

    await session.close()


def sleep_before_next_toot(bar_title: str, sleep_time: int) -> None:
    """Sleeps with progress bar for "sleep_time" seconds.

    :param bar_title: Message to show in progress bar.
    :type bar_title: str
    :param sleep_time: Number of seconds to sleep
    :type sleep_time: int
    """
    with tqdm(
        desc=f"{bar_title:.<60}",
        total=sleep_time,
        unit="s",
        ncols=120,
        bar_format=PROGRESS_BAR_FORMAT,
    ) as progress_bar:
        for _i in range(sleep_time):
            time.sleep(1)
            progress_bar.update()


def check_updates() -> None:
    """Check if there is a newer version of Tootbot available on PyPI."""
    is_outdated = False
    try:
        is_outdated, pypi_version = check_outdated(
            package=__package_name__,
            version=__version__,
        )
        if is_outdated:
            print(
                f"!!! New version of Tootbot ({pypi_version}) "
                f"is available on PyPI.org !!!\n"
            )
            logger.debug(
                "check_updates() ... New version of Tootbot (%s) is available on PyPI.org",
                pypi_version,
            )
    except ValueError:
        print("Notice - Your version is higher than last published version on PyPI")


def start_main() -> None:
    """Start actual main processing using async."""
    asyncio.run(main())


if __name__ == "__main__":
    start_main()

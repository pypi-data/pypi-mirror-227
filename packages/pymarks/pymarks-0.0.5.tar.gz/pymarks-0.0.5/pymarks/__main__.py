# main.py

from __future__ import annotations

import argparse
import functools
import logging
import sys

from pyselector import Menu
from pyselector import key_manager

from pymarks import constants
from pymarks import database
from pymarks import display
from pymarks import files
from pymarks import info
from pymarks import logger
from pymarks import utils
from pymarks.constants import ExitCode
from pymarks.constants import KeyCode
from pymarks.keys import Keybinds


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=constants.APP_HELP,
        add_help=False,
    )
    parser.add_argument(
        'search',
        nargs='*',
        help='Search terms',
    )
    parser.add_argument(
        '-m',
        '--menu',
        choices=constants.MENUS,
        default='rofi',
        help='Select menu',
    )
    parser.add_argument(
        '-V',
        '--version',
        action='store_true',
        help='Show version',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Verbose mode',
    )
    parser.add_argument(
        '-h',
        '--help',
        action='store_true',
        help='show this help message and exit',
    )
    parser.add_argument(
        '--json',
        action='store_true',
    )
    parser.add_argument(
        "--information",
        action='store_true',
    )
    parser.add_argument(
        '--test',
        action='store_true',
    )
    return parser


def setup_project() -> None:
    files.mkdir(constants.PYMARKS_HOME)
    files.mkdir(constants.DATABASES_DIR)
    files.mkdir(constants.PYMARKS_BACKUP_DIR)
    files.touch(constants.DB_DEFAULT_FILE)
    database.init_database(constants.DB_DEFAULT_FILE)


def parse_args_and_exit(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()

    if args.version:
        print(constants.APP_NAME, constants.APP_VERSION)
        sys.exit(0)

    if args.help:
        print(constants.APP_HELP)
        sys.exit(0)

    # if args.test:
    #     logger.verbose(True)
    #     log = logging.getLogger(__name__)
    #     log.info('Test mode')
    #     sys.exit(0)


def main() -> ExitCode:
    parser = setup_args()
    parse_args_and_exit(parser)
    args = parser.parse_args()

    setup_project()

    logger.verbose(args.verbose)
    log = logging.getLogger(__name__)
    log.debug('args: %s', vars(args))

    with database.open_database(constants.DB_DEFAULT_FILE) as cursor:
        if args.json:
            records = database.get_bookmarks_all(cursor)
            database.dump_to_json(records)
            return ExitCode(0)

        if constants.PYMARKS_BACKUP_MAX_AGE > 0:
            from pymarks import backup

            backup.check(
                database=constants.DB_DEFAULT_FILE,
                backup_path=constants.PYMARKS_BACKUP_DIR,
                max_age=constants.PYMARKS_BACKUP_MAX_AGE,
                max_amount=constants.PYMARKS_BACKUP_MAX_AMOUNT,
            )

        menu = Menu.get(args.menu)
        prompt = functools.partial(
            menu.prompt,
            lines=15,
            prompt=f'{constants.APP_NAME}> ',
            width='75%',
            height='50%',
            markup=False,
            mesg=f'Welcome to {constants.APP_NAME}',
        )

        # register keybinds
        for key in Keybinds:
            menu.keybind.add(*key)

        if args.information:
            info.get_app_information(cursor, prompt, menu=menu)
            sys.exit(0)

        records = (
            database.get_bookmarks_by_query(cursor, args.search)
            if args.search
            else database.get_bookmarks_all(cursor)
        )

        items = list(records)
        if len(items) == 0:
            database.insert_initial_record(cursor)
            items = list(database.get_bookmarks_all(cursor))

        bookmark_str, return_code = display.items(prompt=prompt, items=items)
        keycode = KeyCode(return_code)

        while True:
            if keycode == ExitCode(0):
                break

            try:
                keybind = menu.keybind.get_keybind_by_code(keycode)
                bookmark_str, keycode = keybind.callback(
                    cursor,
                    prompt,
                    bookmark=bookmark_str,
                    menu=menu,
                    keybind=keybind,
                )
            except key_manager.KeybindError as err:
                log.warning(err)
                return ExitCode(1)

        bookmark_id = utils.extract_record_id(bookmark_str)
        bookmark = database.get_bookmark_by_id(cursor, bookmark_id)
        utils.copy_to_clipboard(bookmark.url)
        return ExitCode(0)


if __name__ == '__main__':
    sys.exit(main())

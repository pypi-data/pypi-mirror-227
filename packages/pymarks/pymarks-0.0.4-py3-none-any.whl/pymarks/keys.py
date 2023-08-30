from __future__ import annotations

from typing import Any

from pymarks import actions
from pymarks import info
from pymarks.datatypes import Keybind

# FIX: Is this necessary?

Keybinds: list[Keybind] = []


def register(info: dict[str, Any]) -> None:
    Keybinds.append(Keybind(**info))


create_bookmark = {
    'key': 'Alt-a',
    'description': 'add bookmark',
    'callback': actions.create_bookmark,
    'hidden': False,
}
options_selector = {
    'key': 'Alt-e',
    'description': 'options',
    'callback': actions.options_selector,
    'hidden': False,
}
tag_selector = {
    'key': 'Alt-t',
    'description': 'filter by tag',
    'callback': actions.tag_selector,
    'hidden': False,
}
item_detail = {
    'key': 'Alt-d',
    'description': 'item detail',
    'callback': actions.item_detail,
    'hidden': False,
}
database_selector = {
    'key': 'Alt-c',
    'description': 'change db',
    'callback': actions.database_selector,
    'hidden': True,
}
app_information = {
    'key': 'Alt-i',
    'description': 'app information',
    'callback': info.get_app_information,
    'hidden': True,
}

register(create_bookmark)
register(options_selector)
register(tag_selector)
register(database_selector)
register(item_detail)
register(app_information)

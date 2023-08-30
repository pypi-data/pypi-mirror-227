# datatypes.py

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable
from typing import NamedTuple

PromptFn = Callable[..., tuple[str, int]]
RecordFromDB = tuple[int, str, str, str, str]


class Keybind(NamedTuple):
    key: str
    description: str
    callback: Callable
    hidden: bool


class SelectedBookmark(NamedTuple):
    bookmark: str
    keycode: int


@dataclass
class RecordForDB:
    url: str
    tags: str
    title: str | None
    desc: str | None


@dataclass
class Bookmark:
    id: int
    url: str
    title: str | None
    tags: str
    desc: str | None
    markup: bool = True

    def __str__(self) -> str:
        max_url_length = 80
        url = self.url[:max_url_length]
        tags = self.tags[:max_url_length]

        id_str = str(self.id).ljust(5)
        url_str = url.ljust(max_url_length)
        tags_str = tags.ljust(max_url_length)
        return f"{id_str} {url_str} {tags_str}"

    def to_json(self) -> str:
        return json.dumps(self.__dict__)


class BookmarkNotValidadError(Exception):
    pass

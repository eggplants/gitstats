from __future__ import annotations

import platform
from typing import Literal, TypedDict

ON_LINUX = platform.system() == "Linux"
ON_WIN = platform.system() == "Windows"

FIND_CMD = 'find /c /v ""' if ON_WIN else "wc -l"
GREP_CMD = "findstr" if ON_WIN else "grep"


class Configuration(TypedDict):
    max_domains: int
    max_ext_length: int
    style: str
    max_authors: int
    authors_top: int
    commit_begin: str
    commit_end: str
    linear_linestats: int
    project_name: str
    processes: int
    start_date: str


CONF: Configuration = {
    "max_domains": 10,
    "max_ext_length": 10,
    "style": "gitstats.css",
    "max_authors": 20,
    "authors_top": 5,
    "commit_begin": "",
    "commit_end": "HEAD",
    "linear_linestats": 1,
    "project_name": "",
    "processes": 8,
    "start_date": "",
}

ConfigurationKey = Literal[
    "max_domains",
    "max_ext_length",
    "style",
    "max_authors",
    "authors_top",
    "commit_begin",
    "commit_end",
    "linear_linestats",
    "project_name",
    "processes",
    "start_date",
]

WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

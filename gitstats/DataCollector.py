from __future__ import annotations

import datetime
import time
from abc import ABC, abstractmethod
from typing import Literal, TypedDict


class ExtensionInfo(TypedDict):
    files: int
    lines: int


class AuthorInfo(TypedDict, total=False):
    last_commit_stamp: int
    first_commit_stamp: int
    active_days: set[str]
    last_active_day: str
    lines_added: int
    lines_removed: int
    commits: int
    files: int
    lines: int
    # refine:
    place_by_commits: int
    commits_frac: float
    date_first: str
    date_last: str
    timedelta: datetime.timedelta


AuthorInfoKey = Literal[
    "last_commit_stamp",
    "first_commit_stamp",
    "active_days",
    "last_active_day",
    "lines_added",
    "lines_removed",
    "commits",
    "files",
    "lines",
    "place_by_commits",
    "commits_frac",
    "date_first",
    "date_last",
    "timedelta",
]


class TagInfo(TypedDict):
    stamp: int
    hash: str
    date: str
    commits: int
    authors: dict[str, int]


class Cache(TypedDict, total=False):
    files_in_tree: dict[str, int]
    lines_in_blob: dict[str, int]


ChangeInfo = TypedDict(
    "ChangeInfo",
    {
        "files": int,
        "ins": int,
        "del": int,
        "lines": int,
    },
)


class ChangeInfoByAuthor(TypedDict, total=False):
    lines_added: int
    commits: int


class DataCollector(ABC):
    """Manages data collection from a revision control repositor."""

    def __init__(self) -> None:
        self.stamp_created = time.time()
        self.cache: Cache = {}
        self.total_authors = 0
        self.activity_by_hour_of_day: dict[int, int] = {}  # hour -> commits
        self.activity_by_day_of_week: dict[int, int] = {}  # day -> commits
        self.activity_by_month_of_year: dict[int, int] = {}  # month [1-12] -> commits
        self.activity_by_hour_of_week: dict[
            int, dict[int, int]
        ] = {}  # weekday -> hour -> commits
        self.activity_by_hour_of_day_busiest = 0
        self.activity_by_hour_of_week_busiest = 0
        self.activity_by_year_week: dict[str, int] = {}  # yy_wNN -> commits
        self.activity_by_year_week_peak = 0

        self.authors: dict[
            str, AuthorInfo
        ] = {}  # name -> {commits, first_commit_stamp, last_commit_stamp,
        #          last_active_day, active_days, lines_added, lines_removed}

        self.total_commits = 0
        self.total_files = 0
        self.authors_by_commits: list[str] = []

        # domains
        self.domains: dict[str, dict[str, int]] = {}  # domain -> commits

        # author of the month
        self.author_of_month: dict[
            str, dict[str, int]
        ] = {}  # month -> author -> commits
        self.author_of_year: dict[int, dict[str, int]] = {}  # year -> author -> commits
        self.commits_by_month: dict[str, int] = {}  # month -> commits
        self.commits_by_year: dict[int, int] = {}  # year -> commits
        self.lines_added_by_month: dict[str, int] = {}  # month -> lines added
        self.lines_added_by_year: dict[int, int] = {}  # year -> lines added
        self.lines_removed_by_month: dict[str, int] = {}  # month -> lines removed
        self.lines_removed_by_year: dict[int, int] = {}  # year -> lines removed

        self.first_commit_stamp = 0
        self.last_commit_stamp = 0
        self.last_active_day: str | None = None
        self.active_days: set[str] = set()

        # lines
        self.total_lines = 0
        self.total_lines_added = 0
        self.total_lines_removed = 0

        # size
        self.total_size = 0

        # timezone
        self.commits_by_timezone: dict[str, int] = {}  # timezone -> commits

        # tags
        self.tags: dict[str, TagInfo] = {}

        self.files_by_stamp: dict[int, int] = {}  # stamp -> files

        # extensions
        self.extensions: dict[str, ExtensionInfo] = {}  # extension -> { files, lines }

        # line statistics
        self.changes_by_date: dict[
            int, ChangeInfo
        ] = {}  # stamp -> { files, ins, del, lines }

        # defined for stamp, author only if author commited at this timestamp.
        self.changes_by_date_by_author: dict[
            int, dict[str, ChangeInfoByAuthor]
        ] = {}  # stamp -> author -> lines_added

    @abstractmethod
    def collect(self, dir: str) -> None:
        """This should be the main function to extract data from the repository."""
        ...

    @abstractmethod
    def refine(self) -> None:
        """Produce any additional statistics from the extracted data."""
        ...

    @abstractmethod
    def getAuthorInfo(self, author: str) -> AuthorInfo | None:
        """Get a dictionary of author."""
        ...

    @abstractmethod
    def getActivityByDayOfWeek(self) -> dict[int, int]:
        ...

    @abstractmethod
    def getActivityByHourOfDay(self) -> dict[int, int]:
        ...

    @abstractmethod
    def getDomainInfo(self, domain: str) -> dict[str, int]:
        """Get a dictionary of domains."""
        ...

    @abstractmethod
    def getAuthors(self) -> list[str]:
        """Get a list of authors."""
        ...

    @abstractmethod
    def getFirstCommitDate(self) -> datetime.datetime:
        ...

    @abstractmethod
    def getLastCommitDate(self) -> datetime.datetime:
        ...

    # @abstractmethod
    # def getStampCreated(self) -> float:
    #     ...

    @abstractmethod
    def getTags(self) -> list[str]:
        ...

    @abstractmethod
    def getTotalAuthors(self) -> int:
        ...

    @abstractmethod
    def getTotalCommits(self) -> int:
        ...

    @abstractmethod
    def getTotalFiles(self) -> int:
        ...

    @abstractmethod
    def getTotalLOC(self) -> int:
        ...

    @abstractmethod
    def loadCache(self, cachefile: str) -> None:
        """Load cacheable data."""
        ...

    @abstractmethod
    def saveCache(self, cachefile: str) -> None:
        ...

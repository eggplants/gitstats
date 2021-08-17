import platform

ON_LINUX = platform.system() == "Linux"
ON_WIN = platform.system() == "Windows"

FIND_CMD = "find /c /v \"\"" if ON_WIN else "wc -l"
GREP_CMD = "findstr" if ON_WIN else "grep"

conf = {
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

WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

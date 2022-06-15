from __future__ import annotations

import os
import re
import subprocess
import sys
import time

from .constans import CONF, FIND_CMD, ON_LINUX
from .DataCollector import AuthorInfo, AuthorInfoKey


def getpipeoutput(cmds: list[str], quiet: bool = False) -> str:
    # global exectime_external
    start = time.time()
    if not quiet and ON_LINUX and os.isatty(1):
        print(">> " + " | ".join(cmds))
        sys.stdout.flush()
    p = subprocess.Popen(cmds[0], stdout=subprocess.PIPE, shell=True)
    processes = [p]
    for x in cmds[1:]:
        p = subprocess.Popen(x, stdin=p.stdout, stdout=subprocess.PIPE, shell=True)
        processes.append(p)
    output = p.communicate()[0]
    for p in processes:
        p.wait()
    end = time.time()
    if not quiet:
        if ON_LINUX and os.isatty(1):
            print("\r"),
        print(f"[{end - start:.5f}] >> {' | '.join(cmds)}")
    # exectime_external += end - start
    return bytes.decode(output).rstrip("\n")


def getlogrange(defaultrange: str = "HEAD", end_only: bool = True) -> str:
    commit_range = getcommitrange(defaultrange, end_only)
    if len(CONF["start_date"]) > 0:
        return f'--since="{CONF["start_date"]}" "{commit_range}"'
    return commit_range


def getcommitrange(defaultrange: str = "HEAD", end_only: bool = False) -> str:
    if len(CONF["commit_end"]) > 0:
        if end_only or len(CONF["commit_begin"]) == 0:
            return CONF["commit_end"]
        return f"{CONF['commit_begin']}..{CONF['commit_end']}"
    return defaultrange


# dict['author'] = { 'commits': 512 } - ...key(dict, 'commits')
def getkeyssortedbyvaluekey(d: dict[str, AuthorInfo], key: AuthorInfoKey) -> list[str]:
    sorted_keys = sorted(map(lambda el: (d[el][key], el), d.keys()))
    return list(map(lambda el: el[1], sorted_keys))


def getstatsummarycounts(line: str) -> list[int]:
    numbers = re.findall(r"\d+", line)
    if len(numbers) == 1:
        # neither insertions nor deletions:
        # may probably only happen for "0 files changed"
        numbers.append(0)
        numbers.append(0)
    elif len(numbers) == 2 and line.find("(+)") != -1:
        numbers.append(0)
        # only insertions were printed on line
    elif len(numbers) == 2 and line.find("(-)") != -1:
        numbers.insert(1, 0)
        # only deletions were printed on line
    return numbers


def getgitversion() -> str:
    return getpipeoutput(["git --version"]).split("\n")[0]


def getnumoffilesfromrev(time_rev: tuple[str, str]) -> tuple[int, str, int]:
    """Get number of files changed in commit."""
    time, rev = time_rev
    pipeout = getpipeoutput([f'git ls-tree -r --name-only "{rev}"', FIND_CMD])
    return (
        int(time),
        rev,
        int(pipeout.split("\n")[0]),
    )


def getnumoflinesinblob(ext_blob: tuple[str, str]) -> tuple[str, str, int]:
    """Get number of lines in blob."""
    ext, blob_id = ext_blob
    pipeout = getpipeoutput([f"git cat-file blob {blob_id}", FIND_CMD])
    return (
        ext,
        blob_id,
        int(pipeout.split()[0]),
    )


def html_linkify(text: str) -> str:
    return text.lower().replace(" ", "_")


def html_header(level: int, text: str) -> str:
    name = html_linkify(text)
    return f'\n<h{level} id="{name}"><a href="#{name}">{text}</a></h{level}>\n\n'

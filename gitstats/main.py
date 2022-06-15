from __future__ import annotations

# import time
import argparse
import os
import shutil
import sys
from typing import cast

from . import __version__
from .constans import CONF, ConfigurationKey
from .GitDataCollector import GitDataCollector

os.environ["LC_ALL"] = "C"


class CustomHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def check_config(v: str) -> None:
    key, value = v.split("=", 1)
    if key not in CONF:
        raise argparse.ArgumentTypeError(f"no such key {repr(key)} in config.")
    key = cast(ConfigurationKey, key)
    if isinstance(CONF[key], int):
        CONF[key] = int(value)
    else:
        CONF[key] = value


def check_gitpath(v: str) -> str:
    if os.path.isdir(os.path.join(v, ".git")):
        return v

    raise argparse.ArgumentTypeError(f"{repr(v)} is not a git root.")


def check_dir(v: str) -> str:
    if not os.path.exists(v):
        return v
    elif os.path.isdir(v):
        return v
    else:
        raise argparse.ArgumentTypeError(f"{repr(v)} is a file.")


def parse_args() -> argparse.Namespace:
    epilog = os.linesep.join(
        [
            "Default config values:",
            os.linesep.join([f"  - {k}={repr(v)}" for k, v in CONF.items()]),
            "",
            "Please see the manual page for more details.",
        ]
    )
    parser = argparse.ArgumentParser(
        prog="gitstats",
        formatter_class=(
            lambda prog: CustomHelpFormatter(
                prog,
                **{
                    "width": shutil.get_terminal_size(fallback=(120, 25)).columns,
                    "max_help_position": 25,
                },
            )
        ),
        description="Git history statistics generator",
        epilog=epilog,
    )

    parser.add_argument(
        "gitpath",
        type=check_gitpath,
        nargs="+",
        help="repo path to look up",
    )
    parser.add_argument(
        "outputpath",
        type=check_dir,
        help="dir path to output result",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=check_config,
        metavar="K=V",
        help="override configuration value",
    )
    parser.add_argument("-V", "--version", action="version", version=__version__)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    else:
        return parser.parse_args()


def main() -> None:
    args = parse_args()
    outputpath = args.outputpath
    os.makedirs(outputpath, exist_ok=True)

    print(f"Output path: {outputpath}")
    cachefile = os.path.join(outputpath, "gitstats.cache")

    data = GitDataCollector()
    data.loadCache(cachefile)

    for gitpath in args.gitpath:
        print(f"Git path: {gitpath}")

        prevdir = os.getcwd()
        os.chdir(gitpath)

        print("Collecting data...")
        data.collect(gitpath)

        os.chdir(prevdir)

    print("Refining data...")
    data.saveCache(cachefile)
    data.refine()
    savefile = os.path.join(outputpath, "report.json")
    print(data.dumpJson(), file=open(savefile, "w"))


if __name__ == "__main__":
    # time_start = time.time()
    main()
    # time_end = time.time()

import datetime
import getopt
import glob
import os
import pickle
import platform
import re
import shutil
import subprocess
import sys
import time
import zlib
import json
from .constans import conf

class DataCollector:
    """Manages data collection from a revision control repository."""
    def __init__(self):
        self.stamp_created = time.time()
        self.cache = {}
        self.total_authors = 0
        self.activity_by_hour_of_day = {}  # hour -> commits
        self.activity_by_day_of_week = {}  # day -> commits
        self.activity_by_month_of_year = {}  # month [1-12] -> commits
        self.activity_by_hour_of_week = {}  # weekday -> hour -> commits
        self.activity_by_hour_of_day_busiest = 0
        self.activity_by_hour_of_week_busiest = 0
        self.activity_by_year_week = {}  # yy_wNN -> commits
        self.activity_by_year_week_peak = 0

        self.authors = (
            {}
        )  # name -> {commits, first_commit_stamp, last_commit_stamp, last_active_day, active_days, lines_added, lines_removed}

        self.total_commits = 0
        self.total_files = 0
        self.authors_by_commits = 0

        # domains
        self.domains = {}  # domain -> commits

        # author of the month
        self.author_of_month = {}  # month -> author -> commits
        self.author_of_year = {}  # year -> author -> commits
        self.commits_by_month = {}  # month -> commits
        self.commits_by_year = {}  # year -> commits
        self.lines_added_by_month = {}  # month -> lines added
        self.lines_added_by_year = {}  # year -> lines added
        self.lines_removed_by_month = {}  # month -> lines removed
        self.lines_removed_by_year = {}  # year -> lines removed
        self.first_commit_stamp = 0
        self.last_commit_stamp = 0
        self.last_active_day = None
        self.active_days = set()

        # lines
        self.total_lines = 0
        self.total_lines_added = 0
        self.total_lines_removed = 0

        # size
        self.total_size = 0

        # timezone
        self.commits_by_timezone = {}  # timezone -> commits

        # tags
        self.tags = {}

        self.files_by_stamp = {}  # stamp -> files

        # extensions
        self.extensions = {}  # extension -> files, lines

        # line statistics
        self.changes_by_date = {}  # stamp -> { files, ins, del }

    ##
    # This should be the main function to extract data from the repository.
    def collect(self, dir):
        self.dir = dir
        if len(conf["project_name"]) == 0:
            self.projectname = os.path.basename(os.path.abspath(dir))
        else:
            self.projectname = conf["project_name"]

    ##
    # Load cacheable data
    def loadCache(self, cachefile):
        if not os.path.exists(cachefile):
            return
        print("Loading cache...")
        f = open(cachefile, "rb")
        try:
            self.cache = pickle.loads(zlib.decompress(f.read()))
        except:
            # temporary hack to upgrade non-compressed caches
            f.seek(0)
            self.cache = pickle.load(f)
        f.close()

    ##
    # Produce any additional statistics from the extracted data.
    def refine(self):
        pass

    ##
    # : get a dictionary of author
    def getAuthorInfo(self, author):
        return None

    def getActivityByDayOfWeek(self):
        return {}

    def getActivityByHourOfDay(self):
        return {}

    # : get a dictionary of domains
    def getDomainInfo(self, domain):
        return None

    ##
    # Get a list of authors
    def getAuthors(self):
        return []

    def getFirstCommitDate(self):
        return datetime.datetime.now()

    def getLastCommitDate(self):
        return datetime.datetime.now()

    def getStampCreated(self):
        return self.stamp_created

    def getTags(self):
        return []

    def getTotalAuthors(self):
        return -1

    def getTotalCommits(self):
        return -1

    def getTotalFiles(self):
        return -1

    def getTotalLOC(self):
        return -1

    ##
    # Save cacheable data
    def saveCache(self, cachefile):
        print("Saving cache...")
        tempfile = cachefile + ".tmp"
        f = open(tempfile, "wb")
        # pickle.dump(self.cache, f)
        data = zlib.compress(pickle.dumps(self.cache))
        f.write(data)
        f.close()
        try:
            os.remove(cachefile)
        except OSError:
            pass
        os.rename(tempfile, cachefile)

    def dumpJson(self):
        data = {
            'stamp_created': self.stamp_created,
            'total_authors': self.total_authors,
            'activity_by_hour_of_day': self.activity_by_hour_of_day,
            'activity_by_day_of_week': self.activity_by_day_of_week,
            'activity_by_month_of_year': self.activity_by_month_of_year,
            'activity_by_hour_of_week': self.activity_by_hour_of_week,
            'activity_by_hour_of_day_busiest':
            self.activity_by_hour_of_day_busiest,
            'activity_by_hour_of_week_busiest':
            self.activity_by_hour_of_week_busiest,
            'activity_by_year_week': self.activity_by_year_week,
            # 'authors': self.authors,
            'total_commits': self.total_commits,
            'total_files': self.total_files,
            'authors_by_commits': self.authors_by_commits,
            'domains': self.domains,
            'author_of_month': self.author_of_month,
            'author_of_year': self.author_of_year,
            'commits_by_month': self.commits_by_month,
            'commits_by_year': self.commits_by_year,
            'lines_added_by_month': self.lines_added_by_month,
            'lines_added_by_year': self.lines_added_by_year,
            'lines_removed_by_month': self.lines_removed_by_month,
            'lines_removed_by_year': self.lines_removed_by_year,
            'first_commit_stamp': self.first_commit_stamp,
            'last_commit_stamp': self.last_commit_stamp,
            'last_active_day': self.last_active_day,
            # 'active_days': self.active_days,
            'total_lines': self.total_lines,
            'total_lines_added': self.total_lines_added,
            'total_lines_removed': self.total_lines_removed,
            'total_size': self.total_size,
            'commits_by_timezone': self.commits_by_timezone,
            'tags': self.tags,
            'files_by_stamp': self.files_by_stamp,
            'extensions': self.extensions,
            'changes_by_date': self.changes_by_date,
        }
        
        print(self.authors)

        return json.dumps(data, indent=4)

import sys
import os
import time
import getopt

from common.GitDataCollector import GitDataCollector
from common.utils import usage
from common.constans import conf

if sys.version_info < (3, 8):
    sys.exit(1)

from multiprocessing import Pool

os.environ["LC_ALL"] = "C"

exectime_internal = 0.0
exectime_external = 0.0
time_start = time.time()

if __name__ == "__main__":
    args_orig = sys.argv[1:]

    optlist, args = getopt.getopt(args_orig, "hc:", ["help"])
    for o, v in optlist:
        if o == "-c":
            key, value = v.split("=", 1)
            if key not in conf:
                raise KeyError('no such key "%s" in config' % key)
            if isinstance(conf[key], int):
                conf[key] = int(value)
            else:
                conf[key] = value
        elif o in ("-h", "--help"):
            usage()
            sys.exit()

    if len(args) < 2:
        usage()
        sys.exit(0)

    outputpath = os.path.abspath(args[-1])
    rundir = os.getcwd()

    try:
        os.makedirs(outputpath)
    except OSError:
        pass
    if not os.path.isdir(outputpath):
        print("FATAL: Output path is not a directory or does not exist")
        sys.exit(1)

    print("Output path: %s" % outputpath)
    cachefile = os.path.join(outputpath, "gitstats.cache")

    data = GitDataCollector()
    data.loadCache(cachefile)

    for gitpath in args[0:-1]:
        print("Git path: %s" % gitpath)

        prevdir = os.getcwd()
        os.chdir(gitpath)

        print("Collecting data...")
        data.collect(gitpath)

        os.chdir(prevdir)

    print("Refining data...")
    data.saveCache(cachefile)
    data.refine()
    
    with open(os.path.join(outputpath, 'report.json'), 'w') as f:
        f.write(data.dumpJson())
    
    time_end = time.time()


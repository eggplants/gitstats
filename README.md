# gitstats for python 3

- Git history statistics generator
- Forked from [KaivnD/gitstats](https://github.com/KaivnD/gitstats) for support python3

## Install

```bash
pip install git+https://github.com/eggplants/gitstats
# OR
pip install gitstats-forked
```

## Usage

```shellsession
$ gitstats -h
usage: gitstats [-h] [-c K=V] [-V] gitpath [gitpath ...] outputpath

Git history statistics generator

positional arguments:
  gitpath               repo path to look up
  outputpath            dir path to output result

options:
  -h, --help            show this help message and exit
  -c K=V, --config K=V  override configuration value (default: None)
  -V, --version         show program's version number and exit

Default config values:
  - max_domains=10
  - max_ext_length=10
  - style='gitstats.css'
  - max_authors=20
  - authors_top=5
  - commit_begin=''
  - commit_end='HEAD'
  - linear_linestats=1
  - project_name=''
  - processes=8
  - start_date=''

Please see the manual page for more details.
```

## For Example

``` bash
gitstats -c start_date=2021-07-14 <gitdir> <outputdir>
```

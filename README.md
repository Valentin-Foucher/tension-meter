# Tension Meter 

## Description

This project is designed to load test websites. 

There are 3 different request mode:
- iterative (it can either be infinite or bound by a duration or a count)
- concurrent (using CPU, it is bound by a count)
- asynchronous (using coroutines, it is bound by a count)

## Installation

Just run:
```bash
$ pipenv install
Courtesy Notice: Pipenv found itself running within a virtual environment, so it will automatically use that environment, instead of creating its own for any project. You can set PIPENV_IGNORE_VIRTUALENVS=1 to force pipenv to ignore that environment and create its own instead. You can set PIPENV_VERBOSITY=-1 to suppress this warning.
Installing dependencies from Pipfile.lock (fa3efc)...
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 11/11 — 00:00:02
```

You are good to go  
😄

## Help

```bash
$ python run.py -h
usage: run.py [-h] [-P] [-G] [-Q] [-D] [-I] [-R] [-O] [-d DATA] [-p PARAMS] [-H [HEADERS [HEADERS ...]]] [-n COUNT] [-t TIME] [-b TEMPLATE] [-a] [-c] [-v] url

positional arguments:
  url                   Target url

optional arguments:
  -h, --help            show this help message and exit
  -P, --POST, --post
  -G, --GET, --get
  -Q, --PUT, --put
  -D, --DELETE, --delete
  -I, --HEAD, --head
  -R, --PATCH, --patch
  -O, --OPTIONS, --options
  -d DATA, --data DATA  Payload in JSON format
  -p PARAMS, --params PARAMS
                        Query parameters in JSON format
  -H [HEADERS [HEADERS ...]], --headers [HEADERS [HEADERS ...]]
                        Headers in JSON format
  -n COUNT, --count COUNT
                        The maximum amount of requests you want to perform (by default, infinity in sync mode, 1000 in async mode)
  -t TIME, --time TIME  The maximum time in seconds you want to be requesting (only in sync mode if no count was specified)
  -b TEMPLATE, --template TEMPLATE
                        TODO
  -a, --async           Shall the requests be performed asynchronously
  -c, --concurrent      Shall the requests be performed concurrently
  -v, --verbose         Shall you see the responses content
```

## Docker image

From the repository root, run:
```bash
docker build .
```

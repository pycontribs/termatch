#!/usr/bin/env python
import glob
import re
import os
import inspect
import logging

try:
    import coloredlogs
    coloredlogs.install(fmt="%(levelname)s\t%(message)s", level=logging.DEBUG)
except Exception as e:
    print(e)
    pass

logging.basicConfig(level=logging.DEBUG)
patterns = []
pattern_counter = 0
matches_count = 0
lines_count = 0

mydir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
os.chdir(mydir)

for f in glob.glob('patterns/*.txt'):
    with open(f) as infile:
        logging.info(f)
        b = os.path.basename(f)
        for line in infile:
            try:
                patterns.append({
                  'name': b,
                  're': re.compile(line.rstrip()),
                  'positive': 0,
                  'negative': 0
                })
                pattern_counter += 1
            except Exception as e:
                logging.error("ERROR: %s on line [%s]", e, line)

logging.info("Loading samples...")
for f in glob.glob('samples/*.txt'):
    with open(f) as infile:
        logging.debug(f)
        for line in infile:
            lines_count += 1
            for p in patterns:
                result = p['re'].match(line)
                if result:
                    p['positive'] += 1
                    matches_count += 1
                # print(result)

logging.info("Total patterns: %s", pattern_counter)
logging.info("Total matches: %s / %s", matches_count, lines_count)

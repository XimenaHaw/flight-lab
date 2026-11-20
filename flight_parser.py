"""Flight Schedule Parser and Query Tool - command-line entry point.

Run from the project folder, for example:
    python flight_parser.py -i data/db.csv -a data/airports.txt
"""
import argparse
import sys
import logging
import json
import glob
from validator import *
from csv_loader import *
from query import *

# TODO: fill in your details: plain ASCII, no spaces or underscores.
STUDENT_ID = "251ADB044"
FIRST_NAME = "XimenaMaria"
LAST_NAME = "HawithGarcia"


def main(argv: list[str] | None = None) -> int:
    """Run the whole program and return the exit code (0, 1 or 2).

    argv is the argument list without the program name.
    None means use sys.argv[1:] (argparse does this for you).
    Do not call sys.exit() inside main(); return the code instead.
    """
    # parse arguments with argparse (-i, -d, -j, -a, -o, -q, -r).
    parser = argparse.ArgumentParser(description= 'Program') 

    exclusive_group = parser.add_mutually_exclusive_group()

    exclusive_group.add_argument('-i', type=str, nargs=1, help='Parse a single CSV file.')
    exclusive_group.add_argument('-d', type=str, nargs=1, help='Parse every file in the folder whose name ends in .csv (not subfolders), in sorted filename order')
    exclusive_group.add_argument('-j', type=str, nargs=1, help='Load an existing JSON database instead of parsing CSVs.')
    parser.add_argument('-a', type=str, nargs=1, help='Airport list file. Required with -i and -d ; ignored with -j.')
    parser.add_argument('-o', type=str, nargs=1, default = "['db.json']", help='Output path for the JSON database. Default: db.json in the current directory. Only allowed with -i or -d .')
    parser.add_argument('-q', type=str, nargs=1, help='Run the queries in this JSON file against the database (parsed or loaded).')
    parser.add_argument('-r', type=str, nargs=1, help='Folder for the query response file. Default: the current directory.')

    args = parser.parse_args()

    # handling needed file error
    if not (args.i or args.d or args.j):
        parser.error('No data source added. One of -i/-d/-j required.')

    # load or parse the data, write the database and errors.log.

    if args.i is not None:
        records, errors = parse_files(str(args.i[0]), load_airports(str(args.a[0])))
    elif args.d is not None:
        records, errors = parse_files((glob.glob(args.d[0] + "*.csv").sort), load_airports(str(args.a[0])))
    else:
        with open(str(args.j[0]), "r") as file:
            records = json.load(file)

    logger = logging.getLogger("flight_parser")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(records, mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    try:
        logger.addHandler(handler)
        for error in errors:
            logger.warning(error)
    finally:
        logger.removeHandler(handler)
        handler.close()

    # load queries 
    if args.q is not None:
        with open(str(args.q[0]), "r") as file:
            data = json.load(file)

    # run the queries and write the response file.
        query_results = run_queries(records, data)

    # Remember: remove and close the logging handler before returning,
    # also when returning early because of an error (use try/finally).

    return 0

if __name__ == "__main__":
    sys.exit(main())

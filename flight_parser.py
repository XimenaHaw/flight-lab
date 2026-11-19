"""Flight Schedule Parser and Query Tool - command-line entry point.

Run from the project folder, for example:
    python flight_parser.py -i data/db.csv -a data/airports.txt
"""
import sys
import argparse
from validator import *
from csv_loader import *

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
    # TODO: parse arguments with argparse (-i, -d, -j, -a, -o, -q, -r).
    parser = argparse.ArgumentParser(description= 'Program') 

    parser.add_argument('-i', type=str, nargs=1, help='Parse a single CSV file.')
    parser.add_argument('-d', type=str, nargs=1, help='Parse every file in the folder whose name ends in .csv (not subfolders), in sorted filename order')
    parser.add_argument('-j', type=str, nargs=1, help='Load an existing JSON database instead of parsing CSVs.')
    parser.add_argument('-a', type=str, nargs=1, help='Airport list file. Required with -i and -d ; ignored with -j.')
    parser.add_argument('-o', type=str, nargs=1, help='Output path for the JSON database. Default: db.json in the current directory. Only allowed with -i or -d .')
    parser.add_argument('-q', type=str, nargs=1, help='Run the queries in this JSON file against the database (parsed or loaded).')
    parser.add_argument('-r', type=str, nargs=1, help='Folder for the query response file. Default: the current directory.')

    args = parser.parse_args()

    # TODO: load or parse the data, write the database and errors.log.
    parse_files(str(args.i[0]), load_airports(str(args.a[0])))
    # TODO: run the queries and write the response file.
    # Remember: remove and close the logging handler before returning,
    # also when returning early because of an error (use try/finally).

    # return 0 if everything sucesfull 
    return 0


if __name__ == "__main__":
    sys.exit(main())

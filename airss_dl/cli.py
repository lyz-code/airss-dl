"""
Module to store the command line and logger functions.

Functions:
    load_logger: Function to define the program logging object.
    load_parser: Function to define the command line arguments.
"""

import logging
import argparse
# import argcomplete


def load_parser():
    '''
    Function to define the command line arguments.
    '''

    # Argparse
    parser = argparse.ArgumentParser(
        description='Airss content downloader',
    )

    subparser = parser.add_subparsers(dest='subcommand', help='subcommands')
    extract_parser = subparser.add_parser('extract')

    extract_parser.add_argument(
        "url",
        type=str,
        help='URL to extract',
    )

    subparser.add_parser('install')

    # argcomplete.autocomplete(parser)
    return parser


def load_logger():
    '''
    Function to define the program logging object.
    '''

    logging.addLevelName(logging.INFO, "[\033[36mINFO\033[0m]")
    logging.addLevelName(logging.ERROR, "[\033[31mERROR\033[0m]")
    logging.addLevelName(logging.DEBUG, "[\033[32mDEBUG\033[0m]")
    logging.addLevelName(logging.WARNING, "[\033[33mWARNING\033[0m]")
    logging.basicConfig(
        level=logging.INFO,
        format="  %(levelname)s %(message)s"
    )
    return logging.getLogger('main')

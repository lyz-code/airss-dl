#!/usr/bin/python3

# Copyright (C) 2019 lyz <lyz@riseup.net>
# This file is part of airss.
#
# airss is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# airss is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with airss.  If not, see <http://www.gnu.org/licenses/>.

from airss_dl.cli import load_logger, load_parser
from airss_dl.extractor import rss
from airss_dl.models import engine
from airss_dl.ops import install
from sqlalchemy.orm import sessionmaker

import logging
import sys


def main(argv=sys.argv[1:]):
    args = load_parser().parse_args(argv)
    load_logger()
    log = logging.getLogger('main')
    connection = engine.connect()
    session = sessionmaker()(bind=connection)

    if args.subcommand == 'install':
        install(session, log)
    elif args.subcommand == 'extract':
        extractor = rss.RssExtractor(session)
        extractor.create_source(args.url)
        extractor.extract(args.url)

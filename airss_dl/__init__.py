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

from airss_dl.cli import load_logger
from airss_dl.models import engine
from airss_dl.extractor import rss
from sqlalchemy.orm import sessionmaker


def main():

    load_logger()
    connection = engine.connect()
    session = sessionmaker()(bind=connection)

    extractor = rss.RssExtractor(session)
    # extractor.create_source('https://www.gamingonlinux.com/article_rss.php')
    # extractor.extract('https://www.gamingonlinux.com/article_rss.php')
    extractor.create_source('https://xkcd.com/rss.xml')
    extractor.extract('https://xkcd.com/rss.xml')

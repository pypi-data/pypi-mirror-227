#!/usr/bin/env python3

import os
import re
from pathlib import Path

# import requests_cache
from zoneinfo import ZoneInfo

import requests

session = requests.Session()
# session = requests_cache.CachedSession("cache")

import argparse
import time
from datetime import datetime

import rich
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import track
from rich.table import Table
from tinydb import Query, TinyDB
from tinydb.table import Table


def parse_date(date_string, datetime_date):
    try:
        current_time = datetime.strptime(date_string, "%H:%M:%S")
    except ValueError as e:
        # print(date_string)
        raise e
    result = datetime_date.replace(
        hour=current_time.hour,
        minute=current_time.minute,
        second=current_time.second,
        microsecond=current_time.microsecond,
    )
    return result


def get_datetime():
    # The IANA time zone identifier for San Francisco is America/Los_Angeles.
    # tzinfo=ZoneInfo("America/Los_Angeles")
    # Time in San Francisco: 12:27, 24.08.2023 PDT (UTC-7)
    # PST - Pacific Standard Time
    # PDT - Pacific Daylight Time
    # curl "http://worldtimeapi.org/api/timezone/America/Los_Angeles.txt"
    # "datetime" 2023-08-24T14:00:52.278750-07:00
    # response = requests.get("http://worldtimeapi.org/api/timezone/America/Los_Angeles.txt")
    # print(response.text.splitlines())
    # datetime_date = [line for line in response.text.splitlines() if "datetime" in line][0]
    # datetime_date = datetime.fromisoformat(datetime_date.split()[1].strip())
    from zoneinfo import ZoneInfo

    datetime_date = datetime.now(tz=ZoneInfo("America/Los_Angeles"))
    return datetime_date


def prepend_host(link, host="https://somafm.com"):
    if link.startswith("/buy/multibuy.cgi?"):
        return f"{host}{link}"
    else:
        return link


def get_channels(
    channels_url="https://somafm.com/channels.json",
    excluded_channels=["sfinsf", "scanner"],
    keys=["title", "description"],
):
    result = session.get(channels_url).json()
    # channels = {c["id"] : {key:c[key] for key in keys} for c in result["channels"]}
    channels = {c["id"]: {"meta": c} for c in result["channels"]}
    channels = {k: v for k, v in channels.items() if k not in excluded_channels}
    return channels


def get_data(channel):
    url = f"https://somafm.com/{channel}/songhistory.html"
    songs_result = session.get(url)
    # print(songs_result.text)
    soup = BeautifulSoup(songs_result.text, "html.parser")
    # with open(f"./html/{channel}.html", "w") as fh:
    #    fh.write(soup.prettify())
    # print(soup.title.text.strip())
    songs_div = soup.find("div", id="playinc")
    if songs_div:
        songs_html = songs_div.find("table")
        if not songs_html:
            print(f"No table found for {channel}")
    else:
        print(f"Parsing error for {channel}, can't find songs div")
    return songs_html


def extract_data(songs_html):
    table_rows = songs_html.find_all("tr")
    channel_data = []
    for row in table_rows:
        row_td = row.find_all("td")
        r = []
        for td in row_td:
            td_a = td.find("a")
            r.append(td.text)
            if td_a:
                # only append unique links? (no, append all, exclude later)
                # if td_a["href"] not in r and not td_a["href"].startswith("/buy/multibuy.cgi"):
                r[-1] = (r[-1], td_a["href"])
        channel_data.append(r)
    return channel_data


def extract_date(channel_data, datetime_date):
    # you have to look at the tendency of multiple times if they tend to get smaller, if they are getting bigger, catch the wrap-around, f.e. from 00:00:00 to 23:59:59
    previous_date = None
    substract_day = False
    # test if reversion works
    # channel_data[-1][0] = "23:59:00"
    # channel_data[-2][0] = "23:53:00"
    for entry in channel_data:
        # print(entry)
        clean_date = re.sub("[\s]*\(Now\)[\s]*", "", entry[0])
        entry[0] = parse_date(clean_date, datetime_date)
        if previous_date is None:
            previous_date = entry[0]
        else:
            if entry[0] > previous_date:
                substract_day = True
        previous_date = entry[0]
        # print(f"substract_day: {substract_day}")
        if substract_day:
            entry[0] = entry[0].replace(day=entry[0].day - 1)
    return channel_data


def annotate_result(channel_data):
    annotated_data = []
    for result in channel_data:
        ar = {}
        ar["played_at"] = result[0]
        if isinstance(result[1], tuple):
            ar["artist_name"] = result[1][0].strip()
            ar["artist_link"] = prepend_host(result[1][1])
        else:
            ar["artist_name"] = result[1]
        try:
            ar["song_name"] = result[2].strip()
        except AttributeError as e:
            console.print(channel)
            console.print(result)
            raise e
        if isinstance(result[3], tuple):
            ar["album_name"] = result[3][0].strip()
            ar["album_link"] = prepend_host(result[3][1])
        else:
            ar["album_name"] = result[3].strip()
        # ar = {k:v for k,v in ar.items() if v}
        annotated_data.append(ar)
    return annotated_data


def print_channel(channel, channel_key):
    table = Table(title=f"{channel_key}")

    table.add_column("Played")
    table.add_column("Song")
    table.add_column("Artist")
    table.add_column("Album")

    for r in channel["annotated_data"]:
        table.add_row(
            rich.markup.escape(r["played_at"].strftime("%H:%M:%S")),
            rich.markup.escape(r["song_name"]),
            rich.markup.escape(r["artist_name"]),
            rich.markup.escape(r["album_name"]),
        )

    console.print(table)


def filter_data(channel_data):
    exclude_data = {}
    exclude_data[0] = ["Played At"]
    exclude_data[1] = ["Break / Station ID", "(sound bite)"]
    channel_data = [result for result in channel_data if len(result) > 1]
    header = channel_data[0]
    for key, value in exclude_data.items():
        channel_data = [result for result in channel_data if result[key] not in value]
    return header, channel_data


# this should run like every 30 minutes?
# you could take the span of the last tracklist an divide by … 2?
# but then i would need scheduling from inside python (and i would have to run it for each station)
def main():
    parser = argparse.ArgumentParser(
        prog="soma-songs", description="Save song data from somafm.com as JSON"
    )
    parser.add_argument(
        "-o",
        "--output-directory",
        dest="outdir",
        default=os.path.expanduser("~/somafm-json"),
        help="Where to store the output",
    )
    parser.add_argument(
        "-w",
        "--wait",
        dest="wait",
        default=0,
        help="Wait N seconds between channels",
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Print results as rich tables",
    )
    output_group.add_argument(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        default=False,
        help="Don't print output",
    )
    # too verbose + quiet are exclusive
    args = parser.parse_args()
    console = Console(quiet=args.quiet)

    outdir = Path(args.outdir)
    if not outdir.is_dir():
        outdir.mkdir()
    db = TinyDB(outdir.joinpath("music.json"))

    channels = get_channels()
    console.print("Updating song info of {} channels".format(len(channels.keys())))

    datetime_date = get_datetime()

    for i in track(
        range(0, len(channels.keys())), description="Fetching HTML", console=console
    ):
        # for i, channel in enumerate(channels.keys()):
        channel = list(channels.keys())[i]
        songs_html = get_data(channel)
        channels[channel]["raw_data"] = extract_data(songs_html)
        if args.wait > 0:
            # console.print(f"Waiting {args.wait}s")
            time.sleep(args.wait)

    for i in track(
        range(0, len(channels.keys())), description="Annotating data", console=console
    ):
        # for channel in channels.keys():
        channel = list(channels.keys())[i]
        channel_data = channels[channel]["raw_data"]
        header, channel_data = filter_data(channel_data)
        channel_data = extract_date(channel_data, datetime_date)
        channels[channel]["annotated_data"] = annotate_result(channel_data)

    total_previous = 0
    total_current = 0
    for i in track(
        range(0, len(channels.keys())),
        description="Inserting song data",
        console=console,
    ):
        # for channel in channels.keys():
        channel = list(channels.keys())[i]
        if args.verbose:
            print_channel(channels[channel], channel)
        # db.upsert({'name': 'John', 'logged-in': True}, User.name == 'John')
        table = db.table(channel)
        total_previous += len(table)
        for entry in channels[channel]["annotated_data"]:
            entry["played_at"] = datetime.isoformat(entry["played_at"])
            table.upsert(
                entry,
                Query().song_name == entry["song_name"]
                and Query().played_at == entry["played_at"],
            )
        total_current += len(table)
        # table.close()

    db = TinyDB(outdir.joinpath("meta.json"))
    for i in track(
        range(0, len(channels.keys())),
        description="Inserting metadata",
        console=console,
    ):
        # for channel in channels.keys():
        channel = list(channels.keys())[i]
        db.upsert(channels[channel]["meta"], Query().id == channel)

    console.print(
        "✨ 🎶 ✨ [bold]All done![/] Added {} entries, see files in {}".format(
            total_current - total_previous, args.outdir
        )
    )


if __name__ == "__main__":
    main()

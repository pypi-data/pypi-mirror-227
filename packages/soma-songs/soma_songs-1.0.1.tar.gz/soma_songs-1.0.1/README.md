# Soma Songs

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![PyPI: Python Version](https://img.shields.io/pypi/pyversions/soma-songs)

Save songs from <https://somafm.com> as JSON.


## How does it work?

Most somafm radiostations publish their tracklist. F.e. the police `scanner`-channel doesn't, while [def con radio](https://somafm.com/defcon/songhistory.html)) does. But this overview only includes the last hour(s) and is not easily machine-readable.

So why not archive this for all the channels, all the time, clean up the data a little bit and make it more useable?

- results are stored in a `tinydb`, well, two, actually, these are just JSON files
- the timestamp also includes a date and has a timezone annotation. Btw., if you want to get into the details: <https://somafm.com> is based in San Francisco, the IANA time zone identifier is America/Los_Angeles. Currently they use PDT (Pacific Daylight Time), which is UTC-7. PST (Pacific Standard Time) would be UTC-8.
- the somafm amazon links are not relative anymore and are also included to support <https://somafm.com>


# How do you use/run this?

Well, you don't have to :) because I already created inktrap/somafm-json which contains the output.

But you can, by:

```
pipx install somafm-songs
```

If you call `somafm-songs` you'll see that `~/somafm-json/meta.json` contains the channel meta data and `~/somafm-json/music.json` contains tracks/songs.

If you want to keep your results in git and push them to a remote you have to turn that directory into a git repository with a remote and create a cron-job which does (and is allowed to do) the git commit/push spiel.

```
* 30 * * * ~/path/to/somafm-songs && cd ~/somafm-songs && git commit -am $(date) && git push
```

Thanks to somafm and to all these amazing DJ(ane)s :)


# What can you do with this?

You get a nice archive of great radio channels, what else do you want? Well, you could:

- look for overlap/similarity of channels
- create your own rankings (per channel/artist/genre/year/…)
- match albums/artists with musicbrainz-identifiers to find more info
- train your own music recommendation tool for each channel, just for fun <https://github.com/mattmurray/music_recommender>
- you could check for each channel how many artists/albums/songs are in your `beets` library (maybe adjust for popularity?!)

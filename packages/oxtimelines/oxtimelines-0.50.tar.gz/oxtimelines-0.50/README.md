# oxtimelines - create timeline from video

This program takes one or more video files as input and outputs timeline images.
If a cuts path is given, it also outputs a json file containing cuts. If in and
out points are given, only that part of the video(s) will be rendered.

The timeline modes can be any combination of 'antialias' (average color),
'slitscan' (center pixel), 'keyframes' (one or more frames per cut), 'audio'
(waveform), 'cuts' (antialias with cut detection overlay, for debugging) and
'data' (each frame resized to 8x8 px).

One or two timeline heights can be specified, larger height first. The timeline
widths will be 1 px per frame for the first one, and 1 px per second for the
second (smaller) one. If the wide option is set, large 'keyframeswide' tiles
will be rendered. They can be used at a later point to render small 'keyframes'
tiles without having to decode the video again.


## Usage

    usage: oxtimelines [options] video1 [video2]

    Options:
      -h, --help            show this help message and exit
      -o TILES, --output=TILES
                            path for combined timeline tiles
      -c CUTS, --cuts=CUTS  path for combined cuts json file
      -p POINTS, --points=POINTS
                            inpoint,outpoint (optional)
      -m MODES, --modes=MODES
                            timeline mode(s) (antialias, slitscan, keyframes,
                            audio, cuts, data)
      -s SIZES, --sizes=SIZES
                            timeline size(s) (64 or 64,16)
      -w, --wide            keep wide frames tiles
      -l, --log             log performance

## Install

    pip3 install oxtimelines

## Python API

    import oxtimelines

    timeline = oxtimelines.Timelines(videos, output, cuts_json, in_out, modes, sizes, wide, log)
    timeline.render()

## Latest Code

    git clone https://code.0x2620.org/0x2620/oxtimelines

## Dependencies

 - python-imaging
 - python-ox
 - ffmpeg



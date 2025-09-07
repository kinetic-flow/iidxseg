# iidxseg

![screenshot](https://raw.githubusercontent.com/kinetic-flow/iidxseg/refs/heads/master/res/readme/2019-09-15.gif)

IIDX segment display software emulator

## Downloads
Check the [releases page](https://github.com/minsang-github/iidxseg/releases).

## Build Dependencies
Tested on Python 3.7.3. Requires [DSEG14Classic-Italic font](https://github.com/keshikan/DSEG), pygame, and SpiceAPI.

## Instructions

First of all, ensure SpiceAPI server is running. Then, launch with:

    iidxseg.exe server_ip port password

e.g., for running locally -

    iidxseg.exe localhost 50000 "MyPass123"

or, over the network by IP -

    iidxseg.exe "192.168.1.200" 50000 "MyPass123"
    
Display a timer (only ticks up) and the current time:

    iidxseg.exe "192.168.1.200" 50000 "MyPass123" --timer --clock

Use a different color! Or cycle through RGB like a true gamer!

    iidxseg.exe "192.168.1.200" 50000 "MyPass123" --color 0xff12ee
    iidxseg.exe "192.168.1.200" 50000 "MyPass123" --color rgb

Launch it borderless, exactly where you want it:

    iidxseg.exe "192.168.1.200" 50000 "MyPass123" --width 1280 --height 720 --x 200 --y 100

## Updates

### 2020-03-01

* Made the window resizable. Borderless option added. A bunch of command line options added for adjusting the window size at launch.

### 2020-03-06

* Standalone binary release for Windows.

* Add timer and wall clock. Spawn a separate process to handle the network connection (and not block the GUI thread)

### 2020-03-07

* Add color option


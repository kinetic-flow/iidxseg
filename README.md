# iidxseg

![screenshot](https://raw.githubusercontent.com/minsangkim89/iidxseg/7c361018475446fb86a9bcef9d9ac32894fb58f1/res/readme/2019-09-15.gif?token=ANCXP72DCKTMFDSJ6ZKIXMC5P27JI)

IIDX segment display software emulator

## Dependencies
Tested on Python 3.7.3. Requires [DSEG14Classic-Italic font](https://www.keshikan.net/fonts-e.html), pygame, and SpiceAPI.

## Instructions

First of all, launch spicetools with API server enabled. Then, launch with:

    py ticker.py server_ip port password

e.g., for running locally -

    py ticker.py localhost 50000 "MyPass123"

or, over the network by IP -

    py ticker.py "192.168.1.200" 50000 "MyPass123"
    
Display a timer (only ticks up) and the current time:

    py ticker.py "192.168.1.200" 50000 "MyPass123" --timer --clock
    
Launch it borderless, exactly where you want it:

    py ticker.py "192.168.1.200" 50000 "MyPass123" --width 1280 --height 720 --x 200 --y 100

## Updates

### 2020-03-01

Made the window resizable. Borderless option added. A bunch of command line options added for adjusting the window size at launch.

### 2020-03-06

Add timer and wall clock. Spawn a separate process to handle the network connection (and not block the GUI thread)

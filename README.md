# i3pamicstatus.py

aka "i3 PulseAudio Microphone Status"

## What does it do?

`i3pamicstatus.py` is a simple
[`i3status`](https://i3wm.org/docs/i3status.html) decorator that displays the
PulseAudio microphone status.

It displays a green 
[microphone icon](https://fontawesome.com/icons/microphone?s=solid&f=classic)
if any microphones are listening, otherwise it displays a gray
[microphone-slash icon](https://fontawesome.com/icons/microphone-slash?s=solid&f=classic).

![screen recording](status-bar.gif)

This requires that the consumer of your `i3status` (eg: `i3bar`) is using Font
Awesome or a compatible font.

It determines that a microphone is listening by checking if any PulseAudio
"source" is in the "running" state.


### BlinkStick support

i3pamicstatus supports [BlinkStick](https://www.blinkstick.com/) devices.

Note that in order to enable this support, you'll need to manually install the
[BlinkStick Python module](https://pypi.org/project/BlinkStick/). This module
is not listed in `requirements.txt`, because it is optional.

If the `blinkstick` Python module is installed, then the first BlinkStick
device found will be used, and will light up when a microphone is active.
i3pamicstatus is tolerant of the BlinkStick device appearing or disappearing
while it's running.

[![i3pamicstatus BlinkStick Demo](https://img.youtube.com/vi/D7ecg1Aq54k/0.jpg)](https://www.youtube.com/watch?v=D7ecg1Aq54k)

## Why does this exist?

See [this post](https://oldbytes.space/@xenomachina/109321893672994770) that
explains why I made this, and shows a small video of the BlinkStick support in
action.


## To Do

- Right now, there's are no configuration options, but it'd be nice if you
  could configure a few things (options shown are proposals):
    - status bar on/off text (`--on-label` & `--off-label`)
    - status bar on/off color (`--on-color` & `--off-color`)
    - BlinkStick on/off color (`--on-led` & `--off-led`)
    - BlinkStick serial number (right now it uses the first BlinkStick found)
      (`--led-serial`)
    - ability to disable blinkstick? (`--disable-led`)

- A mode that doesn't require `i3status` input, but that instead polls on a
  specified interval might be useful, especially for users who just want the
  BlinkStick support. (`--poll-seconds`)

## Usage

Use it as part of your `i3status` pipeline.

For example, if you're using i3, change the `status_command` in `./i3/config`
to something like:

``` config
bar {
    status_command i3status | some/path/i3pamicstatus.py
    ...
```

`i3pamicstatus.py` expects to read JSON lines from stdin, and outputs those
JSON lines to stdout with the microphone status injected. In the example above,
`i3status` generates the initial set of status lines, which `i3pamicstatus.py`
adds to, and then i3bar consumes these to format and display on your desktop.

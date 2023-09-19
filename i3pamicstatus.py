#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright ©2022 Laurence Gonsalves
# All rights reserved.
#
# This program comes without any warranty, to the extent permitted by
# applicable law.

"""
i3 PulseAudio Microphone Status

A simple i3status wrapper which appends each i3status line with the current
pulseaudio microphone status.

See README.md for details on usage.
"""

import json
import pulsectl
import re
import sys

# https://pypi.org/project/BlinkStick/ is optional
try:
    from usb import USBError
    from blinkstick import blinkstick

    def set_led(value):
        try:
            light = blinkstick.find_first()
            if light:
                light.set_color(hex=LED_COLORS[value])
        except (AttributeError, USBError):
            # Sometimes blinkstick throws one of these exceptions if the
            # device is removed while we are interacting with it, so we
            # silently ignore them.
            pass

except ModuleNotFoundError:
    # make set_led a no-op if we can't import blinkstick module
    def set_led(value):
        pass


pulse = pulsectl.Pulse('i3pamicstatus')


def is_listening():
    return any(x.state == pulsectl.pulsectl.PulseStateEnum.running
               for x in pulse.source_list())

def is_unmute():
    default_source_name = pulse.server_info().default_source_name
    default_source_idx = -1
    for source_id in range(0, len(pulse.source_list())):
        source = pulse.source_list()[source_id]
        if source.name == default_source_name:
            default_source_idx = source_id
            break
    if default_source_idx < 0:
        return False
    return pulse.source_list()[default_source_idx].mute == 0


# See https://i3wm.org/docs/i3bar-protocol.html
OUTPUTS = {
    True: {
        'full_text': '',  # microphone
        'color': '#2dc66d',
    },

    False: {
        'full_text': '',  # muted microphone
        'color': '#666666',
    },
}

for k in OUTPUTS:
    OUTPUTS[k]['name'] = 'i3pamicstatus'
    OUTPUTS[k]['align'] = 'center'
del k


LED_COLORS = {
    False: "#000000",
    True: "#003300",
}

class cmdline_arguments:
    """
    Class to parse command line arguments and set the corresponding options.
    Arguments to parse:

    --show-muted    show whether the microphone is muted or not instead of listening

    Also this class stores options that could be used to change the behavior
    of the program.
    """
    options = {
        "show-muted": False, # show when mic muted/unmuted
    }
    def __init__(self):
        if len(sys.argv) <= 1:
            return
        for arg in sys.argv[1:]:
            opt = arg[2:]
            if opt in self.options:
                self.options[opt] = True

def get_status(cl_args):
    """
    Returns the current status

    Result is a sequence of i3status dictionaries representing "blocks" as
    defined here: https://i3wm.org/docs/i3bar-protocol.html#_blocks_in_detail

    Other side effects based on the status should also be performed here.
    """
    if cl_args.options['show-muted']:
        value = is_unmute()
    else:
        value = is_listening()
    set_led(value)
    return [OUTPUTS[value]]


def read_line():
    """
    Reads line of i3status output, returns (prefix, json)

    prefix is a comma or empty string, json is the rest of the line.

    Terminates program if end of input is reached.
    """
    try:
        line = sys.stdin.readline().strip()
        # i3status sends EOF, or an empty line
        if not line:
            sys.exit(3)
        return line
    except KeyboardInterrupt:
        sys.exit()


JSON_LINE_RE = re.compile(r'^(,?)(.*)$')


def read_json_line():
    prefix, line = JSON_LINE_RE.match(read_line()).groups()
    fields = json.loads(line)
    return prefix, fields

def main():
    # Process the command line arguments
    cl_args = cmdline_arguments()

    # Read i3status output
    print(read_line(), flush=True)  # version header
    print(read_line(), flush=True)  # start of infinite array
    while True:
        prefix, fields = read_json_line()
        fields.extend(get_status(cl_args))

        print(prefix, end='')
        print(json.dumps(fields), flush=True)


if __name__ == '__main__':
    main()

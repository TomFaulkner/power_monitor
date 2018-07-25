#!/usr/bin/env python3
import subprocess

import pync


def log_status():
    # TODO: Delete this
    o = subprocess.run('pmset -g batt'.split(), stdout=subprocess.PIPE)
    try:
        battery_level = o.stdout.decode().strip().split('\t')[1].split(';')[0]
        with open('battery_level.txt', 'a') as f:
            f.write(f'{battery_level}\n')
    except Exception:
        pync.notify('Unable to read battery, something went wrong')

    with open('battery_output.txt', 'a') as f:
        f.write(o.stdout.decode())


"""
Fully charged output:
Now drawing from 'AC Power'
 -InternalBattery-0 (id=3997795)	100%; charged; 0:00 remaining present: true

Not charging, but attached output:
 Now drawing from 'AC Power'
 -InternalBattery-0 (id=3997795)	79%; AC attached; not charging present: true

Recently plugged in output:
Now drawing from 'AC Power'
 -InternalBattery-0 (id=3997795)	78%; charging; (no estimate) present: true

Unplugged output:
Now drawing from 'Battery Power'
 -InternalBattery-0 (id=3997795)	100%; discharging; 7:26 remaining present: true
"""


def get_power_status():
    # TODO: Cleanup outputs
    results = subprocess.run('pmset -g batt'.split(), stdout=subprocess.PIPE)
    output = results.stdout.decode()
    drawing, line_2 = output.strip().split('\n')
    battery_number, details = line_2.split('\t')
    percent_charged, status, remainder = details.split(';')
    estimate, present = remainder.split(' present: ')
    return drawing, battery_number, percent_charged, status, estimate, present


def check_status():
    _, _, _, _, status, _ = get_power_status()
    if "not charging" in status:
        pync.notify("Plugged in but not charging!")


if __name__ == '__main__':
    log_status()  # TODO: Remove this
    check_status()

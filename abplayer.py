#!/usr/bin/env python3
import subprocess
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-c',
                    '--cut',
                    nargs=3,
                    help='Cuts the file specified in SOURCE with DURATION in seconds (e.g. 10.0)',
                    metavar=('SOURCE','DESTINATION','DURATION'))

args = parser.parse_args()

if args.cut:
    source = os.path.expanduser(os.path.abspath(args.cut[0]))
    destination = args.cut[1]
    duration = args.cut[2]
    
    if not "." in duration:
        raise ValueError("Duration was not in decimal form. Received " + duration)
        sys.exit()
    
    splitted = source.split('/')
    
    filename = splitted[len(splitted)-1]
    filename = filename.replace('.mp3', '')

    if not os.path.isdir(destination):
        os.mkdir(destination)

    cmd = "sox -V3 \"" + source + "\" \"" + destination + ".mp3\" silence -l 0 1 " + duration + " 0.1% : newfile : restart"
    print(cmd)
    #subprocess.call(cmd, shell=True)

    count = subprocess.check_output("ls -1 \"" + destination + "\" | wc -l", shell=True, encoding='UTF-8')
    print("Files generated: " + str(count))



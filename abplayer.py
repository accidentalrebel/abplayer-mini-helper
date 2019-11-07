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
    destination = os.path.expanduser(os.path.abspath(args.cut[1]))
    duration = args.cut[2]
    
    if not "." in duration:
        raise ValueError("Duration was not in decimal form. Received " + duration)
        sys.exit()
    
    splitted = source.split('/')
    
    filename = splitted[len(splitted)-1]
    filename = filename.replace('.mp3', '')

    if not os.path.isdir(destination):
        os.mkdir(destination)
    elif len(os.listdir(destination)) > 0:
        print("Directory \"" + destination + "\" is not empty.")
        choice = input("Delete files inside directory? (Y/n): ")
        if choice == "Y":
            for f in os.listdir(destination):
                print("Deleting: " + destination + "/" + f)
                os.remove(destination + "/" + f)
        else:
            print("Received \"" + choice + "\". Exiting...")
            sys.exit()

    cmd = "sox -V3 \"" + source + "\" \"" + destination + "/.mp3\" silence -l 0 1 " + duration + " 0.1% : newfile : restart"
    print(cmd)
    subprocess.call(cmd, shell=True)

    print("Files generated: " + str(len(os.listdir(destination))))



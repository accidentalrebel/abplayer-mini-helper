
#!/usr/bin/env python3
import subprocess
import argparse
import os
import sys
from shutil import copyfile

USB_PATH = "/run/media/arebel/DASHCAM/"

parser = argparse.ArgumentParser()
parser.add_argument('-m',
                    '--merge',
                    nargs=2,
                    help='Merges all files specified in SOURCE and saves to DESTINATION path.',
                    metavar=('SOURCE','DESTINATION'))
parser.add_argument('-c',
                    '--cut',
                    nargs=3,
                    help='Cuts the file specified in SOURCE with DURATION in seconds (e.g. 10.0) and save to DESTINATION folder.',
                    metavar=('SOURCE','DESTINATION','DURATION'))
parser.add_argument('-t',
                    '--transfer',
                    nargs=1,
                    help='Transfers the files from SOURCE folder.',
                    metavar=('SOURCE'))
parser.add_argument('-s',
                    '--start',
                    type=int,
                    default=1,
                    help='Specifies the start index.')
parser.add_argument('-e',
                    '--end',
                    type=int,
                    default=-1,
                    help='Specifies the end index.')

args = parser.parse_args()

if args.merge:
    source = os.path.expanduser(os.path.abspath(args.merge[0]))
    destination = os.path.expanduser(os.path.abspath(args.merge[1]))

    if not os.path.isdir(source):
        raise ValueError("Source should be a directory");
        sys.exit()

    files = []
    for f in os.listdir(source):
        if not ".mp3" in f:
            continue
        
        files.append(source + "/" + f)

    files.sort()

    cmd = "cat "
    for f in files:
        print(f)
        cmd += " \"" + f + "\" "

    cmd += " > \"" + destination + "\""
    #print(cmd)
    subprocess.call(cmd, shell=True)
        
elif args.cut:
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
elif args.transfer:
    cmd = "udisksctl mount -b /dev/sdb1"
    subprocess.call(cmd, shell=True)
    
    choice = input("Delete all files in the USB? (Y/n): ")
    if choice == "Y":
        print('Removing files in ' + USB_PATH)
        for f in os.listdir(USB_PATH):
            if os.path.isdir(USB_PATH + f):
                continue
            os.remove(USB_PATH + f)

    init_count = len(os.listdir(USB_PATH))

    source_path = os.path.expanduser(os.path.abspath(args.transfer[0]))
    
    start_index = args.start
    end_index = args.end

    if end_index <= -1:
        end_index = len(os.listdir(source_path))

    if start_index > end_index:
        raise ValueError("Start index should not be bigger than end index!")
        sys.exit()

    j = init_count + 1
    for i in range(start_index, end_index + 1):
        s = source_path + "/" + f"{i:03}" + ".mp3"
        d = USB_PATH + f"{j:03}" + ".mp3"
        print("Copying " + s + " to " + d)
        copyfile(s, d)
        j = j + 1
    
    

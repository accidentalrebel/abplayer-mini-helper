import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c',
                    '--cut',
                    nargs=2,
                    help='Cuts the file specified in SOURCE with DURATION in seconds (e.g. 10.0)',
                    metavar=('SOURCE','DURATION'))

args = parser.parse_args()

if args.cut:
    source = args.cut[0]
    duration = args.cut[1]
    if not "." in duration:
        raise ValueError("Duration was not in decimal form. Received " + duration)
        sys.exit()
    
    splitted = source.split('/')
    
    directory = splitted[1:len(splitted)-1]
    directory = '/'.join(directory)
    
    filename = splitted[len(splitted)-1]
    filename = filename.replace('.mp3', '')
    
    cmd = "sox -V3 " + args.cut[0] + " " + directory + "/" + filename + "_part_.mp3 silence -l 0 1 " + duration + " 0.1% : newfile : restart"
    print(cmd)
    # subprocess.call(cmd, shell=True)



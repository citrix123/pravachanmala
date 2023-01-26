from pravachanmala import pravachans
import sys
import argparse

# Version string
VERSION = 1.0
parser = argparse.ArgumentParser()
parser.add_argument("--playlist", help="please enter a playlist", required=True)
parser.add_argument("--save-dir", help="where to save ?", default="./converted/")
parser.add_argument("--version", help="prints version of paravachanmala")
parser.add_argument("--jobs", help="prints version of paravachanmala", default=4, type=int)

if __name__ == "__main__":
    args = parser.parse_args()

    if args.version:
        print ("Version : {}".format(VERSION))
    p = pravachans(args)
    p.start_download()

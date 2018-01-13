#!/usr/bin/env python

import json
import argparse
import os
import subprocess

def parse_args():
    """ parse arguments out of sys.argv """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-j",
        "--job-file",
        type=str,
        required=True,
        help="Path to JSON job file."
    )
    parser.add_argument(
        '-s',
        '--start',
        type=int,
        default=0,
        help="First frame."
    )
    return parser.parse_args()

FFMPEG = (
    'ffmpeg -r 15 -start_number {0} -i {1}{2}.%3d.png -c:v libx264 -vf'
    ' "scale=iw/4:ih/4,format=yuv420p" {2}.mp4'
)

def main():
    """main function for module"""
    args = parse_args()

    with open(args.job_file, 'ra') as fi:
        job_desc = json.loads(fi.read())

    print(job_desc)
    cmd = FFMPEG.format(
        args.start,
        job_desc['dir'] + os.path.sep,
        job_desc['prefix']
    )

    print(cmd)
    returncode = subprocess.call(cmd, shell=True)
    if returncode:
        raise RuntimeError(
            "ffmpeg returned non-zero error code: {0}".format(
                returncode
            )
        )

    
if __name__ == '__main__':
    main()

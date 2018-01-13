#!/usr/bin/env python

import json
import argparse
import os
import subprocess

def parse_args():
    """ parse arguments out of sys.argv """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-d',
        '--dryrun',
        action="store_true",
        default=False,
        help="Print out command instead of running it."
    )
    parser.add_argument(
        "job_file",
        type=str,
        help="Path to JSON job file."
    )
    parser.add_argument(
        '-s',
        '--start',
        type=int,
        default=0,
        help="First frame."
    )
    parser.add_argument(
        '-e',
        '--end',
        type=int,
        default=-1,
        help="Final frame.  - means count back from end."
    )
    parser.add_argument(
        '-p',
        '--preview',
        default=False,
        action='store_true',
        help="Preview timelapse in RV rather than making movie."
    )
    return parser.parse_args()

FFMPEG = (
    'ffmpeg -r 15 -start_number {0} -i {1}.%03d.png -c:v libx264 -vframes {3} '
    '-vf "scale=iw/4:ih/4,format=yuv420p" {2}.mp4'
)

RV = 'rv {1}.%03d.png {0}-{3}'

def main():
    """main function for module"""
    args = parse_args()

    with open(args.job_file, 'ra') as fi:
        job_desc = json.loads(fi.read())

    if args.end < 0:
        # print(job_desc)
        final_fnum = int(os.path.basename(job_desc['files'][-1]).split('.')[-2])
        final_fnum = final_fnum + 1 + args.end
    else:
        final_fnum = args.end

    final_fnum = final_fnum + 1 + args.end
    print final_fnum

    path_with_prefix = os.path.join(job_desc['dir'], job_desc['prefix'])

    if args.preview:
        cmd = RV.format(
            args.start,
            path_with_prefix,
            job_desc['prefix'],
            final_fnum
        )
    else:
        cmd = FFMPEG.format(
            args.start,
            path_with_prefix,
            job_desc['prefix'],
            int(final_fnum)-int(args.start),
        )

    if args.dryrun:
        cmd = '[DRYRUN] ' + cmd
    print(cmd)
    if not args.dryrun:
        returncode = subprocess.call(cmd, shell=True)
        if returncode:
            raise RuntimeError(
                "ffmpeg returned non-zero error code: {0}".format(
                    returncode
                )
            )

    
if __name__ == '__main__':
    main()

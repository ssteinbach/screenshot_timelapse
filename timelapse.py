#!/usr/bin/env python

""" Simple timelapse script using mac os built in screengrab system """

import argparse, os, itertools, time, subprocess

SCREENGRAB_BIN_PATH = "/usr/sbin/screencapture"

def parse_args():
    """ parse arguments out of sys.argv """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-d',
        '--dirname',
        required = True,
        type=str,
        help='Directory to save files in.'
    )
    parser.add_argument(
        '-p',
        '--prefix',
        default = '',
        type=str,
        help='Prefix string for the file names.'
    )
    parser.add_argument(
        '-s',
        '--sleep',
        default=5,
        type=int,
        help="Amount in seconds to wait in between screen grabs.",
    )
    parser.add_argument(
        '-f',
        '--force',
        default=False,
        action='store_true',
        help="Overwrite files if they already exist.",
    )
    return parser.parse_args()

def main():
    """Infinite loop of screenshots."""
    args = parse_args()

    counter = itertools.count()
    while True:
        # wait
        time.sleep(args.sleep)

        ind = next(counter)
        prefix = args.prefix + '.' if args.prefix else ''
        fname = os.path.join(
            args.dirname,
            '{0}{1:03d}.png'.format(prefix, ind)
        )

        if os.path.exists(fname) and not args.force:
            raise RuntimeError("File already exists: {0}".format(fname))

        # screen grab
        cmd = "/usr/sbin/screencapture {0}".format(fname)

        returncode = subprocess.call(cmd, shell=True)
        if returncode:
            raise RuntimeError(
                "screengrab returned non-zero error code: {0}".format(
                    returncode
                )
            )

        print(
            "Took screengrab: {0}, waiting {1} seconds.".format(
                fname,
                args.sleep
            )
        )

if __name__ == '__main__':
    main()

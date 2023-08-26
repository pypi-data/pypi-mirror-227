#!/usr/bin/env python3

import os
import subprocess

def sync_drive(args):
    """Sync a local directory to a Google Drive directory using rsync."""
    try:
        drive_dir = f"{os.environ['GOOGLEDRIVE']}"
        drive_dir = f"{os.environ['SHAREDRIVE']}"
    except KeyError:
        print('GOOGLEDRIVE environment variable is not defined. Error...')
        exit()
    project_name = os.path.basename(os.getcwd()) if args.project_name is None else args.project_name 
    local_dir = f"{args.folder}/{args.subdir}/"
    drive_dir = f"{project_name}/{args.folder}/{args.subdir}/"
    if args.target == 'personal':
        drive_dir = f"{os.environ['GOOGLEDRIVE']}/{drive_dir}"
    else:
        drive_dir = f"{os.environ['SHAREDRIVE']}/{drive_dir}"
    if args.open:
        cmd = ["open", f"{drive_dir}"]
        subprocess.run(cmd, check=True)
        return
    if args.list:
        cmd = ["ls", f"{os.environ['GOOGLEDRIVE']}"] if args.target == 'personal' else ["ls", f"{os.environ['SHAREDRIVE']}"]
        subprocess.run(cmd, check=True)
        return
    includes = ["--include=*.tsv", "--include=*.csv",
                "--include=*.txt", "--include=*.xlsx", "--include=*/"]
    excludes = ["--exclude=*"]
    max_size = f"--max-size={args.max_size_mb}mb"
    cmd = ["rsync", "-avhW"]
    if args.debug:
        cmd.append("--dry-run")
    cmd = cmd + includes + excludes + [max_size]
    if args.dir == 'up':
        cmd.extend([local_dir, drive_dir])
    else:
        cmd.extend([drive_dir, local_dir])
    subprocess.run(cmd, check=True)
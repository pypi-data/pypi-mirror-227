# teamconnector

## Overview

`teamconnector` is a command-line tool for interacting with various cloud storage and remote server platforms. It provides a simple and unified interface for managing files and directories across different platforms, making it easier to work with data in a distributed environment.

## Installation

To install `teamconnector`, you can use pip:

`pip install teamconnector`
## Usage

`tc config` 

This command lists all the environment variables that are currently described in your `~/.bashrc` or Conda environment.

## local to Google Drive

`tc drive -ls`
This command lists all the files and folders in your Google Drive Shared directory.


`# tc drive -ls -t personal`
This command lists all the files and folders in your Google Drive "Personal" directory.

`tc drive -o -p aouexplore`
This command opens the "aouexplore" shared drive in your Google Drive.

`tc drive -o -p aouexplore -s sample_qc`
This command opens the "sample_qc" folder in the "aouexplore" shared drive in your Google Drive.

`tc --debug drive --dir up --subdir sample_qc`
This command uploads the "sample_qc" folder to the parent directory of your Google Drive root directory.

`tc drive --dir up --subdir sample_qc`
This command uploads the "sample_qc" folder to the parent directory of your Google Drive root directory.

## local to Google Cloud

Need to set `BUCKET_NAME` within your Makefile and Conda environment.

`tc gcp -ls`
This command lists all the files and folders in your Google Cloud Storage bucket described in `BUCKET_NAME`.


`tc -n gcp --dir down --subdir phenotypes`
This command downloads the "phenotypes" folder from your Google Cloud Storage bucket to your local machine.

# remote

`tc remote -r /gpfs/commons/groups/singh_lab/projects/gpc_array/ --dir down --subdir preprocessing`

This command downloads the "preprocessing" folder from the remote server at "/gpfs/commons/groups/singh_lab/projects/gpc_array/" to your local machine.

## Cite

## Maintainer

[Tarjinder Singh @ ts3475@cumc.columbia.edu](ts3475@cumc.columbia.edu)

## Acknowledgements

## Release Notes
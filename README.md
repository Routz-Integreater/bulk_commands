# Bulk commands

Script to run bulk commands over SSH on a multitude of files

## Usage

```
usage: bulk_commands [-h] [-c commands | -f command_file] [-m maxthreads] [-n] [-p] [-s filename] [-v] devices [devices ...]

positional arguments:
  devices               Hostnames or files with a list of hostnames to process

optional arguments:
  -h, --help            show this help message and exit
  -c commands, --commands commands
                        The commands to send to the device
  -f command_file, --command_file command_file
                        A file containing the the commands to send
  -m maxthreads, --max_threads maxthreads
                        How many devices to do concurrent
  -n, --no-output       Hide the output of the devices from STDIN
  -p, --start-at-prompt
                        Starts the output to the streams as soon as it finds a prompt
  -s filename, --save_output filename
                        File to write the device output to
  -v, --verbose         The amount of logging to display
```

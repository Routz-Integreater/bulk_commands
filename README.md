# Bulk commands

Script to run bulk commands over SSH on a multitude of devices. Can either use a static command or commands, or a file that contains the commands to be executed.

## Usage instructions

The `bulk_commands` command should be run on the terminal and has the following usage:

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

## Examples

To run the `show version` command on a multitude of devices:

```
bulk_commands -c "show version" switch1 switch2 switch3
```

To run a few commands on a multitude of devices and save them to individual files:

```
bulk_commands -c "show version; show interface description" -s %h.txt switch1 switch2 switch3
```

To run a few commands from a file on a multitude of devices, running on 32 devices at the same time:

```
bulk_commands -f commands.txt -m 32 switch1 switch2 switch3
```
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/Routz-Integreater/bulk_commands)

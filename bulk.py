#!/usr/bin/env/python3
"""
    Bulk Command
    Version 0.1
    Author: Daryl Stark (daryl.stark@routz.nl)

    Script to run multiple commands on multiple devices.
"""
#---------------------------------------------------------------------------------------------------
# Imports
import argparse
import logging
import os
import getpass
import sys
from bulk_commands import BulkCommand
#---------------------------------------------------------------------------------------------------
# Main method
def main():
    # Create a ArgumentParser and set the needed arguments
    parser = argparse.ArgumentParser()

    # Positional arguments
    parser.add_argument('devices', metavar = 'devices', type = str, help = 'Hostnames or files with a list of hostnames to process', nargs = '+')

    # Mutually exclusive group; either a list of commands is send or a file containing commands
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--commands', metavar = 'commands', type = str, help = 'The commands to send to the device')
    group.add_argument('-f', '--command_file', metavar = 'command_file', type = str, help = 'A file containing the the commands to send')

    # Optional arguments
    parser.add_argument('-m', '--max_threads', metavar = 'maxthreads', type = int, help = 'How many devices to do concurrent', default = 1)
    parser.add_argument('-n', '--no-output', action = 'store_true', help = 'Hide the output of the devices from STDIN')
    parser.add_argument('-p', '--start-at-prompt', action = 'store_true', help = 'Starts the output to the streams as soon as it finds a prompt')
    parser.add_argument('-s', '--save_output', metavar = 'filename', type = str, help = 'File to write the device output to')
    parser.add_argument('-v', '--verbose', action = 'count', help = 'The amount of logging to display', default = 0)

    # Parse the argument
    args = parser.parse_args()

    # Set up the logger
    logger = logging.getLogger('MAIN')

    # Default loglevel is Warning
    loglevel = logging.WARNING

    if args.verbose == 1:
        loglevel = logging.INFO
    if args.verbose > 1:
        loglevel = logging.DEBUG

    logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = loglevel)
    logger.debug('Logger is created, arguments are parsed. Let\'s start processing the data!')

    # Find the devices to process
    devices = set()
    for host_arg in args.devices:
        # Expand the user for the argument
        host_arg = os.path.expanduser(host_arg)

        # Check if this is a file. If it is, we use that file as a list of hostnames
        if os.path.isfile(host_arg):
            logger.debug('The host "{argument}" is a file'.format(argument = host_arg))
            with open(host_arg, 'r') as inputfile:
                # Get the hosts in the file and remove the newline
                host_list = set([ x.strip() for x in inputfile.readlines() ])
                logger.debug('Found {cnt} hosts in file "{filename}"'.format(cnt = len(host_list), filename = host_arg))

                # Add the new hosts to the set with all devices
                devices.update(host_list)
        else:
            logger.debug('The host "{argument}" is not a file so will be used as hostname'.format(argument = host_arg))
            # Add the device to the set with all devices to process
            devices.add(host_arg)

    logger.info('Starting script for {cnt} hosts'.format(cnt = len(devices)))

    # Make sure we have the credentials to log into the device
    logger.debug('Checking if there is a .pass file to use')
    try:
        with open(os.path.expanduser('~/.pass')) as passfile:
            logger.info('Using credentials from .pass file in home directory')
            password = passfile.readline().strip()
            username = getpass.getuser()
    except FileNotFoundError:
        logger.debug('No .pass file found; ask the user for credentials')
        username = input('Username: ')
        password = getpass.getpass('Password: ')

    # Read the commands that are to be performed
    commands = list()
    if args.command_file:
        try:
            logger.debug('Opening commandfile "{commands}"'.format(commands = args.command_file))
            with open(args.command_file) as commandfile:
                logger.debug('Commandfile "{commands}" exists'.format(commands = args.command_file))
                commands = commandfile.readlines()
        except FileNotFoundError:
            logger.critical('File "{commands}" does not exist!'.format(commands = args.command_file))

    if args.commands:
        logger.debug('Commands given via the command line: "{commands}"'.format(commands = args.commands))
        commands = args.commands.split(';')

    if len(commands) == 0:
        logger.debug('No commands given; we need to get the commands from STDIN')
        # If no file is specified, we are going to read the STDIN
        print('Enter commands, end with CTRL+D')
        for line in sys.stdin:
            commands.append(line)

    # Remove newlines from the commands
    commands = [ x.strip() for x in commands if x.strip() != '' ]

    logger.info('Got {count_commands} commands to run on the {count_devices} devices'.format(
        count_commands = len(commands),
        count_devices = len(devices)
    ))

    # We have the devices and the commands; we can start
    bulk = BulkCommand(
        devices = devices,
        threads = args.max_threads,
        username = username,
        password = password,
        commands = commands,
        hide = args.no_output,
        output_file = args.save_output,
        start_at_prompt = args.start_at_prompt
    )
    bulk.start()
#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
#---------------------------------------------------------------------------------------------------

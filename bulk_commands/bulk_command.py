#!/usr/bin/env/python3
#---------------------------------------------------------------------------------------------------
# Imports
from bulk_commands import CombinedStreams
import concurrent.futures
import logging
import os
import sys
import pexpect
import datetime
#---------------------------------------------------------------------------------------------------
class AuthenticationErrorException(Exception):
    """ Exception that is raised when the authentication fails """
    pass
#---------------------------------------------------------------------------------------------------
class BulkCommand:
    """ Class to run commands on devices """

    def __init__(self, devices, threads, username, password, commands, hide = False, output_file = None):
        """ Initiator sets default values """

        # Set specific values
        self.devices = devices
        self.threads = threads
        self.username = username
        self.password = password
        self.commands = commands
        self.output_file = output_file

        # Set the stream for the 'pexpect' module
        self.default_stream = None
        if hide == False:
            self.default_stream = sys.stdout

        # Create a logger
        self.logger = logging.getLogger('BulkCommand')

    def process_device(self, devicename):
        """ The method that does the actual processing """

        # Create a logger
        devicename = devicename.upper()
        logger = logging.getLogger(devicename)
        logger.info('Starting processing device "{devicename}"'.format(devicename = devicename))

        # New stream combiner
        outstream = CombinedStreams()
        if self.default_stream:
            outstream.add(self.default_stream)

        # If the user specified a file to write to, add it to the output streams
        if self.output_file:
            # Create objects for the date and time
            today = datetime.date.today()
            now = datetime.datetime.now()

            # Replace the variables in the filename
            filename = os.path.expanduser(self.output_file)
            filename = filename.replace('%h', devicename)
            filename = filename.replace('%d', today.strftime('%Y-%m-%d'))
            filename = filename.replace('%t', now.strftime('%H.%M.%S'))

            # Add the default stream and the filestream if needed
            outfile = None

            try:
                logger.debug('Opening "{filename}" in append mode'.format(filename = filename))
                outfile = open(filename, 'a')
                outstream.add(outfile)
            except:
                logging.critical('File "{filename}" couldn\'t be opened for writing in append mode'.format(filename = filename))

        # Log in to the device
        try:
            sshp = pexpect.spawn('ssh {username}@{host}'.format(username = self.username, host = devicename), encoding = 'utf-8')
            sshp.logfile_read = outstream

            # Search for the password prompt
            loggedin = False
            while not loggedin:
                response = sshp.expect([ 'Password: ', '(yes/no)' ])
                if response == 0:
                    logger.debug('Sending password')
                    sshp.sendline(self.password)
                    response = sshp.expect([ '^.+\#', 'Password: ' ])
                    if response == 0:
                        loggedin = True
                    else:
                        raise AuthenticationErrorException('Password is incorrect')
                else:
                    logger.debug('We got a "yes/no" question: "{before}". Sending "yes"'.format(before = sshp.before))
                    sshp.sendline('yes')

            # Set the terminal length to 0
            sshp.sendline('term len 0')
            sshp.expect('^.+\#')

            # Execute the commands
            for command in self.commands:
                logger.debug('Sending command "{command}"'.format(command = command))
                sshp.sendline(command)
                response = -1
                while response < 2:
                    response = sshp.expect([ '^.+\#', pexpect.EOF, '[confirm]' ], timeout = 600)
                    if response == 2:
                        sshp.send('\n')
                        sshp.expect('^.+\#')

            # Close the connection
            sshp.sendline('exit')
            sshp.close()
        except AuthenticationErrorException:
            logger.critical('Password is incorrect!')
        except Exception as e:
            logger.critical('Couldn\'t connect to "{devicename}"'.format(devicename = devicename))
            logger.debug('Error was: {e}'.format(e = e))

        # Close the file
        if self.output_file:
            if outfile:
                outfile.close()

        # Done
        logger.info('Done with device "{devicename}"'.format(devicename = devicename))

    def start(self):
        """ Method to start the actual processing of the devices in a threaded way """

        self.logger.info('Starting processing the devices with {threads} threads'.format(threads = self.threads))

        with concurrent.futures.ThreadPoolExecutor(max_workers = self.threads) as executor:
            executor.map(self.process_device, self.devices)
#---------------------------------------------------------------------------------------------------

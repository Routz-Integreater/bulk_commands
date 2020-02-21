#!/usr/bin/env/python3
#---------------------------------------------------------------------------------------------------
# Imports
import io
#---------------------------------------------------------------------------------------------------
class CombinedStreams(io.StringIO):
    """ Class to use multiple streams """

    def __init__(self, streams = None):
        """ The initiator sets the default values """

        if type(streams) is list:
            self.streams = streams
        else:
            self.streams = list()

    def add(self, stream):
        """ Method to append a stream """
        self.streams.append(stream)

    def delete(self, stream):
        """ Method to delete a stream from the list """
        self.streams = [ x for x in self.streams if not x is stream ]

    def write(self, *args, **kwargs):
        """ The 'write' method writes the data to the stream """

        for stream in self.streams:
            stream.write(*args, **kwargs)
#---------------------------------------------------------------------------------------------------

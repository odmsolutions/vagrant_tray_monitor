"""Vagrant interface - commands to ask for stuff from vagrant"""
from subprocess import check_output
import re
import logging

logger = logging.getLogger(__name__)

class VagrantInterface(object):
    def __init__(self):
        # TODO - may need to have location of vagrant passed in.
        pass

    def get_columns(self, line):
        """Get the column name, start index, length from a line.
        The line is this format:
        title   title1   title2.
        Titles do not contain spaces. 
        The column length will be the next column index less 1 space. 
        The last column length will be to the end of the unstripped line"""
        matches = re.finditer("(?: |^)(\w+ *)(?= )", line)
        indexes = [(item.start(1), item.end(1)) for item in matches]
        columns = dict((line[start:end].strip(), (start, end)) for start, end in indexes)
        return columns

    def columns_to_dict(self, columns, line):
        """Create a dict from a column def and line"""
        logger.debug("Parsing line %s", line)
        return dict((name, line[start:end].strip()) for name, (start, end) in columns.items())

    def get_vms(self):
        """Get information about current vagrant vm's"""
        output = check_output("vagrant global-status", shell=True)
        lines = output.splitlines()
        logger.debug("Got lines %s", repr(lines))
        logger.debug("Getting column names")
        columns = self.get_columns(lines[0])
        logger.debug("Got %s", repr(columns))
        lines = lines[2:] # Skip the title bits
        lines = lines[:lines.index(' ')]
        logger.debug("Converting lines to columns")
        return [self.columns_to_dict(columns, line) for line in lines]

    def get_running_count(self):
        """Get the number of VM's that are running"""
        return len([item for item in self.get_vms() if item['state'] == "running"])


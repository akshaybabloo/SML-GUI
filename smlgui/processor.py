"""
Processes the selected files - Reads the samples and other specified files the converts it into an SML file.
"""
import logging

logger = logging.getLogger(__name__)

__all__ = ['check_files']


def check_files(location):
    """
    Checks the types of files and process accordingly.

    Parameters
    ----------
    location: str
        Absolute path of the folder.
    """
    if location:
        logger.info("Path selected: " + location)
    else:
        logger.info("No path provided")

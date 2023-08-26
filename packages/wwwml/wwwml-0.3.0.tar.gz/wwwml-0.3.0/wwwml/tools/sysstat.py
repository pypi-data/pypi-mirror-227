import subprocess

from langchain.tools import tool
from loguru import logger


def shell(cmd):
    output = subprocess.check_output(cmd, shell=True)
    return output


@tool
def iostat():
    """iostat - Report Central Processing Unit (CPU) statistics and input/output statistics for devices and partitions."""

    logger.info("Checking IO")
    return shell("iostat -dxsm 1 3 | grep -v loop")


@tool
def vmstat():
    """vmstat - Report virtual memory statistics."""

    logger.info("Checking Memory")
    return shell("vmstat -S m 1 3")


@tool
def mpstat():
    """mpstat - Report processors related statistics."""

    logger.info("Checking CPU")
    return shell("mpstat 1 3")


@tool
def loadavg():
    """uptime - Gives average load on system."""

    logger.info("Checking load")
    return shell("uptime")

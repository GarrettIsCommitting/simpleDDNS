# app/network.py
import socket
from requests import get
from config import settings
from std_logging import logger


def get_public_ipv4() -> str:
    """Get the public IPv4 address for the local network
    Uses the ipify.org API, others could be used if desired
    :returns
        public_ipv4(str): IPv4 address as a string
    """
    public_ipv4 = get("https://api.ipify.org").text
    logger.debug("Found public IP of {}".format(public_ipv4))
    return public_ipv4


def get_hostname() -> str:
    """Get the hostname used for DDNS from settings
    :returns
        hostname(str): Hostname as a string
    """
    hostname = "{}.{}".format(settings.host, settings.domain)
    return hostname


def does_record_match(hostname:str = get_hostname(), public_ipv4: str = get_public_ipv4()) -> bool:
    """
    Compares the address for the A record of the hostname and the public IP of the network
    :param hostname: hostname to check, by default is populated from get_hostname()
    :param public_ipv4: the IPv4 to compare against
    :return: bool
    """
    record_ipv4 = socket.gethostbyname(hostname)
    logger.debug("Resolved IP on record to {}".format(record_ipv4))
    if record_ipv4 == public_ipv4:
        return True
    return False

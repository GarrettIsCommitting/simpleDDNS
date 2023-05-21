# app/network.py
import dns.resolver
from requests import get
from app.config import settings


def get_public_ipv4() -> str:
    """Get the public IPv4 address for the local network
    :returns
        public_ipv4(str): IPv4 address as a string
    """
    public_ipv4 = get("https://api.ipify.org").text
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
    try:
        record_ipv4 = dns.resolver.resolve(hostname)
    except dns.resolver.NXDOMAIN:
        print("No record found for {}".format(hostname))
        return False
    if record_ipv4 == public_ipv4:
        return True
    return False

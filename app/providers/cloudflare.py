# app/providers/cloudflare.py
from std_logging import logger
import CloudFlare

from config import settings

if settings.dns_provider != "https://api.cloudflare.com":
    """
    Don't try and run with Cloudflare if not using the Cloudflare API
    """
    logger.exception("Trying to use the wrong DNS provider, exiting")
    raise SystemExit


def get_record_id(
        access: CloudFlare,
        zone_id: str = settings.zone_id,
        host: str = settings.host,
        domain: str = settings.domain
):
    """
    Get the ID for the DNS record for the DDNS A record
    :param access: Cloudflare object configured with access credentials
    :param zone_id: The zone ID for the DNS zone
    :param host: The host value for the DDNS address
    :param domain: The domain for the DDNS address
    :return: str | None: Returns the record id if found, otherwise returns none
    """
    try:
        records = access.zones.dns_records.get(zone_id)
    except CloudFlare.cloudflare.CloudFlareAPIError:
        logger.warning("Could not connect to Cloudflare")
        raise ConnectionError
    for record in records:
        if record['name'] == host + '.' + domain:
            logger.debug("Found {} with id of {}".format(record['name'], record['id']))
            return record['id']
    return None


def update_or_create_record(
        ipv4: str,
        access: CloudFlare,
        zone_id: str= settings.zone_id,
        host: str = settings.host,
        domain: str = settings.domain
):
    """
    Checks the zone for the record and updates or creates as appropriate
    :param ipv4: The IPv4 address the A record should point to
    :param access: Cloudflare object configured with access credentials
    :param zone_id: The zone ID for the DNS zone
    :param host: The host value for the DDNS address
    :param domain: The domain for the DDNS address
    """
    dns_record = {'name':host, 'type':'A', 'content':ipv4}
    record_id = get_record_id(access, zone_id, host, domain)
    if record_id is not None:
        try:
            access.zones.dns_records.patch(zone_id, record_id, data=dns_record)
        except CloudFlare.cloudflare.CloudFlareAPIError:
            logger.warning("Could not connect to Cloudflare")
            raise ConnectionError
    else:
        try:
            access.zones.dns_records.post(zone_id, data=dns_record)
        except CloudFlare.cloudflare.CloudFlareAPIError:
            logger.warning("Could not connect to Cloudflare")
            raise ConnectionError


cf = CloudFlare.CloudFlare(key=settings.api_key)
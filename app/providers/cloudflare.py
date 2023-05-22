# app/providers/cloudflare.py
from std_logging import logger
import CloudFlare

from config import settings

if settings.dns_provider != "https://api.cloudflare.com":
    logger.exception("Trying to use the wrong DNS provider, exiting")
    raise SystemExit


def get_record_id(
        access: CloudFlare,
        zone_id: str = settings.zone_id,
        host: str = settings.host,
        domain: str = settings.domain
):
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
    return


cf = CloudFlare.CloudFlare(key=settings.api_key)
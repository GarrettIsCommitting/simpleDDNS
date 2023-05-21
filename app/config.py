# app/config.py

import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """ Provide access to needed env parameters
        :param str domain: The root domain used for DDNS
        :param str record: The A record used for DDNS
        :param str dns_provider: The URL for the DNS provider's API
        :param str api_key: The api key for the DNS provider
        :param str zone_id: The zone id (if needed) for the DNS zone to manage
    """
    domain: str = Field('example.com', env='DYN_DOMAIN')
    host: str = Field('ddns', env='DYN_HOST')
    dns_provider: str = Field('https://api.cloudflare.com', env="DNS_PROVIDER")
    api_key: str = Field('fake_key', env='API_KEY')
    zone_id: str = Field('fake_zone_id', env="ZONE_ID")


settings = Settings()

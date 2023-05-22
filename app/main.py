# app/main.py
from time import sleep

from network import does_record_match, get_public_ipv4
from providers.cloudflare import update_or_create_record, cf


if __name__ == "__main__":
    print("Starting simpleDDNS")
    while True:
        if does_record_match():
            print("Records match, no update needed")
        else:
            print("Records do not match, updating")
            update_or_create_record(get_public_ipv4(), cf)
        print("Checking again in 15 minutes")
        sleep(900)
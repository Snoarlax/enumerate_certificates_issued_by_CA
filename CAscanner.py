#!/usr/bin/python
 #TODO: Make this multithreaded!
from threading import Thread
from queue import Queue
from time import sleep
import requests, sys
import re
import argparse

# TODO: implement AIMD

pattern=r'(?<=CN=)[^<>]+'
MAX_ATTEMPTS=5
DEFAULT_NUMBER=100

def get_caid(caid, n):
    res = None

    for tries in range(MAX_ATTEMPTS):
        try:
            res = send_request(caid, n)
            return re.findall(pattern, res.text)
        except:
            # TODO: decrease rate in a better way
            sleep(tries)

    return []

def send_request(caid, n):
    params = {
        'CN': '%',
        'iCAID': caid,
        'match': 'LIKE',
        'deduplicate': 'Y',
        'n': n
    }

    response = requests.get('https://crt.sh/', params=params)
    response.close()
    response.raise_for_status()

    return response

def print_formatted_list(list_domains):
    for domain in list_domains:
        print(domain)

def parse_file(file):
    return file.readlines()

def main():
    parser = argparse.ArgumentParser(
            prog='TODO',
            description='TODO',
    )
    parser.add_argument('-f', '--file', action='store', type=argparse.FileType('r'), help='Name of a file containing a line delimited list of caids to test')
    parser.add_argument('-i', '--caid', action='store', type=int, help='CAID of the certificate authority to search, found in CRT.sh')
    parser.add_argument('-n', '--number', action='store', type=int, default=DEFAULT_NUMBER, help='Number of domains to return from each CA. Must be less than 100,000')
    # TODO: find a way of getting more than 100,000
    args = parser.parse_args()

    if args.file:
        caids = parse_file(args.file)

        for caid in caids:
            print_formatted_list(get_caid(caid, args.number))

    if args.caid:
        print_formatted_list(get_caid(args.caid, args.number))




   
if __name__ == "__main__":
    main()


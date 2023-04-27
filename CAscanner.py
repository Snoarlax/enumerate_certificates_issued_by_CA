#!/usr/bin/python
from threading import Thread
from queue import Queue
from time import sleep
import requests, sys
import re
import argparse

# TODO: implement AIMD

pattern=r'(?<=CN=)[^<>]+'
DEFAULT_MAX_ATTEMPTS=5
DEFAULT_NUMBER=100

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

def get_caid(caid, n, retries):
    # Takes in a CAID and natural number n, returns a list of common names
    res = None

    for tries in range(retries):
        try:
            res = send_request(caid, n)
            return re.findall(pattern, res.text)
        except:
            # TODO: decrease rate in a better way
            if tries < retries - 1:
                sleep(tries)

    return []

def __get_caids(result, caid, n, retries):
    result[caid] = get_caid(caid, n, retries)

def get_caids(caid_list, n, retries):
    # Takes in a list of caids, returns a dictionary mapping CAIDs to common names for certificates issued by that CAID in that list.
    # TODO: might need to change this to map from a (caid, x) pair to CN list, where x is an index for records to return
    common_name_list = dict()
    threads = [None] * len(caid_list)
    for i in range(len(caid_list)):
        threads[i] = Thread(target=__get_caids(common_name_list, caid_list[i], n, retries))
        threads[i].start()

    for thread in threads:
        thread.join()

    return common_name_list

def print_formatted_list(list_domains):
    for domain in list_domains:
        print(domain)

def print_formatted_dictionary(dictionary_domains):
    for caid in dictionary_domains.keys():
        for domain in dictionary_domains[caid]:
            print("{0} : {1}".format(caid, domain))

def parse_file(file):
    return [s.strip() for s in file.readlines()]

def main():
    parser = argparse.ArgumentParser(
            prog='CAscanner',
            description='Uses certificate transparency logs from crt.sh to return the common name of certificates issued by a given list of CAs.',
    )
    parser.add_argument('-f', '--file', action='store', type=argparse.FileType('r'), help='Name of a file containing a line delimited list of caids to test')
    parser.add_argument('-i', '--caid', action='store', type=int, help='CAID of the certificate authority to search, found in CRT.sh')
    parser.add_argument('-n', '--number', action='store', type=int, default=DEFAULT_NUMBER, help='Number of domains to return from each CA. Must be less than 100,000')
    parser.add_argument('-r', '--retries', action='store', type=int, default=DEFAULT_MAX_ATTEMPTS, help='Number of retries when an error HTTP status code is recieved.')
    # TODO: find a way of getting more than 100,000
    args = parser.parse_args()

    if args.file:
        caids = parse_file(args.file)
        print_formatted_dictionary(get_caids(caids, args.number, args.retries))

    elif args.caid:
        print_formatted_list(get_caid(args.caid, args.number, args.retries))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()


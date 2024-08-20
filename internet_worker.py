#!/bin/python3

import base64
from colorama import init, Fore, Back, Style
import requests
import schedule
import time
from values import *


def is_connected_to_ap():
    try:
        requests.get(GATEWAY_BASE_URL, timeout=5)
        return True
    except requests.ConnectionError:
        return False

def is_internet_reachable():
    try:
        requests.get(INTERNET_CHECK_URL, timeout=5)
        return True
    except requests.ConnectionError:
        return False

def login():
    data = {'goformId': USERNAME, 'password': base64.b64encode(PASSWORD)}
    response = requests.post(f'{GATEWAY_BASE_URL}/reqproc/proc_post', data=data)
    return response.json()['result'] == '0'

def logout():
    data = {'goformId': 'LOGOUT'}
    requests.post(f'{GATEWAY_BASE_URL}/reqproc/proc_post', data=data)

def connect():
    print(Style.BRIGHT + Fore.YELLOW + "Connecting...")
    data = {'goformId': 'CONNECT_NETWORK'}
    response = requests.post(f'{GATEWAY_BASE_URL}/reqproc/proc_post', data=data)
    return_value = response.json()['result'] == 'success'
    print(Style.BRIGHT + Fore.GREEN + "Successful!" if return_value else Style.BRIGHT + Fore.RED + "Failed!")
    return return_value

def disconnect():
    print(Style.BRIGHT + Fore.YELLOW + "Disconnecting...")
    data = {'goformId': 'DISCONNECT_NETWORK'}
    response = requests.post(f'{GATEWAY_BASE_URL}/reqproc/proc_post', data=data)
    return_value = response.json()['result'] == 'success'
    print(Style.BRIGHT + Fore.GREEN + "Successful!" if return_value else Style.BRIGHT + Fore.RED + "Failed!")
    return return_value

def reconnect_internet():
    if is_connected_to_ap():
        try:
            if is_internet_reachable():
                print(Style.BRIGHT + Fore.GREEN + "Internet is reachable, waiting for next interval...")
            else:
                print(Style.BRIGHT + Fore.RED + "Internet is not reachable, trying to reconnect...")
                if not disconnect():
                    print(Style.BRIGHT + Fore.RED + "Failed to disconnect, logging in...")
                    if login():
                        print(Style.BRIGHT + Fore.GREEN + "Log in successful...")
                        disconnect()
                    else:
                        print(Style.BRIGHT + Fore.RED + "Log in failed, check credentials...")
                        return
                connect()
        except requests.ReadTimeout:
            print(Style.BRIGHT + Fore.YELLOW + "Timeout occurred, waiting for next interval...")
    else:
        print(Style.BRIGHT + Fore.YELLOW + "Not connected to AP, waiting for next interval...")


if __name__ == "__main__":
    init(autoreset=True)
    # Run the script every 10 seconds
    schedule.every(3).seconds.do(reconnect_internet)

    while True:
        schedule.run_pending()
        time.sleep(1)
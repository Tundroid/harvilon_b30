#!/bin/python3

import base64
from colorama import init, Fore, Back, Style
import requests
import schedule
import time
from values import *

connect_failure_count = 0

def is_connected_to_ap():
    try:
        requests.get(GATEWAY_BASE_URL, timeout=5)
        return True
    except requests.ConnectionError:
        return False

def is_internet_reachable():
    print(Style.BRIGHT + Fore.YELLOW + "Checking internet...: ", end="")
    try:
        requests.get(INTERNET_CHECK_URL, timeout=10)
        return True
    except requests.ConnectionError:
        return False

def login():
    print(Style.BRIGHT + Fore.YELLOW + "Logging in...: ", end="")
    data = {'goformId': USERNAME, 'password': base64.b64encode(PASSWORD)}
    response = requests.post(f'{GATEWAY_BASE_URL}/reqproc/proc_post', data=data)
    return_value = response.json()['result'] == '0'
    print(Style.BRIGHT + Fore.GREEN + "Ok!" if return_value else Style.BRIGHT + Fore.RED + "Failed, check credentials...")
    return return_value

def logout():
    data = {'goformId': 'LOGOUT'}
    requests.post(f'{GATEWAY_BASE_URL}/reqproc/proc_post', data=data)

def connect():
    print(Style.BRIGHT + Fore.YELLOW + "Connecting...: ", end="")
    data = {'goformId': 'CONNECT_NETWORK'}
    response = requests.post(f'{GATEWAY_BASE_URL}/reqproc/proc_post', data=data)
    return_value = response.json()['result'] == 'success'
    print(Style.BRIGHT + Fore.GREEN + "Ok!" if return_value else Style.BRIGHT + Fore.RED + "Failed!")
    return return_value

def disconnect():
    print(Style.BRIGHT + Fore.YELLOW + "Disconnecting...: ", end="")
    data = {'goformId': 'DISCONNECT_NETWORK'}
    response = requests.post(f'{GATEWAY_BASE_URL}/reqproc/proc_post', data=data)
    return_value = response.json()['result'] == 'success'
    print(Style.BRIGHT + Fore.GREEN + "Ok!" if return_value else Style.BRIGHT + Fore.RED + "Failed!")
    return return_value

def reboot():
    print(Style.BRIGHT + Fore.YELLOW + "Rebooting...")
    data = {'goformId': 'REBOOT_DEVICE'}
    try:
        requests.post(f'{GATEWAY_BASE_URL}/reqproc/proc_post', data=data)
    except requests.exceptions.ConnectionError:
        pass
    print(Style.BRIGHT + Fore.YELLOW + "Waiting for device", end="")
    for i in range(40):
        print(Style.BRIGHT + Fore.YELLOW + ".", end="")
        time.sleep(1)
    print()

def reconnect_internet():
    global connect_failure_count
    if is_connected_to_ap():
        try:
            if is_internet_reachable():
                print(Style.BRIGHT + Fore.GREEN + "Ok, waiting for next interval...")
                connect_failure_count = 0
            else:
                print(Style.BRIGHT + Fore.RED + "Failed, trying to reconnect...")
                connect_failure_count += 1
                if not disconnect():
                    if login():
                        disconnect()
                    else:
                        return
                connect()
        except requests.ReadTimeout:
            print(Style.BRIGHT + Fore.YELLOW + "Timeout occurred, waiting for next interval...")
            connect_failure_count += 1
    else:
        print(Style.BRIGHT + Fore.YELLOW + "Not connected to AP, waiting for next interval...")


if __name__ == "__main__":
    init(autoreset=True)
    # Run the script every 10 seconds
    schedule.every(3).seconds.do(reconnect_internet)

    while True:
        if connect_failure_count == MAX_CONNECT_FAILURE:
            connect_failure_count = 0
            reboot()
        schedule.run_pending()
        time.sleep(1)
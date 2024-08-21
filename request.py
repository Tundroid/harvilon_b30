#!/bin/python3

import base64
from colorama import init, Fore, Back, Style
import requests
import schedule
import time
from values import *

# Constants
MAX_RECONNECT_TRIES = 5

# Global variables
connect_failure_count = 0

def is_connected_to_ap() -> bool:
    """
    Check if connected to AP.
    
    Returns:
        bool: True if connected, False otherwise.
    """
    try:
        requests.get(GATEWAY_BASE_URL, timeout=5)
        return True
    except requests.ConnectionError:
        return False

def is_internet_reachable() -> bool:
    """
    Check if internet is reachable.
    
    Returns:
        bool: True if reachable, False otherwise.
    """
    print(Style.BRIGHT + Fore.YELLOW + "Checking internet...: ", end="")
    try:
        requests.get(INTERNET_CHECK_URL, timeout=10)
        return True
    except requests.ConnectionError:
        return False

def login() -> bool:
    """
    Log in to the gateway.
    
    Returns:
        bool: True if login successful, False otherwise.
    """
    print(Style.BRIGHT + Fore.YELLOW + "Logging in...: ", end="")
    data = {'goformId': USERNAME, 'password': base64.b64encode(PASSWORD)}
    response = requests.post(f'{GATEWAY_BASE_URL}/reqproc/proc_post', data=data)
    return_value = response.json()['result'] == '0'
    print(Style.BRIGHT + Fore.GREEN + "Ok!" if return_value else Style.BRIGHT + Fore.RED + "Failed, check credentials...")
    return return_value

def logout() -> None:
    """
    Log out of the gateway.
    """
    data = {'goformId': 'LOGOUT'}
    requests.post(f'{GATEWAY_BASE_URL}/reqproc/proc_post', data=data)

def connect() -> bool:
    """
    Connect to the network.
    
    Returns:
        bool: True if connected, False otherwise.
    """
    print(Style.BRIGHT + Fore.YELLOW + "Connecting...: ", end="")
    data = {'goformId': 'CONNECT_NETWORK'}
    response = requests.post(f'{GATEWAY_BASE_URL}/reqproc/proc_post', data=data)
    return_value = response.json()['result'] == 'success'
    print(Style.BRIGHT + Fore.GREEN + "Ok!" if return_value else Style.BRIGHT + Fore.RED + "Failed!")
    return return_value

def disconnect() -> bool:
    """
    Disconnect from the network.
    
    Returns:
        bool: True if disconnected, False otherwise.
    """
    print(Style.BRIGHT + Fore.YELLOW + "Disconnecting...: ", end="")
    data = {'goformId': 'DISCONNECT_NETWORK'}
    response = requests.post(f'{GATEWAY_BASE_URL}/reqproc/proc_post', data=data)
    return_value = response.json()['result'] == 'success'
    print(Style.BRIGHT + Fore.GREEN + "Ok!" if return_value else Style.BRIGHT + Fore.RED + "Failed!")
    return return_value

def reboot() -> None:
    """
    Reboot the device.
    """
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

def reconnect_internet() -> None:
    """
    Reconnect to the internet.
    """
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
        print(Style.BRIGHT + Fore.YELLOW + "Not connected to AP, searching for device...")


if __name__ == "__main__":
    init(autoreset=True)
    # Run the script every 60 seconds
    schedule.every(2).seconds.do(reconnect_internet)

    while True:
        if connect_failure_count == MAX_RECONNECT_TRIES:
            connect_failure_count = 0
            reboot()
        schedule.run_pending()
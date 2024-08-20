#!/bin/python3

import requests
import schedule
import time


def is_connected_to_ap():
    try:
        requests.get('http://192.168.213.1', timeout=5)
        return True
    except requests.ConnectionError:
        return False

def is_internet_reachable():
    try:
        requests.get('https://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False

def login():
    data = {'goformId': 'LOGIN', 'password': 'bW9sZWFkbWlu'}
    response = requests.post('http://192.168.213.1/reqproc/proc_post', data=data)
    return response.json()['result'] == '0'

def logout():
    data = {'goformId': 'LOGOUT'}
    requests.post('http://192.168.213.1/reqproc/proc_post', data=data)

def connect():
    print("Connecting...")
    data = {'goformId': 'CONNECT_NETWORK'}
    response = requests.post('http://192.168.213.1/reqproc/proc_post', data=data)
    return_value = response.json()['result'] == 'success'
    print("Successful!" if return_value else "Failed!")
    return return_value

def disconnect():
    print("Disconnecting...")
    data = {'goformId': 'DISCONNECT_NETWORK'}
    response = requests.post('http://192.168.213.1/reqproc/proc_post', data=data)
    return_value = response.json()['result'] == 'success'
    print("Successful!" if return_value else "Failed!")
    return return_value

def reconnect_internet():
    if is_connected_to_ap():
        try:
            if is_internet_reachable():
                print("Internet is reachable, waiting for next interval...")
            else:
                print("Internet is not reachable, trying to reconnect...")
                if not disconnect():
                    print("Failed to disconnect, logging in...")
                    if login():
                        print("Log in successful...")
                        disconnect()
                connect()
        except requests.ReadTimeout:
            print("Timeout occurred, waiting for next interval...")
    else:
        print("Not connected to AP, waiting for next interval...")

# Run the script every 10 seconds
schedule.every(3).seconds.do(reconnect_internet)

while True:
    schedule.run_pending()
    time.sleep(1)
#!/bin/bash
# connect
curl 'http://192.168.213.1/reqproc/proc_post' \
  --data-raw 'goformId=CONNECT_NETWORK' \
  --verbose
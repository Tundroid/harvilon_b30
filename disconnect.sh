#!/bin/bash
# disconnect
curl 'http://192.168.213.1/reqproc/proc_post' \
  --data-raw 'goformId=DISCONNECT_NETWORK' \
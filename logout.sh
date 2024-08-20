#!/bin/bash
# logout
curl 'http://192.168.213.1/reqproc/proc_post' \
  --data-raw 'goformId=LOGOUT' \
  --insecure --verbose
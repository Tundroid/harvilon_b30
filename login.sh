#!/bin/bash
# login
curl 'http://192.168.213.1/reqproc/proc_post' \
  --data-raw 'goformId=LOGIN&password=bW9sZWFkbWlu' \
  --insecure --verbose
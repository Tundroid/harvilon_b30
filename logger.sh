#!/bin/bash
echo -e "[SCRIPT]" >> detail ; cat logout.sh >> detail ; echo -e "\n\n[RESPONSE]\n# logging out" >> detail ; ./logout.sh >> detail 2>&1 ; echo -e "\n\n" >> detail
echo -e "[SCRIPT]" >> detail ; cat connect.sh >> detail ; echo -e "\n\n[RESPONSE]\n# connect without logging in" >> detail ; ./connect.sh >> detail 2>&1 ; echo -e "\n\n" >> detail
echo -e "[SCRIPT]" >> detail ; cat disconnect.sh >> detail ; echo -e "\n\n[RESPONSE]\n# disconnect without logging in" >> detail ; ./disconnect.sh >> detail 2>&1 ; echo -e "\n\n" >> detail

echo -e "[SCRIPT]" >> detail ; cat login.sh >> detail ; echo -e "\n\n[RESPONSE]\n# logging in" >> detail ; ./login.sh >> detail 2>&1 ; echo -e "\n\n" >> detail
echo -e "[SCRIPT]" >> detail ; cat connect.sh >> detail ; echo -e "\n\n[RESPONSE]\n# connect with logging in" >> detail ; ./connect.sh >> detail 2>&1 ; echo -e "\n\n" >> detail
echo -e "[SCRIPT]" >> detail ; cat disconnect.sh >> detail ; echo -e "\n\n[RESPONSE]\n# disconnect with logging in" >> detail ; ./disconnect.sh >> detail 2>&1 ; echo -e "\n\n" >> detail
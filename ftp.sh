#!/bin/bash
HOST='localhost'
USER='testuser' #  This needs to be changed
PASSWD='TestPassword' # This needs to be changed

ftp -n -v $HOST << EOT
ascii
user $USER $PASSWD
prompt
put export_service.txt
ls -la
get export_service.txt -
bye
EOT
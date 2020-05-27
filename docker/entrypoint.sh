#!/bin/bash

# Wait for the database to be up
if [[ -n $AIRSS_DATABASE_URL ]];then
    wait-for-it db:3306
fi

# Execute database migrations
/opt/venv/bin/airss-dl install

# Enter in daemon mode
sleep 99999

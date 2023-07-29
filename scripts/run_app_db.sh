#!/usr/bin/bash
# Run Flask app.py while using DbStorage using environment variables.

PS_MYSQL_USER=ps_dev PS_MYSQL_PWD=ps_dev_pwd PS_MYSQL_HOST=localhost PS_MYSQL_DB=ps_dev_db PS_TYPE_STORAGE=db ./app.py 

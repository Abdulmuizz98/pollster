#!/usr/bin/bash
# Run all unitests in tests while using DbStorage engine, with environment variables.

PS_ENV=test PS_MYSQL_USER=ps_test PS_MYSQL_PWD=ps_test_pwd PS_MYSQL_HOST=localhost PS_MYSQL_DB=ps_test_db PS_TYPE_STORAGE=db python3 -m unittest discover tests 2>&1 /dev/null | tail -n 1

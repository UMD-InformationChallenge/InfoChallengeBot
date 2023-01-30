#!/bin/sh

set -e

# activate our virtual environment here
. /opt/pysetup/.venv/bin/activate

# You can put other setup logic here
echo Sleeping 20 seconds for DB to start
sleep 20

# Evaluating passed command:
exec "$@"

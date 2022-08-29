#!/bin/bash
#
# Run our app interactively, in development mode.
#

# Errors are fatal
set -e

# Change to the parent directory of this script
pushd $(dirname $0)/.. > /dev/null

#
# Run the main app
#
uvicorn --host 0.0.0.0 main:app


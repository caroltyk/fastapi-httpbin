#!/bin/bash
#
# Push our Docker image our Docker Hub.
#

# Errors are fatal
set -e

# Change to the parent directory of this script
pushd $(dirname $0)/.. > /dev/null

if test "$1"
then
    echo "# Publish image with tag: $1"
    docker tag fastapi-httpbin caroltyk/fastapi-httpbin:$1
    docker push caroltyk/fastapi-httpbin:$1
else
    echo "# Specify an image tag"
fi
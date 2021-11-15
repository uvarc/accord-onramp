#!/bin/bash

set -e

echo -n "The CIDR range to add: "
read -r CIDR

echo -n "Abbreviated campus name: "
read -r CAMPUS

UNIQID=`/usr/bin/openssl rand -base64 6`

# sync the repo with S3
aws --profile uvarc dynamodb put-item --table-name accord-blocks \
  --item "{\"block_id\":{\"S\":\"$UNIQID\"},\"block_value\":{\"S\":\"$CIDR\"},\"block_campus\":{\"S\":\"$CAMPUS\"}}"

echo "Adding $CIDR for ACCORD member: $CAMPUS";

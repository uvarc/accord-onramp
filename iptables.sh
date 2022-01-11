#!/bin/bash

echo ""
echo " Here are current CIDR values: "
echo ""
aws --profile uvarc dynamodb scan --table-name accord-blocks | jq -r .'Items[] | .block_value.S + " - " + .block_campus.S'
echo ""

echo ""
echo "Saving to blocks.txt"
aws --profile uvarc dynamodb scan --table-name accord-blocks | jq -r .'Items'[].'block_value'.'S' > blocks.txt
echo ""


aws --profile uvarc dynamodb scan --table-name accord-blocks | jq -r .'Items[] | "Require ip " + .block_value'.'S' > apache2-blocks.txt

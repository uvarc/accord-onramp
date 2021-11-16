#!/bin/bash

aws --profile uvarc dynamodb scan --table-name accord-blocks | jq -r .'Items'[].'block_value'.'S' > blocks.txt


#!/bin/bash

# sync the repo with S3
aws --profile defaultz s3 sync . s3://accord-frontdoor/ --acl public-read --delete 

# invalidate CF cache
aws --profile defaultz cloudfront create-invalidation --distribution-id E33CY0JIMDZFTI --paths "/*"
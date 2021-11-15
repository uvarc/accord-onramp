#!/bin/bash

set -e

# sync the repo with S3
aws --profile uvarc s3 sync . s3://accord-frontdoor/ --acl public-read --delete --exclude ".git/*" --exclude ".github/*";

# invalidate CF cache
aws --profile uvarc cloudfront create-invalidation --distribution-id E33CY0JIMDZFTI --paths "/*";

exit 0;
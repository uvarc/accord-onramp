# accord-onramp

This site consists of a static HTML/Javascript front-end backed by APIs to provide a front door for users of the ACCORD platform. The primary purpose of the site is to help users troubleshoot and/or verify their connectivity to ACCORD.

The two most essential checks for connecting are:

1. **Network connectivity** - trying to access ACCORD from the proper campus or campus VPN address ranges.
2. **OPSWAT MetaAccess** - that security posture software is installed and running.

## HTML

The HTML site consists of one page (plus CSS, images, and JS) published to a website-enabled S3 bucket and served to the public via a CloudFront distribution.

## API

The backing API is provided by the AWS API Gateway and an accompanying Lambda function. These are written and published using the Chalice framework and live
within the `api/` directory. The API takes the client IP address and verifies whether that address is part of a known ACCORD CIDR range.

Endpoint:
```
https://06iteam4j8.execute-api.us-east-1.amazonaws.com/api/validate/128.143.20.25
```
Results:
```
{
  "message": "128.143.20.25 is a valid IP address",
  "status": "true",
  "institution": "UVA HSVPN",
  "ip": "128.143.20.25"
}
```

## Data

Data is stored in DynamoDB, within a single table. Each record consists of a key, the IP range (in CIDR notation), and a descriptive name or institutional owner of the address block.

## Status

An additional endpoint of the API serves status messages for display on the page:
```
https://47tpa1dam4.execute-api.us-east-1.amazonaws.com/api/accord/messages
```
Results:
```
[
  {
    "message": "message",
    "body": "2021-12-15 11:18:42 The ACCORD platform is operating normally."
  }
]
```

## MetaAccess

The final logical component of the page is a JS function to determine whether the MetaAccess agent is running on the localhost. For this particular deployment that is port `11369` as configured by UVA. The public DNS record `eapi.opswatgears.com` resolves to `127.0.0.1`.
```
https://eapi.opswatgears.com:11369/opswat/devinfo?callback=js0
```
This site does not need the return payload from such an internal API request, it only needs to determine whether that service is available or not as a simple check for whether MetaAccess is running or not.

## Logic

The two checks, one verifying the user IP address is from an ACCORD partner and another verifying MetaAccess, must both be met for the user to be given the link to the ACCORD console. This is not meant as a security control whatsoever, only as a helpful check for user access.

## Builds

This repository makes use of a GitHub Action that builds and deploys with each push:
```
#!/bin/sh

set -e

git clone --depth=50 --branch=main https://github.com/uvarc/accord-onramp.git
cd accord-onramp

echo "minify the JS"
cp js/onramp.min.js js/onramp.js
/usr/bin/uglifyjs js/onramp.js > js/onramp.min.js

echo "clone project and sync"

# sync the repo with S3
aws s3 sync . s3://accord-frontdoor/ --acl public-read --delete --exclude ".git/*" --exclude ".github/*"

# invalidate CF cache
aws cloudfront create-invalidation --distribution-id E33CY0JIMDZFTI --paths "/*"
```

1. Pulls a special deployment container and runs it using AWS credentials (stored as secrets)
2. The container's build script pulls the repository.
3. The build script then minifies the JS.
4. The build script then syncs the HTML/image/CSS/JS content with an S3 bucket.
5. The build script then invalidates all `*` objects in the CloudFront distribution's cache.
#!/bin/bash
set -x

echo "${UPLOAD_KEY}" > key
chmod 0600 key

rm -rf dist/

sed -i "s/version = \"\(.*\)\"/version = \"\1-$(date +%Y%m%d%H%M)\"/" pyproject.toml
/venv/bin/poetry build

# TODO: host key checking...
ssh -o StrictHostKeyChecking=no -i key pypi@pypi.zerfeciz.com mkdir -p packages/weevils-python/
scp -o StrictHostKeyChecking=no -i key dist/* pypi@pypi.zerfeciz.com:packages/weevils-python/

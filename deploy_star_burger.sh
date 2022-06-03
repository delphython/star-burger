#!/bin/bash
set -e

cd /opt/star-burger

echo "Update the repository code"
git pull

echo "Install libraries"
./venv/bin/pip3 install -r requirements.txt

npm ci --dev

echo "Build the frontend"
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

echo "Collect Django static files"
./venv/bin/python3 manage.py collectstatic --noinput

echo "Migrate the database"
./venv/bin/python3 manage.py migrate --noinput

echo "Restart necessary services"
systemctl restart star-burger.service
systemctl reload nginx.service

echo "Let rollbar know about deploy"
http POST https://api.rollbar.com/api/1/deploy \
X-Rollbar-Access-Token:$POST_SERVER_ACCESS_TOKEN \
environment=production \
revision=$(git rev-parse --short HEAD) \
rollbar_name=FirstProject \
local_username=delphython

echo "Successful completion of the deployment"

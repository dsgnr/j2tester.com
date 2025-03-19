#!/usr/bin/env sh
set -e

# Export API_URL so envsubst can use it
: ${API_URL:="http://api:8000"}
export API_URL

# Updates the `API_URL` variable in the Nginx config. Defaults to http://api:8000 if not set.
envsubst "\$API_URL" < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

exec nginx -g "daemon off;"

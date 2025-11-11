#!/bin/sh
# script to perform the substitution of BACKEND_URL_PLACEHOLDER_TOKEN in all js compiled files
# using the environment variable taken BACKEND_URL


if [ -z "$BACKEND_URL" ]; then
  echo "WARN: BACKEND_URL not defined. Using default value (http://localhost:5000/router)."
  BACKEND_URL="http://localhost:5000/router"
fi

JS_FILES=$(find /usr/share/nginx/html -type f -name "*.js")

echo "INFO: replacing: BACKEND_URL_PLACEHOLDER_TOKEN -> $BACKEND_URL"

for file in $JS_FILES; do
  sed "s|BACKEND_URL_PLACEHOLDER_TOKEN|$BACKEND_URL|g" "$file" > "$file.tmp" && mv "$file.tmp" "$file"
done

echo "INFO: replacement done"

exec "$@"
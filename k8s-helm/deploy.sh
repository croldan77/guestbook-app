#!/bin/bash
set -e

echo "🔓 Decrypting secrets..."
sops --decrypt secrets.enc.yaml > .secrets-temp.yaml

echo "📦 Running Helm upgrade..."
helm upgrade guestbook-release . \
    -n guestbook-app \
    --install \
    --create-namespace \
    -f values.yaml \
    -f .secrets-temp.yaml

echo "🧹 Cleaning..."
rm -f .secrets-temp.yaml

echo "🎉 Ready!"
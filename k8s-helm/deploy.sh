#!/bin/bash
set -e

echo "🔓 Desencriptando secrets..."
sops --decrypt secrets.enc.yaml > .secrets-temp.yaml

echo "📦 Ejecutando Helm upgrade..."
helm upgrade guestbook-release . \
    -n guestbook-app \
    --install \
    --create-namespace \
    -f values.yaml \
    -f .secrets-temp.yaml

echo "🧹 Limpiando..."
rm -f .secrets-temp.yaml

echo "🎉 Listo!"
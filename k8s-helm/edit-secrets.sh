#!/bin/bash
# edit-secrets.sh - Edit encrypted secrets
set -e

echo "📝 Editing encrypted secrets..."
sops secrets.enc.yaml

echo "✅ Editing completed. The file was automatically saved in encrypted format.."
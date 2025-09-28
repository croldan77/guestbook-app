#!/bin/bash
# edit-secrets.sh - Editar secrets encriptados
set -e

echo "📝 Editando secrets encriptados..."
sops secrets.enc.yaml

echo "✅ Editado completado. El archivo se guardó encriptado automáticamente."
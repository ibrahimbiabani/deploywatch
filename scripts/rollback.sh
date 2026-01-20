#!/bin/bash
set -euo pipefail

SERVICE="$1"
VERSION="$2"

echo "rolling back ${SERVICE} to ${VERSION}"
docker service update --image "registry.internal/${SERVICE}:${VERSION}" "${SERVICE}"

#!/usr/bin/env bash
#
# Usage:
#   ./build_docker_image.sh

set -euox pipefail

SRC_DIR="$(realpath "${0}" | xargs dirname)/src"
AWS_ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
AWS_REGION="$(aws configure get region)"
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
TAG_NAME="sha-$(git rev-parse --short HEAD)"
BUILD_TARGET='app'
PLATFORMS='linux/arm64'

find src -type f -name Dockerfile -print0 \
  | xargs -0 dirname \
  | xargs -L1 basename \
  | xargs -I{} -t docker buildx build \
    --tag "${ECR_REGISTRY}/{}:${TAG_NAME}" \
    --target "${BUILD_TARGET}" \
    --platform "${PLATFORMS}" \
    --provenance false \
    "${SRC_DIR}/{}"
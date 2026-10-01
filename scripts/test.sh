#!/bin/bash

# Run end-to-end tests for specified Blender version.
# Is supposed to be executed from repository root.

BLENDER_DIR="/home/mcr/blender/$1"

if [ ! -f "$BLENDER_DIR/blender" ]; then
    echo "Unable to find blender executable at \"$BLENDER_DIR\""
    return 1
fi

echo "Running end-to-end tests at $BLENDER_DIR"

pytest -s -v --blender "$BLENDER_DIR/blender" --repo user_default --background-only $MCR_ROOT_DIR/tests

#!/bin/bash

# Builds extension using Blender extension command.
# Is supposed to be executed from repository root.

if ! [ -d $MCR_DISTRIBUTION_DIR ]; then
    mkdir -p $MCR_DISTRIBUTION_DIR
fi

pip download -r "$MCR_ROOT_DIR/requirements.txt" --dest "$MCR_ROOT_DIR/src/multiple_camera_render/wheels"

blender --command extension build \
    --source-dir="$MCR_ROOT_DIR/src/multiple_camera_render" \
    --output-dir="$MCR_DISTRIBUTION_DIR"

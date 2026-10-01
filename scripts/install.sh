#!/bin/bash

# Install build extension to all existing Blender installations.
# Is supposed to be executed from repository root. 

EXTENSION_ZIP=$(find "$MCR_DISTRIBUTION_DIR" -type f -name "multiple_camera_render-*.zip" | head -n 1)

if [[ ! -f "$EXTENSION_ZIP" ]]; then
    echo "Extension should be build first. Could not find suitable file at ${MCR_DISTRIBUTION_DIR}"
    return 1
fi

for directory in /home/mcr/blender/*/; do
    echo "Installing using \"$directory\""
    $directory/blender --command extension install-file --repo user_default --enable "$EXTENSION_ZIP" 
done

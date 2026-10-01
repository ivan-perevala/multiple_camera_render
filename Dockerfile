# syntax=docker/dockerfile:1

# SPDX-FileCopyrightText: 2026 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

FROM ubuntu:26.04

LABEL version=1.0.0
LABEL description="Multiple Camera Render extension testing environment."

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    xz-utils \
    python3 \
    python3-venv \
    python3-pip \
    libx11-6 \
    libxrender1 \
    libxxf86vm1 \
    libxfixes3 \
    libxi6 \
    libxkbcommon0 \
    libsm6 \
    libice6 \
    libxext6 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --gid users --comment "Test user for non-root access" mcr
USER mcr
WORKDIR /home/mcr

RUN python3 -m venv .venv \
    && . .venv/bin/activate \
    && pip install pytest

WORKDIR /home/mcr/blender/blender-4.2
ADD --chown=mcr:users \
    https://download.blender.org/release/Blender4.2/blender-4.2.23-linux-x64.tar.xz \
    blender.tar.xz
RUN tar --extract --strip-components=1 --file blender.tar.xz \
    && rm -f blender.tar.xz \
    && ./4.2/python/bin/python3.11 -m pip install pytest

WORKDIR /home/mcr/blender/blender-4.5
ADD --chown=mcr:users \
    https://download.blender.org/release/Blender4.5/blender-4.5.14-linux-x64.tar.xz \
    blender.tar.xz
RUN tar --extract --strip-components=1 --file blender.tar.xz \
    && rm -f blender.tar.xz \
    && ./4.5/python/bin/python3.11 -m pip install pytest

WORKDIR /home/mcr/blender/blender-5.2
ADD --chown=mcr:users \
    https://download.blender.org/release/Blender5.2/blender-5.2.2-linux-x64.tar.xz \
    blender.tar.xz
RUN tar --extract --strip-components=1 --file blender.tar.xz \
    && rm -f blender.tar.xz \
    && ./5.2/python/bin/python3.13 -m pip install pytest

ENV PATH="$PATH:/home/mcr/blender/blender-5.2"
RUN echo 'source /home/mcr/.venv/bin/activate' >> /home/mcr/.bashrc

WORKDIR /home/mcr/multiple_camera_render

ENV MCR_DISTRIBUTION_DIR=/home/mcr/dist
ENV MCR_ROOT_DIR=/home/mcr/multiple_camera_render
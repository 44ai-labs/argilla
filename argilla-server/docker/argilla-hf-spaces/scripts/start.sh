#!/usr/bin/env bash

set -e

DEFAULT_USERNAME="admin"
DEFAULT_PASSWORD=$(pwgen -s 16 1)
export USERNAME="${USERNAME:-$DEFAULT_USERNAME}"
export PASSWORD="${PASSWORD:-$DEFAULT_PASSWORD}"

honcho start

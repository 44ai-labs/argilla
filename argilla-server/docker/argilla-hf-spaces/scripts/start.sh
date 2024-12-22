#!/usr/bin/env bash

set -e

DEFAULT_USERNAME="admin"
DEFAULT_PASSWORD="admin"
DEFAULT_API_KEY="admin"
export USERNAME="${USERNAME:-$DEFAULT_USERNAME}"
export PASSWORD="${PASSWORD:-$DEFAULT_PASSWORD}"
export API_KEY="${API_KEY:-$DEFAULT_API_KEY}"

honcho start

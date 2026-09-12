#!/bin/bash

set -e

exec odoo \
  --http-port="${PORT:-10000}" \
  --db_host="${HOST}" \
  --db_port="5432" \
  --db_user="${USER}" \
  --db_password="${PASSWORD}"
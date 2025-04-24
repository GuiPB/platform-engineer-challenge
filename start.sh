#!/bin/bash

# Make the directory if it doesn't exist
mkdir -p .env

# Generate LDAP environment variables
./scripts/generate_ldap_env.py > .env/ldap.env

# Start services with the generated environment
docker compose --env-file .env/ldap.env up -d
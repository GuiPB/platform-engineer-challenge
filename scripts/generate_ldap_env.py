#!/usr/bin/env python3

import json
from pathlib import Path

def generate_ldap_env():
    # Read teams configuration
    with open(Path(__file__).parent.parent / 'teams.json', 'r') as f:
        config = json.load(f)

    # Extract users and passwords
    users = []
    passwords = []
    
    for team_data in config['teams'].values():
        for username, user_data in team_data['users'].items():
            users.append(username)
            passwords.append(user_data['password'])

    # Return formatted environment variables
    return {
        'LDAP_USERS': ','.join(users),
        'LDAP_PASSWORDS': ','.join(passwords)
    }

if __name__ == '__main__':
    env_vars = generate_ldap_env()
    # Print in a format that can be used with docker-compose
    for key, value in env_vars.items():
        print(f"{key}={value}")
# Platform Engineer Challenge Documentation

## Overview
This project sets up a HashiCorp Vault instance with OpenLDAP integration for managing team-based access to secrets.

## Prerequisites
- Docker and Docker Compose
- Python 3.x
- Visual Studio Code (recommended)

## Project Structure
```
platform-engineer-challenge/
├── docker-compose.yml    # Docker services configuration
├── teams.json           # User and team management
├── src/                 # Terraform configurations
├── scripts/            # Utility scripts
└── .env/               # Generated environment files
```

## User Management
Users and teams are managed through the teams.json file. Here's the structure:

````json
{
  "teams": {
    "team-a": {
      "users": {
        "interna": {
          "password": "internapassword",
          "role": "intern"
        },
        "staffa": {
          "password": "staffapassword",
          "role": "admin"
        }
      }
    }
  }
}
````

### Adding Users
1. Open teams.json
2. Add a new user under the appropriate team:
```json
"newuser": {
  "password": "userpassword",
  "role": "developer"
}
```

### Available Roles
- `intern`: Read-only access to production secrets
- `developer`: Full access to dev, read-only to preprod
- `admin`: Full access to all environments

## Running the Project

1. Clone the repository:
```bash
git clone <repository-url>
cd platform-engineer-challenge
```

2. Make the startup script executable:
```bash
chmod +x start.sh
```

3. Start the services:
```bash
./start.sh
```

This will:
- Generate LDAP environment variables from teams.json
- Start OpenLDAP and Vault containers
- Configure user access

4. Initialize and apply Terraform configuration:
```bash
cd src
terraform init
terraform plan    # Review the changes
terraform apply   # Apply the configuration and type 'yes' when prompted
```

This will:
- Configure Vault's LDAP authentication
- Create team-specific policies
- Map users to their respective roles and permissions
- Set up the secret engine paths

## Verifying the Setup

1. Check OpenLDAP users:
```bash
ldapsearch -x -H ldap://localhost:1389 \
  -b "dc=example,dc=org" \
  -D "cn=admin,dc=example,dc=org" \
  -w adminpassword
```

2. Test Vault login with LDAP:
```bash
export VAULT_ADDR='http://localhost:8200'
vault login -method=ldap username=interna
```

## Secret Path Structure
```
secret/
├── teams/
│   ├── team-a/
│   │   ├── dev/
│   │   ├── preprod/
│   │   └── prod/
│   └── team-b/
└── applications/
    ├── app-1/
    └── app-2/
```

## Common Tasks

### Restart Services
```bash
docker compose down
./start.sh
```

### View Logs
```bash
docker compose logs -f
```

### Reset Environment
```bash
docker compose down -v
./start.sh
```

## Troubleshooting

### LDAP Connection Issues
```bash
# Test LDAP connectivity
ldapwhoami -x -H ldap://localhost:1389 \
  -D "cn=admin,dc=example,dc=org" \
  -w adminpassword
```

### Vault Status
```bash
export VAULT_ADDR='http://localhost:8200'
vault status
```

## Security Notes
- Default passwords in teams.json should be changed in production
- Consider using a secrets manager for password storage
- Production deployments should enable TLS for both Vault and LDAP

For more information, consult the individual documentation for [HashiCorp Vault](https://www.vaultproject.io/docs) and [OpenLDAP](https://www.openldap.org/doc/).
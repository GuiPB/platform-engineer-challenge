# Create team-specific policies for each role
resource "vault_policy" "intern" {
  for_each = local.teams_config.teams
  
  name = "intern-${each.key}"

  policy = <<EOT
# Read-only access to prod environment for specific team
path "secret/data/teams/${each.key}/prod/*" {
  capabilities = ["read", "list"]
}
path "secret/metadata/teams/${each.key}/prod/*" {
  capabilities = ["list"]
}

path "secret/data/applications/${each.key}/prod/*" {
  capabilities = ["read", "list"]
}
path "secret/metadata/applications/${each.key}/prod/*" {
  capabilities = ["list"]
}
EOT
}

resource "vault_policy" "developer" {
  for_each = local.teams_config.teams
  
  name = "developer-${each.key}"

  policy = <<EOT
# Dev environment - full access for specific team
path "secret/data/teams/${each.key}/dev/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
path "secret/metadata/teams/${each.key}/dev/*" {
  capabilities = ["list"]
}

path "secret/data/applications/${each.key}/dev/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
path "secret/metadata/applications/${each.key}/dev/*" {
  capabilities = ["list"]
}

# Preprod environment - read-only access for specific team
path "secret/data/teams/${each.key}/preprod/*" {
  capabilities = ["read", "list"]
}
path "secret/metadata/teams/${each.key}/preprod/*" {
  capabilities = ["list"]
}

path "secret/data/applications/${each.key}/preprod/*" {
  capabilities = ["read", "list"]
}
path "secret/metadata/applications/${each.key}/preprod/*" {
  capabilities = ["list"]
}
EOT
}

resource "vault_policy" "admin" {
  for_each = local.teams_config.teams
  
  name = "admin-${each.key}"

  policy = <<EOT
# Full access to all environments for specific team
path "secret/data/teams/${each.key}/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
path "secret/metadata/teams/${each.key}/*" {
  capabilities = ["list"]
}

path "secret/data/applications/${each.key}/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
path "secret/metadata/applications/${each.key}/*" {
  capabilities = ["list"]
}
EOT
}
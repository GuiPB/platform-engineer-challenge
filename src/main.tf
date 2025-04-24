locals {
  teams_config = jsondecode(file("../teams.json"))

  # Flatten users from all teams into a single map
  users = merge([
    for team_name, team in local.teams_config.teams : {
      for user_name, user in team.users : "${user_name}" => {
        role     = user.role
        team     = team_name
      }
    }
  ]...)

  # Update roles_to_policy to use team-specific policies
  roles_to_policy = {
    for team_name, team in local.teams_config.teams : team_name => {
      "intern"    = vault_policy.intern[team_name].name
      "developer" = vault_policy.developer[team_name].name
      "admin"     = vault_policy.admin[team_name].name
    }
  }
}

# Configure LDAP auth method
resource "vault_ldap_auth_backend" "ldap" {
  path         = "ldap"
  url          = "ldap://openldap:1389"
  userdn       = "dc=example,dc=org"
  groupdn      = "dc=example,dc=org"
  binddn       = "cn=admin,dc=example,dc=org"
  bindpass     = "adminpassword"
  userattr     = "uid"
  insecure_tls = true
}

# Update LDAP user resource to use team-specific policies
resource "vault_ldap_auth_backend_user" "users" {
  for_each = local.users

  backend  = vault_ldap_auth_backend.ldap.path
  username = each.key
  policies = [local.roles_to_policy[each.value.team][each.value.role]]
}
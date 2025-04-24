#!/usr/bin/env python3

import subprocess
import json

def run_command(command):
    """Run a shell command and return output and error status"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {
            'success': result.returncode == 0,
            'output': result.stdout.strip(),
            'error': result.stderr.strip()
        }
    except Exception as e:
        return {
            'success': False,
            'output': '',
            'error': str(e)
        }

def vault_login(username, password):
    """Login to Vault using LDAP"""
    result = run_command(f'vault login -method=ldap username={username} password={password}')
    if not result['success']:
        raise Exception(f"Failed to login as {username}: {result['error']}")
    return result['success']

def test_vault_access(username, path, operation):
    """Test access to a specific path with an operation"""
    if operation == "read":
        cmd = f'vault kv get secret/{path}'
    elif operation == "write":
        cmd = f'vault kv put secret/{path} test=value'
    
    result = run_command(cmd)
    return {
        'success': result['success'],
        'output': result['output'],
        'error': result['error']
    }

def main():
    # Set Vault address
    vault_addr_result = run_command('export VAULT_ADDR=http://localhost:8200')
    if not vault_addr_result['success']:
        print("Failed to set VAULT_ADDR")
        return

    # Test cases for different roles
    test_cases = [
        # Intern tests
        {
            "user": "interna",
            "tests": [
                {"path": "teams/team-a/prod/test", "op": "read", "expected": "success"},
                {"path": "teams/team-a/dev/test", "op": "write", "expected": "error"},
                {"path": "applications/app-1/prod/test", "op": "read", "expected": "error"}
            ]
        },
        # Developer tests
        {
            "user": "juniora",
            "tests": [
                {"path": "teams/team-a/dev/test", "op": "write", "expected": "success"},
                {"path": "teams/team-a/preprod/test", "op": "read", "expected": "success"},
                {"path": "teams/team-a/prod/test", "op": "write", "expected": "error"}
            ]
        },
        # Admin tests
        {
            "user": "staffa",
            "tests": [
                {"path": "teams/team-a/dev/test", "op": "write", "expected": "success"},
                {"path": "teams/team-a/preprod/test", "op": "write", "expected": "success"},
                {"path": "teams/team-a/prod/test", "op": "write", "expected": "success"}
            ]
        },
        {
            "user": "juniorb",
            "tests": [
                {"path": "teams/team-a/dev/test", "op": "write", "expected": "error"},
                {"path": "teams/team-a/preprod/test", "op": "write", "expected": "error"},
                {"path": "teams/team-a/prod/test", "op": "write", "expected": "error"},
                {"path": "teams/team-b/dev/test", "op": "write", "expected": "success"},
                {"path": "teams/team-b/preprod/test", "op": "write", "expected": "sucess"},
                {"path": "teams/team-b/prod/test", "op": "read", "expected": "error"},
            ]
        }
    ]

    # Run tests
    for case in test_cases:
        print(f"\nTesting user: {case['user']}")
        print("=" * 50)
        
        try:
            # Login as user
            if not vault_login(case['user'], f"{case['user']}password"):
                print(f"❌ Failed to login as {case['user']}")
                continue
            
            # Run test cases
            for test in case['tests']:
                result = test_vault_access(case['user'], test['path'], test['op'])
                
                # Determine if the test passed based on expected outcome
                if test['expected'] == "success":
                    success = result['success']
                else:  # expected == "error"
                    success = not result['success'] and "permission denied" in result['error'].lower()
                
                print(f"Path: {test['path']}")
                print(f"Operation: {test['op']}")
                print(f"Expected: {test['expected']}")
                print(f"Result: {'✅ Pass' if success else '❌ Fail'}")
                if not success:
                    print(f"Error: {result['error']}")
                print("-" * 30)
                
        except Exception as e:
            print(f"❌ Error during test execution: {str(e)}")
            continue

if __name__ == "__main__":
    main()
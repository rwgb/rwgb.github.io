---
title: "Building Powerful Infrastructure Automation with Proxmox-CLI"
date: 2025-11-08
description: "Automation and tooling for proxmox VE environments."
tags: ['python', 'github-actions', 'tutorial', 'python-development']
categories: ["Uncategorized"]
draft: false
---

## Introduction

If you're managing a Proxmox Virtual Environment and find yourself constantly clicking through the web interface to perform routine tasks, it's time to level up. **proxmox-cli** is a Python-based command-line tool that brings your Proxmox infrastructure under scriptable, automatable control. Whether you're orchestrating VM deployments, managing users at scale, or building infrastructure-as-code pipelines, this tool transforms tedious point-and-click operations into elegant one-liners.

### What Is proxmox-cli?

proxmox-cli is an open-source wrapper around the Proxmox API that lets you manage virtually every aspect of your Proxmox Virtual Environment from the terminal. Built in Python and designed with automation in mind, it supports everything from virtual machine lifecycle management to granular permission control—all with multiple output formats for seamless integration into your scripts and pipelines.

#### Core Capabilities

The tool provides comprehensive management across several domains:

**Virtual Machines & Containers**: Create, start, stop, and monitor VMs and LXC containers with simple commands. **User & Access Management**: Create users, organize them into groups, define custom roles, and implement fine-grained ACLs. **Infrastructure Monitoring**: Check node status, storage configuration, and resource utilization. **API Token Management**: Generate and manage authentication tokens for programmatic access. **Flexible Output**: JSON (default), table, YAML, and plain text formats let you pipe data wherever you need it.

### Why Use a CLI Tool for Proxmox?

#### The Problem It Solves

The Proxmox web interface is excellent for interactive administration, but it becomes a bottleneck when you need to perform repetitive tasks or coordinate changes across your infrastructure. Imagine spinning up 10 new development VMs with identical configurations, provisioning users for a new department, or running compliance audits across all nodes—doing these through the GUI is time-consuming and error-prone.

#### Real-World Use Cases

**Scripting & Automation**: Build bash scripts that provision entire application stacks on demand. A CI/CD pipeline could automatically spin up test environments, run workloads, and tear them down—no manual intervention required.

**Infrastructure as Code**: Define your entire infrastructure in version-controlled scripts. Changes go through code review before hitting production. Rollbacks become trivial—just revert the commit.

**Batch Operations**: Need to update permissions for 50 users? Generate the commands programmatically and execute them all at once.

**Monitoring & Alerting Integration**: Extract metrics in JSON and pipe them into your monitoring stack. Create custom alerts based on Proxmox state.

**Multi-Cluster Management**: Manage multiple Proxmox installations from a single control point. Use configuration files to target different clusters without changing commands.

**Disaster Recovery**: Automate backup verification, replication checks, or failover procedures as part of your disaster recovery testing.

**Policy Enforcement**: Run periodic scripts to audit user permissions, ensure storage quotas are configured, or validate role assignments across your infrastructure.

### Installation & Setup

#### Getting Started

The simplest approach is installing from PyPI:

```bash
pip install proxmox-cli

```

For development work or contribution to the project:

```bash
git clone https://github.com/rwgb/proxmox.cli.git
cd proxmox.cli
pip install -e ".[dev]"

```

The `[dev]` extra installs testing frameworks and linting tools, giving you a complete development environment.

#### Configuration

proxmox-cli expects configuration at `~/.config/proxmox-cli/config.yaml`. Here's a typical setup:

```yaml
proxmox:
  host: proxmox.example.com
  user: root@pam
  password: your-password
  verify_ssl: false

output:
  format: json

```

**Better yet: use API tokens instead of passwords.** This is more secure and better for automation:

```yaml
proxmox:
  host: proxmox.example.com
  user: yourusername@pve
  token_name: mytoken
  token_value: your-token-value
  verify_ssl: false

output:
  format: json

```

The `verify_ssl: false` option is useful in development with self-signed certs, but should be reconsidered in production.

#### Authentication Best Practices

Never hardcode passwords in scripts. Instead:

1. Generate an API token in Proxmox and store it securely (e.g., in environment variables, secret management systems, or encrypted files with restricted permissions)

1. Reference the token in your configuration

1. Consider using tools like HashiCorp Vault for enterprise environments

1. For CI/CD pipelines, use your platform's secret storage (GitHub Secrets, GitLab CI/CD variables, etc.)

### Core Commands & Examples

#### Virtual Machine Management

Listing all VMs is straightforward:

```bash
proxmox-cli vm list

```

This returns JSON by default, perfect for parsing. Want a human-readable table?

```bash
proxmox-cli --output table vm list

```

To list VMs on a specific node:

```bash
proxmox-cli vm list --node pve1

```

Controlling VMs is equally simple:

```bash
proxmox-cli vm start 100 --node pve1
proxmox-cli vm stop 100 --node pve1
proxmox-cli vm status 100 --node pve1

```

#### Container Management

LXC containers work similarly:

```bash
proxmox-cli container list
proxmox-cli container start 108 --node pve1
proxmox-cli container stop 108 --node pve1

```

#### User & Permission Management

Creating a new user with email and group assignment:

```bash
proxmox-cli user create developer@pve \
  --password "SecurePass123" \
  --email "dev@example.com" \
  --groups "developers"

```

Updating user information:

```bash
proxmox-cli user update developer@pve \
  --email "newemail@example.com"

```

Listing all users to verify:

```bash
proxmox-cli --output table user list

```

#### Role-Based Access Control

Define a custom role with specific privileges:

```bash
proxmox-cli role create CustomRole \
  --privs "VM.Allocate,VM.Audit,VM.PowerMgmt"

```

Grant permissions to users or groups:

```bash
proxmox-cli acl add \
  --path "/" \
  --roles "PVEAdmin" \
  --users "admin@pve"

```

#### API Token Management

Generate a token for a user (useful for automation):

```bash
proxmox-cli token create user@pve mytoken \
  --comment "Automation token" \
  --no-privsep

```

List tokens:

```bash
proxmox-cli token list user@pve

```

### Practical Automation Examples

#### Example 1: Batch VM Startup Script

Start all VMs matching a naming pattern on a specific node:

```bash
#!/bin/bash

NODE="pve1"

# Get all VMs on the node, parse JSON, extract VMID
proxmox-cli vm list --node $NODE | jq -r '.[] | select(.name | startswith("prod-")) | .vmid' | while read VMID; do
  echo "Starting VM $VMID..."
  proxmox-cli vm start $VMID --node $NODE
done

echo "All production VMs started."

```

#### Example 2: User Onboarding Workflow

Create a new user with proper group assignment and permissions:

```bash
#!/bin/bash

NEW_USER="alice@pve"
NEW_EMAIL="alice@company.com"
NEW_GROUP="engineering"
TEMP_PASSWORD=$(openssl rand -base64 12)

# Create user
proxmox-cli user create "$NEW_USER" \
  --password "$TEMP_PASSWORD" \
  --email "$NEW_EMAIL" \
  --groups "$NEW_GROUP"

# Grant permissions
proxmox-cli acl add \
  --path "/" \
  --roles "CustomDeveloper" \
  --users "$NEW_USER"

# Output for IT to share with user
echo "User created: $NEW_USER"
echo "Temporary password: $TEMP_PASSWORD"
echo "Please change password on first login"

```

#### Example 3: Infrastructure Status Report

Generate a compliance report of all nodes and their resource usage:

```bash
#!/bin/bash

echo "=== Proxmox Infrastructure Status ==="
echo ""
echo "Node Resource Utilization:"
proxmox-cli --output table node list
echo ""

echo "User Accounts:"
proxmox-cli --output table user list
echo ""

echo "Custom Roles:"
proxmox-cli --output table role list

# Output to JSON for programmatic processing
proxmox-cli node list > node_status.json

```

#### Example 4: Container Deployment Pipeline

Integrate into a deployment script for automated testing environments:

```bash
#!/bin/bash

CONTAINER_ID="200"
NODE="pve2"
IMAGE="ubuntu-22.04"

# Stop if running
proxmox-cli container stop $CONTAINER_ID --node $NODE 2>/dev/null

# Verify stopped
proxmox-cli container status $CONTAINER_ID --node $NODE

# Ready for re-provisioning
echo "Container $CONTAINER_ID is ready for deployment"

```

### Output Formats for Different Use Cases

proxmox-cli's multiple output formats make it flexible for any workflow:

**JSON** is the default—parse it with `jq`, `python -m json.tool`, or any JSON library. Perfect for scripts that need structured data.

**Table** format is human-readable, ideal for ad-hoc commands and documentation.

**YAML** is great when you're building configuration files or integrating with Ansible.

**Plain text** minimizes noise for simple lookups.

Switch formats with the `--output` flag:

```bash
proxmox-cli --output json vm list
proxmox-cli --output table vm list
proxmox-cli --output yaml user list
proxmox-cli --output plain node list

```

### Advanced Workflows

#### Combining with Other Tools

proxmox-cli shines when combined with other utilities:

**With jq for powerful JSON filtering**:

```bash
proxmox-cli vm list | jq '.[] | select(.status=="stopped")'

```

**With xargs for parallel operations**:

```bash
proxmox-cli vm list | jq -r '.[] | .vmid' | xargs -I {} proxmox-cli vm start {} --node pve1

```

**With cron for scheduled automation**:

```bash
# Daily compliance check at 2 AM
0 2 * * * /usr/local/bin/proxmox-compliance-check.sh

```

**With Ansible for orchestration**:

```yaml
- name: Get VM status
  shell: proxmox-cli vm list --output json
  register: vm_list

- name: Parse results
  set_fact:
    vms: "{{ vm_list.stdout | from_json }}"

```

#### Building Custom Tools

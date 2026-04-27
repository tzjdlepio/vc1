<!--
Sync Impact Report:
- Version change: None -> 1.0.0
- List of modified principles: New Constitution
- Added sections: Core Principles, Technical Requirements, Governance
- Removed sections: None
-->

# Asgard Python Package Constitution

## Core Principles

### I. REST-Centric Mapping
Asgard must maintain a 1-to-1 mapping logic between Python methods and Azure DevOps REST API endpoints. Every method should clearly document which API it calls.
**Reason**: Ensures predictability for developers familiar with Azure DevOps documentation and simplifies troubleshooting.

### II. Resource-Oriented Architecture
Logic must be strictly partitioned into modules based on Azure DevOps resources: `projects.py`, `repos.py`, `members.py`, `pipelines.py`, and `releases.py`. Each module contains a Manager class (e.g., `ProjectManager`).
**Reason**: Keeps the codebase organized and allows for focused maintenance as the API grows.

### III. Fail-Fast & Explicit Exceptions
All non-2xx/3xx HTTP responses must raise an `AsgardAPIException`. The exception must contain the status code, reason, and the raw response body from the API.
**Reason**: Prevents silent failures and provides immediate feedback for debugging API-related issues.

### IV. Environment-Driven & Secure
No sensitive data (PAT, Organization URL) shall be hard-coded. All configuration must be loaded via `asgard.config.Config` from environment variables.
**Reason**: Prevents credential leakage and enables easy configuration across different environments.

### V. Atomic & Idempotent Design
Operations like creating branches, setting policies, or managing memberships should be atomic. Where possible, methods should be designed to handle re-execution gracefully.
**Reason**: Ensures stability in automated workflows.

## Technical Requirements

- **Project**: Support CRUD and existence check.
- **Repository**: Support file CRUD, 5MB size limit setting, branch creation, and branch policies (Work Item, Comment Resolution, Base Merge).
- **Membership**: Support ProjectManager/Member group discovery and membership management.
- **Automation**: Pipeline creation from YAML and Release retention policy configuration.

## Governance
This Constitution is the source of truth for all development within the Asgard package. Any new feature must be validated against these principles.

**Version**: 1.0.0 | **Ratified**: 2026-04-22 | **Last Amended**: 2026-04-22

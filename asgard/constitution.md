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
**Reason**: Prevents credential leakage and enables easy configuration across different environments (Dev, CI, Prod).

### V. Atomic & Idempotent Design
Operations like creating branches, setting policies, or managing memberships should be atomic. Where possible, methods should be designed to handle re-execution gracefully (e.g., checking existence before creation).
**Reason**: Ensures stability in CI/CD pipelines where retries are common.

## Technical Requirements

### 1. Project Management
- Must support CRUD operations.
- Must provide a dedicated `exists_project(name)` method for easy validation.

### 2. Repository Management
- **File Ops**: Support fetching content and pushing updates (Commits).
- **Size Constraints**: Must be able to enforce a 5MB repository size limit via Azure DevOps settings/policies.
- **Branch Management**: Support branch creation and policy enforcement (Work Item binding, Comment resolution, Base Merge mode).

### 3. Member & Identity Management
- Support CRUD for project members.
- Support group-based management, specifically finding "Project Managers" and "Project Members" (Contributors) groups.
- Enable adding/removing users from specific groups using descriptors.

### 4. Pipeline & Release Automation
- **Pipeline**: Enable creating pipelines from YML files stored in repositories.
- **Retention**: Strictly enforce retention policies for Releases (deletion days, default keep days, max versions, and associated build records).

## Governance
This Constitution is the source of truth for all development within the Asgard package. Any new feature must be validated against these principles before merging.

**Version**: 1.0.0 | **Ratified**: 2026-04-22 | **Last Amended**: 2026-04-22

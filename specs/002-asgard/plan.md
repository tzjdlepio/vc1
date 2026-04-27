# Asgard Implementation Plan

## Phase 1: Core Package Development (Week 4 & 5) - COMPLETED
The core package is structured into resource-specific managers.

1.  **ProjectManager (`projects.py`)**: Implement project CRUD and existence checks.
2.  **RepoManager (`repos.py`)**: Implement repository CRUD, file content operations (get/push), size limits, and branch management (creation/policies).
3.  **MemberManager (`members.py`)**: Implement member listing, group discovery (PM/Member), and membership management (add/remove).
4.  **PipelineManager (`pipelines.py`)**: Implement pipeline creation from YAML.
5.  **ReleaseManager (`releases.py`)**: Implement release retention policy configuration.

## Phase 2: Automation Runbooks (Week 6) - IN PROGRESS

### 1. `create_project` Runbook Implementation
This runbook will orchestrate multiple managers to perform a full project bootstrap.

- **Location**: `asgard/runbooks.py` (New file)
- **Workflow**:
    1.  Initialize `AsgardClient` and Managers.
    2.  Check if Project name exists.
    3.  If not exists, create Project.
    4.  Verify/Create Repo with the same name.
    5.  Apply 5MB size limit to the repo.
    6.  Fetch `pipeline.yml` from a template source (e.g., another repo or local path) and push to `pipelines/main.yml`.
    7.  Create a Build Pipeline using the pushed YAML.
    8.  Create standard branches: `develop`, `uat`, `master`, `hotfix`.
    9.  Apply branch policies to each branch.
    10. Locate "Project Manager" and "Project Member" groups.
    11. Add initial members to their respective groups.

### 2. `modify_member` Runbook Implementation
A utility for bulk or targeted member management.

- **Workflow**:
    1.  Discover group descriptors for the specified project.
    2.  Iterate through a list of users and add/remove them from the target group.

## Phase 3: Validation & Testing
- Unit tests for each Manager class.
- Integration tests for Runbooks in a sandbox Azure DevOps organization.
- Verification of policy enforcement (manual check in ADO UI).

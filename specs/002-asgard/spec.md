# Asgard (Azure DevOps Python Package) Specification

## Background
Asgard is a Python package designed to simplify and automate common Azure DevOps operations. It provides a clean, resource-oriented API for managing projects, repositories, members, pipelines, and releases.

## Scope
The project covers the development of the core `asgard` package and a set of automation runbooks.

### Week 4 & 5: Core Package Development
- **Constitution**: Establish core principles and technical requirements.
- **Project Management**: CRUD operations and existence checks.
- **Repository Management**: 
    - List, create, get, update, delete repositories.
    - Fetch file content from specific branches.
    - Push file updates (commit) to repositories.
    - Set repository size limits (5MB).
- **Branch & Policy**:
    - Create branches (`develop`, `uat`, `master`, `hotfix`).
    - Enforce branch policies:
        - Work Item linking.
        - Comment resolution required.
        - Merge Strategy: Basic Merge (No Fast-Forward).
- **Member Management**:
    - Find "ProjectManager" and "ProjectMember" groups.
    - Add/remove users from these groups.
- **Pipeline & Release**:
    - Create pipelines from YAML files.
    - Configure Release retention policies (UI deletion, default/max days, build retention).

### Week 6: Automation Runbooks
- **create_project Runbook**:
    - Pre-check: Verify project existence and repo name consistency.
    - Initialization: Create project and default repository.
    - Configuration: Set 5MB size limit.
    - CI Setup: Copy `pipeline.yml` to `pipelines/main.yml` and create the build.
    - Branching: Create standard branches and apply policies.
    - Access Control: Assign users to PM/Member groups.
- **modify_member Runbook**:
    - Scalable member management for adding or removing users from PM/Member groups.

## Technical Stack
- Python 3.9+
- `requests` (via `AsgardClient`)
- Azure DevOps REST API

## Success Criteria
- All `asgard` package methods are tested and functional.
- Runbooks successfully automate the end-to-end project setup process.
- All operations adhere to the Asgard Constitution.

# Asgard Development Tasks

## Week 4 & 5: Foundation (Completed)
- [x] Create `asgard/constitution.md`
- [x] Implement `AsgardClient` for API communication
- [x] Implement `ProjectManager` (CRUD + Existence check)
- [x] Implement `RepoManager` (CRUD + File Ops + Size Limit)
- [x] Implement `MemberManager` (Group Discovery + Add/Remove)
- [x] Implement `PipelineManager` (YAML to Build)
- [x] Implement `ReleaseManager` (Retention Policies)
- [x] Implement Branch creation and Policy enforcement in `RepoManager`

## Week 6: Automation & Runbooks (To-Do)

### Task 1: Create `asgard/pipelines.py` or `asgard/runbooks.py`
- [ ] Implement `create_project` runbook logic
    - [ ] Add pre-check for project existence
    - [ ] Orchestrate project and repo creation
    - [ ] Implement file copying from template repo to target repo
    - [ ] Create build pipeline from YAML
    - [ ] Automate creation of `develop`, `uat`, `master`, `hotfix` branches
    - [ ] Apply policies to all created branches
    - [ ] Assign initial users to PM/Member groups
- [ ] Implement `modify_member` runbook logic
    - [ ] Add support for bulk adding/removing members

### Task 2: Refinement & Validation
- [ ] Verify Week 4 & 5 implementations with unit tests
- [ ] Test Runbooks end-to-end
- [ ] Record token usage and execution time as requested

## Metrics Tracking
- [ ] Record total tokens used for Week 6 implementation
- [ ] Record total time spent on Week 6 tasks

## Documentation & Retention
- [x] Update `spec.md` with Week 4, 5, 6 requirements
- [x] Update `plan.md` with Runbook strategy
- [x] Maintain existing spec files for future reference

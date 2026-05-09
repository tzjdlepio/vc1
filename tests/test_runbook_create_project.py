import pytest
from unittest.mock import MagicMock, patch
from asgard import AsgardClient
from runbooks.create_project import CreateProjectRunbook

@pytest.fixture
def mock_client():
    return MagicMock(spec=AsgardClient)

def test_create_project_runbook_execution_flow(mock_client):
    """
    測試 create_project runbook 的執行流程，確認各個 Manager 有被正確呼叫。
    """
    runbook = CreateProjectRunbook(mock_client)
    
    # 模擬各個 Manager
    runbook.projects = MagicMock()
    runbook.repos = MagicMock()
    runbook.members = MagicMock()
    runbook.pipelines = MagicMock()
    
    # 設定模擬回傳值
    runbook.projects.exists_project.return_value = False
    runbook.projects.create_project.return_value = {"id": "proj-123", "name": "TestProj"}
    runbook.repos.create_repo.return_value = {"id": "repo-456", "name": "TestRepo"}
    runbook.repos.set_repo_size_limit.return_value = {"status": "success"}
    runbook.repos.get_file_content.return_value = "fake content"
    runbook.repos.push_file_content.return_value = {"status": "success"}
    runbook.pipelines.create_pipeline_from_yml.return_value = {"id": "pipe-789"}
    runbook.members.find_groups.return_value = {
        "ProjectManager": "manager-group-desc",
        "ProjectMember": "member-group-desc"
    }
    
    # 執行 runbook
    result = runbook.execute(
        project_name="TestProj",
        repo_name="TestRepo",
        managers=["manager@example.com"],
        members=["member@example.com"]
    )
    
    # 驗證結果
    assert result["status"] == "success"
    
    # 驗證各步驟是否被呼叫
    runbook.projects.create_project.assert_called_once_with("TestProj")
    runbook.repos.create_repo.assert_called_once_with("TestProj", "TestRepo")
    runbook.repos.set_repo_size_limit.assert_called_once_with("repo-456", limit_mb=5)
    runbook.members.add_user_to_group.assert_any_call("manager@example.com", "manager-group-desc")
    runbook.members.add_user_to_group.assert_any_call("member@example.com", "member-group-desc")

def test_create_project_runbook_already_exists(mock_client):
    """
    測試當專案已存在時，runbook 應回傳失敗。
    """
    runbook = CreateProjectRunbook(mock_client)
    runbook.projects = MagicMock()
    runbook.projects.exists_project.return_value = True
    
    result = runbook.execute(project_name="ExistingProj")
    
    assert result["status"] == "failed"
    assert "already exists" in result["error"]
    runbook.projects.create_project.assert_not_called()

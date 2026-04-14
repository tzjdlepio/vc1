from typing import List, Dict, Any
from .client import AsgardClient

class RepoManager:
    """管理 Azure DevOps Git Repositories 的 CRUD"""
    
    def __init__(self, client: AsgardClient):
        self.client = client

    def list_repos(self, project_name: str) -> List[Dict[str, Any]]:
        """列出特定 Project 下的所有 Repos"""
        response = self.client.get(f"/{project_name}/_apis/git/repositories")
        return response.get("value", [])

    def get_repo(self, project_name: str, repo_id: str) -> Dict[str, Any]:
        """取得特定 Repo 資訊"""
        return self.client.get(f"/{project_name}/_apis/git/repositories/{repo_id}")

    def create_repo(self, project_name: str, name: str) -> Dict[str, Any]:
        """在特定 Project 下建立新 Repo"""
        payload = {"name": name}
        return self.client.post(f"/{project_name}/_apis/git/repositories", json=payload)

    def update_repo(self, project_name: str, repo_id: str, new_name: str) -> Dict[str, Any]:
        """更新 Repo 名稱"""
        payload = {"name": new_name}
        return self.client.patch(f"/{project_name}/_apis/git/repositories/{repo_id}", json=payload)

    def delete_repo(self, project_name: str, repo_id: str) -> bool:
        """刪除 Repo"""
        return self.client.delete(f"/{project_name}/_apis/git/repositories/{repo_id}")

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

    def get_file_content(self, project_name: str, repo_id: str, path: str, version: str = "main") -> str:
        """取得特定來源的特定檔案內容"""
        params = {
            "path": path,
            "includeContent": "true",
            "versionDescriptor.version": version
        }
        response = self.client.get(f"/{project_name}/_apis/git/repositories/{repo_id}/items", params=params)
        return response.get("content", "")

    def push_file_content(self, project_name: str, repo_id: str, path: str, content: str, branch: str, message: str) -> Dict[str, Any]:
        """將檔案內容推送到指定的 repo 中 (Commit)"""
        # 取得最新 Commit ID (Old ObjectId)
        refs = self.client.get(f"/{project_name}/_apis/git/repositories/{repo_id}/refs", params={"filter": f"heads/{branch}"})
        old_object_id = refs["value"][0]["objectId"] if refs.get("value") else "0000000000000000000000000000000000000000"

        payload = {
            "refUpdates": [{"name": f"refs/heads/{branch}", "oldObjectId": old_object_id}],
            "commits": [{
                "comment": message,
                "changes": [{
                    "changeType": "edit" if old_object_id != "0000000000000000000000000000000000000000" else "add",
                    "item": {"path": path},
                    "newContent": {"content": content, "contentType": "rawtext"}
                }]
            }]
        }
        return self.client.post(f"/{project_name}/_apis/git/repositories/{repo_id}/pushes", json=payload)

    def set_repo_size_limit(self, repo_id: str, limit_mb: int = 5) -> Dict[str, Any]:
        """設定 repo 大小限制 (預設 5MB)"""
        # 註：這通常透過 Project Settings 或特定的 Policy 實作。
        # 此處使用 Azure DevOps 的 Settings Entries API 示範。
        key = f"ms.vss-code.repository-size-limit-{repo_id}"
        payload = {"value": str(limit_mb * 1024 * 1024)} # Byte
        return self.client.put(f"/_apis/settings/entries/me", json={key: payload["value"]})

    def create_branch(self, project_name: str, repo_id: str, branch_name: str, source_branch: str = "main") -> Dict[str, Any]:
        """建立分支"""
        refs = self.client.get(f"/{project_name}/_apis/git/repositories/{repo_id}/refs", params={"filter": f"heads/{source_branch}"})
        source_object_id = refs["value"][0]["objectId"]
        
        payload = [{
            "name": f"refs/heads/{branch_name}",
            "oldObjectId": "0000000000000000000000000000000000000000",
            "newObjectId": source_object_id
        }]
        return self.client.post(f"/{project_name}/_apis/git/repositories/{repo_id}/refs", json=payload)

    def set_branch_policy(self, project_id: str, repo_id: str, branch_pattern: str = "refs/heads/main") -> List[Dict[str, Any]]:
        """
        設置分支 Policy:
        - 必須綁定 Work Item
        - PR 留言必須全部解完
        - Merge 模式為 Base Merge (No Fast-Forward)
        """
        policies = []
        # 1. Work Item Binding
        policies.append(self._create_policy_config(project_id, repo_id, branch_pattern, "40e30b90-eec9-4bea-92f1-616401019001", {}))
        # 2. Comment Resolution
        policies.append(self._create_policy_config(project_id, repo_id, branch_pattern, "c6a188d0-619b-4aa1-95ee-9b9fa13c2e0e", {}))
        # 3. Base Merge (Merge Strategy)
        policies.append(self._create_policy_config(project_id, repo_id, branch_pattern, "fa4e907d-c16b-4a4c-9dfa-4906e5d171dd", {
            "useSquashMerge": False, "allowRebase": False, "allowNoFastForward": True
        }))
        return policies

    def _create_policy_config(self, project_id: str, repo_id: str, branch_pattern: str, type_id: str, settings: Dict) -> Dict:
        payload = {
            "type": {"id": type_id},
            "isBlocking": True,
            "isEnabled": True,
            "settings": {
                "scope": [{"repositoryId": repo_id, "refName": branch_pattern, "matchKind": "exact"}]
            }
        }
        payload["settings"].update(settings)
        return self.client.post(f"/{project_id}/_apis/policy/configurations", json=payload)

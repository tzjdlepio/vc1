from typing import List, Dict, Any
from .client import AsgardClient

class ProjectManager:
    """管理 Azure DevOps Projects 的 CRUD"""
    
    def __init__(self, client: AsgardClient):
        self.client = client

    def list_projects(self) -> List[Dict[str, Any]]:
        """列出所有 Projects"""
        response = self.client.get("/_apis/projects")
        return response.get("value", [])

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """取得單一 Project 資訊"""
        return self.client.get(f"/_apis/projects/{project_id}")

    def create_project(self, name: str, description: str = "", process_id: str = None) -> Dict[str, Any]:
        """
        建立新 Project
        註：Azure DevOps 建立專案是異步操作，回傳的是 Operation 資訊。
        """
        payload = {
            "name": name,
            "description": description,
            "capabilities": {
                "versioncontrol": {"sourceControlType": "Git"},
                "processTemplate": {"templateTypeId": process_id or "adcc42ab-9882-485e-a3ed-7678f01f66bc"} # 預設 Agile
            }
        }
        return self.client.post("/_apis/projects", json=payload)

    def update_project(self, project_id: str, description: str) -> Dict[str, Any]:
        """更新 Project 描述"""
        payload = {"description": description}
        return self.client.patch(f"/_apis/projects/{project_id}", json=payload)

    def delete_project(self, project_id: str) -> bool:
        """刪除 Project"""
        return self.client.delete(f"/_apis/projects/{project_id}")

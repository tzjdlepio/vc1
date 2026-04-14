from typing import List, Dict, Any
from .client import AsgardClient

class MemberManager:
    """管理 Azure DevOps Project Members 的 CRUD"""
    
    def __init__(self, client: AsgardClient):
        self.client = client

    def list_project_members(self, project_id: str, team_id: str = None) -> List[Dict[str, Any]]:
        """
        列出專案/團隊成員
        註：在 Azure DevOps 中，成員通常隸屬於 Team。預設會建立一個與專案同名的 Team。
        """
        t_id = team_id or project_id # 預設 Team ID 通常與 Project ID 關聯
        response = self.client.get(f"/_apis/projects/{project_id}/teams/{t_id}/members")
        return response.get("value", [])

    def add_member_to_project(self, project_id: str, user_descriptor: str, team_id: str = None) -> Dict[str, Any]:
        """
        新增成員至專案團隊
        註：Azure DevOps 使用 Descriptor 或 Identity ID。
        """
        t_id = team_id or project_id
        # 此處使用 Identity API (注意：Member Entitlement API 可能更適合某些情境)
        # 這裡示範最常見的 Add 方式
        payload = {
            "values": [{"id": user_descriptor}]
        }
        return self.client.patch(f"/_apis/projects/{project_id}/teams/{t_id}/members", json=payload)

    def remove_member_from_project(self, project_id: str, user_id: str, team_id: str = None) -> bool:
        """從專案團隊移除成員"""
        t_id = team_id or project_id
        return self.client.delete(f"/_apis/projects/{project_id}/teams/{t_id}/members/{user_id}")

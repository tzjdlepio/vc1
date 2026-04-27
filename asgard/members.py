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

    def find_groups(self, project_name: str) -> Dict[str, str]:
        """尋找 Project Administrators (Manager) 與 Contributors (Member) 的群組 Descriptor"""
        # Graph API 通常在 vssps.dev.azure.com
        # 這裡簡化實作，先列出所有 Graph Groups
        response = self.client.get("/_apis/graph/groups", api_version="6.0-preview.1")
        groups = response.get("value", [])
        
        result = {}
        target_manager = f"[{project_name}]\\Project Administrators"
        target_member = f"[{project_name}]\\Contributors"
        
        for g in groups:
            if g.get("principalName") == target_manager:
                result["ProjectManager"] = g["descriptor"]
            elif g.get("principalName") == target_member:
                result["ProjectMember"] = g["descriptor"]
        return result

    def add_user_to_group(self, user_descriptor: str, group_descriptor: str) -> Dict[str, Any]:
        """將人加入群組"""
        return self.client.put(f"/_apis/graph/memberships/{user_descriptor}/{group_descriptor}", api_version="6.0-preview.1")

    def remove_user_from_group(self, user_descriptor: str, group_descriptor: str) -> bool:
        """將人移除群組"""
        return self.client.delete(f"/_apis/graph/memberships/{user_descriptor}/{group_descriptor}", api_version="6.0-preview.1")

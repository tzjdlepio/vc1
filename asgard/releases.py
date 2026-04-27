from typing import Dict, Any
from .client import AsgardClient

class ReleaseManager:
    """管理 Azure DevOps Release 設定"""
    
    def __init__(self, client: AsgardClient):
        self.client = client

    def set_release_retention_policy(self, 
                                     project_id: str, 
                                     days_to_keep_deleted_from_ui: int = 30,
                                     default_days_to_keep: int = 30,
                                     max_days_to_keep: int = 365,
                                     max_releases_to_keep: int = 50,
                                     retain_build: bool = True) -> Dict[str, Any]:
        """
        設定 Release 的 retention policy
        :param days_to_keep_deleted_from_ui: 設定從 UI 上刪除的保留天數
        :param default_days_to_keep: 設定預設保留天數
        :param max_days_to_keep: 設定最高保留天數
        :param max_releases_to_keep: 設定最高保留代數
        :param retain_build: 設定預設是否保留關聯的 Build 記錄
        """
        payload = {
            "daysToKeepDeletedReleases": days_to_keep_deleted_from_ui,
            "defaultRetentionPolicy": {
                "daysToKeep": default_days_to_keep,
                "releasesToKeep": 1, # Azure DevOps 預設通常為 1
                "retainBuild": retain_build
            },
            "maximumRetentionPolicy": {
                "daysToKeep": max_days_to_keep,
                "releasesToKeep": max_releases_to_keep,
                "retainBuild": retain_build
            }
        }
        # 註：Release Settings API 通常在 vsrm.dev.azure.com
        return self.client.patch(f"/{project_id}/_apis/release/retentionsettings", json=payload, api_version="6.0-preview.1")

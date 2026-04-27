from typing import Dict, Any
from .client import AsgardClient

class PipelineManager:
    """管理 Azure DevOps Pipelines"""
    
    def __init__(self, client: AsgardClient):
        self.client = client

    def create_pipeline_from_yml(self, project_id: str, name: str, repo_id: str, yml_path: str = "/azure-pipelines.yml") -> Dict[str, Any]:
        """將 yml 檔案轉成 pipeline build"""
        payload = {
            "name": name,
            "configuration": {
                "type": "yaml",
                "path": yml_path,
                "repository": {
                    "id": repo_id,
                    "type": "azureReposGit"
                }
            }
        }
        return self.client.post(f"/{project_id}/_apis/pipelines", json=payload, api_version="6.0-preview.1")

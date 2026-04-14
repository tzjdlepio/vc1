import requests
import base64
from typing import Any, Dict, Optional
from .config import Config
from .exceptions import AsgardAPIException

class AsgardClient:
    """Azure DevOps REST API 的核心封裝 Client"""
    
    def __init__(self, org_url: Optional[str] = None, pat: Optional[str] = None):
        """
        初始化 Client
        :param org_url: Azure DevOps Organization URL
        :param pat: Personal Access Token
        """
        self.org_url = org_url or Config.AZURE_DEVOPS_ORG_URL
        self.pat = pat or Config.AZURE_DEVOPS_PAT
        
        if not self.org_url or not self.pat:
            raise ValueError("Organization URL and PAT must be provided either via constructor or environment variables.")
        
        self.org_url = self.org_url.rstrip('/')
        self._session = requests.Session()
        self._session.headers.update(self._get_headers())

    def _get_headers(self) -> Dict[str, str]:
        """產生成認證所需的 Headers (使用 PAT 的 Basic Auth)"""
        token = base64.b64encode(f":{self.pat}".encode()).decode()
        return {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json"
        }

    def request(self, method: str, path: str, api_version: str = "6.0", **kwargs) -> Any:
        """
        發送 HTTP 請求的通用方法
        :param method: HTTP Method (GET, POST, etc.)
        :param path: API 路徑 (不含 org_url)
        :param api_version: API 版本號
        :param kwargs: 其他 requests.request 的參數
        """
        # 自動處理 API Version
        params = kwargs.get("params", {})
        if "api-version" not in params:
            params["api-version"] = api_version
        kwargs["params"] = params

        # 拼接完整的 URL
        url = f"{self.org_url}{path}"
        
        try:
            response = self._session.request(method, url, **kwargs)
            # 檢查並處理 HTTP 錯誤
            if not response.ok:
                raise AsgardAPIException(
                    f"API Request Failed: {response.status_code} {response.reason}",
                    status_code=response.status_code,
                    response_body=response.text
                )
            
            # 若有內容則回傳 JSON，否則回傳 True
            if response.status_code == 204:
                return True
            return response.json()
            
        except requests.RequestException as e:
            raise AsgardAPIException(f"Network error: {str(e)}")

    def get(self, path: str, **kwargs): return self.request("GET", path, **kwargs)
    def post(self, path: str, **kwargs): return self.request("POST", path, **kwargs)
    def patch(self, path: str, **kwargs): return self.request("PATCH", path, **kwargs)
    def put(self, path: str, **kwargs): return self.request("PUT", path, **kwargs)
    def delete(self, path: str, **kwargs): return self.request("DELETE", path, **kwargs)

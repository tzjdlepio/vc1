import os
from dotenv import load_dotenv

# 嘗試載入 .env 檔案
load_dotenv()

class Config:
    """集中管理 Asgard 的配置資訊"""
    
    # Azure DevOps Organization URL (e.g., https://dev.azure.com/my-org)
    AZURE_DEVOPS_ORG_URL = os.getenv("AZURE_DEVOPS_ORG_URL")
    
    # Personal Access Token (PAT)
    AZURE_DEVOPS_PAT = os.getenv("AZURE_DEVOPS_PAT")

    # API 版本預設值
    DEFAULT_API_VERSION = "6.0"

    @classmethod
    def validate(cls):
        """驗證必要配置是否存在"""
        if not cls.AZURE_DEVOPS_ORG_URL:
            raise ValueError("AZURE_DEVOPS_ORG_URL is missing.")
        if not cls.AZURE_DEVOPS_PAT:
            raise ValueError("AZURE_DEVOPS_PAT is missing.")
        
        # 確保 URL 不以斜線結尾，方便後續拼接
        cls.AZURE_DEVOPS_ORG_URL = cls.AZURE_DEVOPS_ORG_URL.rstrip('/')

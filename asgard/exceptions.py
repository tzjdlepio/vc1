class AsgardException(Exception):
    """Asgard 專案的基礎異常類"""
    pass

class AsgardAPIException(AsgardException):
    """當 Azure DevOps API 回傳非 2xx 狀態碼時拋出"""
    def __init__(self, message, status_code=None, response_body=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

class AsgardConfigException(AsgardException):
    """當配置資訊缺失或格式錯誤時拋出"""
    pass

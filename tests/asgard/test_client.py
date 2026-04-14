import pytest
from unittest.mock import MagicMock, patch
from asgard.client import AsgardClient
from asgard.exceptions import AsgardAPIException

@patch("requests.Session.request")
def test_client_request_success(mock_request):
    # 模擬 API 回傳成功
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.json.return_value = {"value": "success"}
    mock_request.return_value = mock_response

    client = AsgardClient(org_url="https://dev.azure.com/test", pat="fake-pat")
    result = client.get("/_apis/test")

    assert result == {"value": "success"}
    mock_request.assert_called_once()

@patch("requests.Session.request")
def test_client_request_failure(mock_request):
    # 模擬 API 回傳失敗
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    mock_response.text = "Resource not found"
    mock_request.return_value = mock_response

    client = AsgardClient(org_url="https://dev.azure.com/test", pat="fake-pat")
    
    with pytest.raises(AsgardAPIException) as excinfo:
        client.get("/_apis/invalid")
    
    assert "404" in str(excinfo.value)
    assert excinfo.value.status_code == 404

# Asgard Project Constitution

## 1. 專案願景
Asgard 是一個輕量化、易用的 Azure DevOps REST API Python 封裝庫。旨在簡化開發者對 Azure DevOps 資源的操作，並提供一致的開發介面。

## 2. 命名規範
- **Module/Package**: 全小寫，底線分隔 (Snake Case)，如 `asgard.projects`。
- **Class**: 大駝峰 (Pascal Case)，如 `AsgardClient`。
- **Function/Method**: 小寫底線 (Snake Case)，如 `list_projects`。
- **Variables**: 具備語義的小寫底線，避免單一字母命名。

## 3. 模組分工
- `client.py`: 唯一負責與網路層 (requests) 接軌的模組，處理底層通訊與共通 Headers。
- `config.py`: 集中管理所有來自環境變數或設定檔的參數。
- `exceptions.py`: 定義專案專屬的異常層級，方便調用者捕獲。
- `models.py`: 封裝 API 回傳的 JSON 數據，提供物件化存取。
- `[resource].py`: 各資源的商業邏輯與 URL 構建。

## 4. 認證資訊管理方式
- **禁止硬編碼 (Hard-coding)**: 任何 PAT (Personal Access Token) 或 URL 均不得出現在程式碼中。
- **環境變數**: 優先從 `.env` 檔案或系統環境變數讀取。
- **優先順序**: 實體化 Client 時傳入參數 > 環境變數。

## 5. 錯誤處理方式
- 網路錯誤、4xx/5xx 狀態碼應被轉換為 `AsgardException` 或其子類。
- 每個 API 呼叫必須執行 `response.raise_for_status()` 或在 Client 層級統一判斷。
- 應提供具備除錯資訊的錯誤訊息 (包含狀態碼與 API 回傳內容)。

## 6. CRUD Function 設計風格
- **Create**: `create_[resource](**kwargs)` -> 回傳新建立的物件。
- **Read (List)**: `list_[resource](**filters)` -> 回傳物件列表。
- **Read (Get)**: `get_[resource](identity)` -> 回傳單一物件。
- **Update**: `update_[resource](identity, **updates)` -> 回傳更新後的物件。
- **Delete**: `delete_[resource](identity)` -> 布林值或空回傳。

## 7. 測試原則
- **100% Mocking**: 單元測試不應依賴真實的 Azure DevOps 環境。
- **使用 pytest**: 配合 `unittest.mock` 或 `responses` 套件模擬 API 回傳。
- **覆蓋率**: 每個 CRUD 至少有一個成功的 Test Case 與一個失敗的 Test Case。

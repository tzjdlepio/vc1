# Tasks: Parameterized Runbook Pipeline

## 1. 程式碼清理 (Cleanup)
- [x] **T1.1: 移除 `runbooks/create_project.py` 中的 Dry Run 邏輯**
    - 刪除 `self.dry_run` 及其相關判斷區塊。
    - 確保 `execute` 直接進入真實 API 呼叫流程。
- [x] **T1.2: 移除 `runbooks/modify_member.py` 中的 Dry Run 邏輯**
    - (若有) 刪除相關模擬代碼。
- [x] **T1.3: 刪除舊的自動化入口腳本**
    - 移除 `scripts/run_asgard_automation.py` (將由新腳本取代)。

## 2. 核心功能開發 (Core Development)
- [x] **T2.1: 建立新的 Runbook 派發腳本 `scripts/run_runbook.py`**
    - 使用 `argparse` 定義所有參數。
    - 實作 Runbook 選擇邏輯。
    - 加入環境變數與參數驗證。
- [x] **T2.2: 實作 `create_project` 的參數傳遞邏輯**
    - 確保 `repo_name`、`manager_email` 等能正確傳入 `CreateProjectRunbook.execute`。

## 3. Pipeline 實作 (Pipeline Implementation)
- [x] **T3.1: 建立 `pipelines/runbook-pipeline.yml`**
    - 定義 `parameters` 區塊。
    - 設定 `trigger: none`。
    - 呼叫 `scripts/run_runbook.py`。
- [x] **T3.2: 關閉 `azure-pipelines.yml` 中的舊自動化階段**
    - 移除或註解掉 `Asgard Runbook Automation` stage，避免混淆。

## 4. 測試與驗證 (Testing & Validation)
- [x] **T4.1: 更新 `tests/` 下的 Runbook 測試案例**
    - 將 Dry Run 測試移除。
    - 新增 Mock 測試，模擬真實呼叫流程並檢查參數正確性。
- [x] **T4.2: 驗證 Pipeline 參數傳遞**
    - 透過本地執行 `python scripts/run_runbook.py --help` 確認參數定義正確。

## 5. 驗收 (Acceptance)
- [x] 確認 ADO UI 可以正確顯示所有參數輸入框。
- [x] 確認選擇 `create_project` 並執行後，日誌中沒有 "Simulation" 或 "Dry Run" 字樣。
- [x] 確認操作結果真實反應在 Azure DevOps Org 中。

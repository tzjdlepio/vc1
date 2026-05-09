# Implementation Plan: Parameterized Runbook Pipeline

## 1. 實作策略
本計畫將透過以下步驟達成目標：
- **清理程式碼**: 移除 `runbooks/` 與 `scripts/` 中所有的 `dry_run` 相關邏輯，將其改為純粹的真實執行。
- **重構入口點**: 修改 `scripts/run_asgard_automation.py` (或建立新腳本) 以接收命令列參數，並根據 `runbook_name` 分派執行任務。
- **建立 Pipeline**: 新增 `pipelines/runbook-pipeline.yml`，定義 UI 參數並呼叫 Python 腳本。
- **安全性優化**: 確保 ADO PAT 等資訊透過 Pipeline 環境變數帶入，不在日誌中列印。

## 2. Pipeline YAML 設計
- 使用 `parameters` 語法定義輸入欄位。
- `trigger: none` 關閉自動觸發。
- 呼叫方式範例：
  ```yaml
  - script: |
      python scripts/run_runbook.py \
        --runbook_name "$(runbook_name)" \
        --project_name "$(project_name)" \
        --repo_name "$(repo_name)" \
        --manager_email "$(manager_email)" \
        --member_email "$(member_email)"
  ```

## 3. 如何根據 Parameter 選擇 Runbook
- 在 Python 進入點腳本中（如 `scripts/run_runbook.py`），使用 `argparse` 解析參數。
- 使用簡單的條件判斷或 Dispatcher 模式根據 `args.runbook_name` 實例化對應的 Runbook 類別並執行。

## 4. 參數傳遞
- 透過命令列引數 (Command Line Arguments) 將 Pipeline Parameters 傳遞給 Python 腳本。
- 在 Python 腳本中進行必要性檢查，若參數缺失則呼叫 `sys.exit(1)`。

## 5. 安全性管理 (Secrets)
- `ADO_PAT` 應存放在 Azure DevOps Pipeline 的 **Secret Variable** 中。
- 在 Pipeline YAML 的 `env` 區塊中，將其對應至環境變數：
  ```yaml
  env:
    ADO_PAT: $(AZURE_DEVOPS_PAT)
    ADO_ORG_URL: $(ADO_ORG_URL)
  ```
- 腳本中嚴禁 `print(os.getenv("ADO_PAT"))`。

## 6. 驗證方式
- **單元測試**: 使用 `unittest.mock` 模擬 `AsgardClient` 的各個 Manager，驗證 `execute` 方法中的調用流程是否符合預期。
- **本地執行**: 在本地帶入真實環境變數執行 Python 腳本，確認能成功打入測試用的 ADO Org。
- **Pipeline 測試**: 在 ADO UI 上手動 Run pipeline，檢查執行日誌。

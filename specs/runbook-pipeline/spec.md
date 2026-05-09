# Specification: Parameterized Runbook Pipeline

## 1. 功能目標
建立一個參數化的 Azure DevOps Pipeline，讓使用者可以手動觸發並選擇要執行的 Runbook，同時輸入該 Runbook 所需的參數，達成自動化維運操作。

## 2. 使用者需求
- 使用者可以在 Azure DevOps UI 的 "Run pipeline" 畫面中，看到可供選擇的 Runbook 清單。
- 使用者可以針對選定的 Runbook 輸入對應的參數（如專案名稱、成員 Email 等）。
- 執行過程必須是 **真實執行 (Real Execution)**，不再支援模擬模式 (Dry Run)。
- 敏感資訊（如 PAT）必須安全地管理，不可洩漏。

## 3. Pipeline Parameters 設計
| 參數名稱 | 顯示名稱 | 類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `runbook_name` | 選擇 Runbook | string (values) | 目前支援：`create_project` |
| `project_name` | 專案名稱 | string | 目標 Azure DevOps 專案名稱 |
| `repo_name` | Repository 名稱 | string | (僅限 create_project) 建立的 Repo 名稱 |
| `manager_email` | Project Manager Email | string | (僅限 create_project) 管理者信箱 |
| `member_email` | Project Member Email | string | (僅限 create_project) 一般成員信箱 |

## 4. 支援的 Runbook 清單
- `create_project`: 建立專案、Repo、分支策略及分配成員。

## 5. `create_project` 需要的參數
- `project_name`: (必填)
- `repo_name`: (必填)
- `manager_email`: (必填)
- `member_email`: (必填)

## 6. 成功條件
- Pipeline 成功根據 `runbook_name` 呼叫對應的 Python 程式。
- 參數正確傳遞至 Python 程式。
- Runbook 在 Azure DevOps 上完成實體操作（如真的建立了專案）。
- Pipeline 日誌中顯示清晰的執行步驟與結果。

## 7. 失敗情境
- 未輸入必填參數（應在腳本中驗證並報錯）。
- 選擇了不支援的 `runbook_name`。
- Azure DevOps API 呼叫失敗（權限不足、名稱重複等）。
- 憑證 (PAT) 遺失或過期。

## 8. 不做的範圍 (Out of Scope)
- **不支援 Dry Run**: 本功能完全移除模擬模式。
- **不支援自動觸發**: 本 Pipeline 僅設計為手動觸發 (Manual Trigger)。
- **不支援多個 Runbook 同時執行**: 一次 Pipeline 執行僅處理一個 Runbook。

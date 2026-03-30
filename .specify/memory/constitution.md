<!--
Sync Impact Report:
- Version change: [CONSTITUTION_VERSION] -> 1.0.0
- List of modified principles:
  - [PRINCIPLE_1_NAME] -> I. 結構化資料夾與命名規範 (Structured Folders & Naming)
  - [PRINCIPLE_2_NAME] -> II. 規格驅動開發 (SDD - Specification Driven Development)
  - [PRINCIPLE_3_NAME] -> III. 自動化品質檢查與 SonarQube (Automated Quality & SonarQube)
  - [PRINCIPLE_4_NAME] -> IV. 安全的機密管理 (Secure Secrets Management)
  - [PRINCIPLE_5_NAME] -> V. 極簡 CI/CD 與易維護性 (Simple CI/CD & Maintainability)
- Added sections:
  - 技術棧與工具 (Technology Stack & Tools)
  - 開發與部署流程 (Dev & Deployment Workflow)
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md (✅ updated/reviewed)
  - .specify/templates/spec-template.md (✅ updated/reviewed)
  - .specify/templates/tasks-template.md (✅ updated/reviewed)
- Follow-up TODOs: None
-->

# Azure DevOps 學生專案憲法 (Azure DevOps Student Project Constitution)

## 核心原則 (Core Principles)

### I. 結構化資料夾與命名規範 (Structured Folders & Naming)
專案結構必須直觀且命名清晰，方便初學者理解。核心程式碼、測試、文件與設定檔應有明確區隔（例如 `src/`, `tests/`, `docs/`, `pipelines/`）。變數與函式命名應具描述性，禁止使用不明縮寫。Python 代碼必須遵循 PEP 8 規範。
**理由**：確保初學者能快速定位檔案，並養成良好的編碼習慣，降低長期維護成本。

### II. 規格驅動開發 (SDD - Specification Driven Development)
所有功能開發必須遵循「規格優先」原則。在撰寫代碼前，必須先完成規格文件（Spec）與實作計畫（Plan），並使用 Gemini CLI 進行驗證與輔助。
**理由**：培養先思考再動手的工程思維，確保開發目標明確且可追蹤。

### III. 自動化品質檢查與 SonarQube (Automated Quality & SonarQube)
每次 Commit 必須自動觸發 Azure DevOps Pipeline。Pipeline 必須包含 SonarQube 靜態掃描，且必須通過預設的品質門檻（Quality Gate）。代碼應包含基礎的單元測試，並在 CI 階段執行。
**理由**：透過自動化工具確保代碼品質，即時發現潛在錯誤，並減少人為審查的負擔。

### IV. 安全的機密管理 (Secure Secrets Management)
嚴禁在程式碼、設定檔或文件中硬編碼（Hard-code）任何 API Key、密碼或敏感資訊。所有機密資訊必須儲存於 Azure DevOps Variable Groups 或環境變數中。
**理由**：建立基礎的資訊安全意識，防止敏感資訊外洩，並確保部署環境的安全性。

### V. 極簡 CI/CD 與易維護性 (Simple CI/CD & Maintainability)
Pipeline 的 YAML 設定應保持簡潔，步驟邏輯清晰（Build -> Test -> Analyze -> Deploy），並附上繁體中文註釋。避免過度複雜的腳本，確保專案對初學者友善且易於維護。
**理由**：降低初學者的學習與維護門檻，確保專案能被持續開發與更新。

## 技術棧與工具 (Technology Stack & Tools)

- **開發語言**：Python 3.x
- **CI/CD 平台**：Azure DevOps Pipelines
- **品質分析**：SonarQube
- **AI 輔助工具**：Gemini CLI
- **開發方法論**：SDD (Specification -> Plan -> Tasks -> Code)

## 開發與部署流程 (Development Workflow & Gates)

- **分支管理**：建議使用 Git Flow 或 GitHub Flow，所有功能開發應在 Feature 分支進行。
- **品質門檻**：Pull Request 必須通過所有單元測試與 SonarQube 掃描方可合併。
- **機密檢查**：部署前必須確認所有必要的 Secrets 已正確配置於目標環境。
- **同步更新**：代碼變更時，相關的規格文件與實作計畫應同步更新。

## 治理 (Governance)

本憲法為專案開發的最高準則。所有參與開發的人員與 AI Agent 均須嚴格遵守上述原則。若有違反憲法之行為，應在 Pull Request 階段予以攔截並修正。
本憲法的修訂需經過團隊成員討論並記錄版本變更。

**Version**: 1.0.0 | **Ratified**: 2026-03-30 | **Last Amended**: 2026-03-30

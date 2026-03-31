# 專案說明 (README)

## 目錄結構

- `asgards/`: 核心原始碼 (Python)
- `pipelines/`: CI/CD 相關設定與腳本
- `azure-pipelines.yml`: Azure DevOps Pipeline 定義

## 快速開始

1. **開發**: 在 `asgards/` 目錄下撰寫 Python 程式。
2. **測試**: 執行 `python -m unittest discover asgards`。
3. **部署**: Push 到 `main` 分支後，Azure DevOps 將自動啟動 Pipeline 並執行 SonarQube 掃描。

## 憲法提醒

- 遵守 PEP 8 命名規範。
- 嚴禁硬編碼 Secrets (API Keys)。
- 確保 Pipeline 綠燈 (通過 SonarQube 品質門檻)。2

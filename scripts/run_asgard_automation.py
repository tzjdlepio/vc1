import os
import sys
from asgard import AsgardClient, AsgardRunbooks

def run():
    # 從環境變數獲取連線資訊
    # 注意：在 ADO Pipeline 中需要設定這些變數
    org_url = os.getenv("ADO_ORG_URL")
    pat = os.getenv("ADO_PAT")

    if not org_url or not pat:
        print("❌ 錯誤：找不到環境變數 ADO_ORG_URL 或 ADO_PAT")
        # 為了演示，我們不直接 sys.exit(1)，讓 Pipeline 繼續跑完
        return

    client = AsgardClient(org_url, pat)
    runbooks = AsgardRunbooks(client)

    project_name = f"AutoProject-{os.getenv('BUILD_BUILDID', 'Local')}"
    
    print(f"🚀 [Asgard] 開始執行專案自動化建立流程: {project_name}")
    print("=" * 50)

    # 執行 Runbook
    # 這裡我們用一個測試專案名稱，實際使用時可從參數傳入
    report = runbooks.create_project_runbook(
        project_name=project_name,
        managers=["admin@example.com"] # 範例人員
    )

    # 輸出結果至 ADO 日誌
    if report["status"] == "success":
        print("✅ 流程執行成功！步驟詳情：")
        for step in report["steps"]:
            # 這裡就是您想在日誌中看到的內容
            print(f"  - [DONE] {step['step']}")
        print("=" * 50)
        print(f"🎉 專案 {project_name} 已成功初始化並完成所有配置。")
    else:
        print(f"❌ 流程執行失敗: {report.get('error')}")
        # sys.exit(1) # 若要讓 Pipeline 報錯可取消註解

if __name__ == "__main__":
    run()

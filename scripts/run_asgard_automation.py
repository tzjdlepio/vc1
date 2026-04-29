import os
import sys
from asgard import AsgardClient
from runbooks.create_project import CreateProjectRunbook

def run():
    # 檢查 Dry Run 模式
    dry_run_env = os.getenv("ASGARD_DRY_RUN", "false").lower() == "true"
    
    # 從環境變數獲取連線資訊
    org_url = os.getenv("ADO_ORG_URL")
    pat = os.getenv("ADO_PAT")

    print("=" * 60)
    if dry_run_env:
        print("🛡️  模式: [DRY RUN / SIMULATION]")
        print("💡 說明: 目前處於模擬模式，不會對 Azure DevOps 產生任何真實變動。")
    else:
        print("🔥 模式: [REAL EXECUTION]")
        print("⚠️  警告: 目前處於真實執行模式，將會呼叫 API 進行實體操作。")
    print("=" * 60)

    # 在 Dry Run 模式下，即使沒有 PAT 也可以繼續執行模擬
    if not dry_run_env and (not org_url or not pat):
        print("❌ 錯誤：真實執行模式下找不到環境變數 ADO_ORG_URL 或 ADO_PAT")
        sys.exit(1)

    # 初始化 Client
    client = AsgardClient(org_url or "https://simulated.dev.azure.com/org", pat or "simulated-pat")
    
    # 初始化特定的 Runbook
    runbook = CreateProjectRunbook(client)

    project_name = f"AutoProject-{os.getenv('BUILD_BUILDID', 'Local')}"
    
    print(f"🚀 [Asgard] 開始執行流程: {project_name}")

    # 執行 Runbook
    report = runbook.execute(
        project_name=project_name,
        managers=["admin@example.com"]
    )

    # 輸出結果
    print("-" * 60)
    if report["status"] in ["success", "simulated_success"]:
        print(f"✅ 流程完成！(狀態: {report['status']})")
        if "steps" in report:
            for step in report["steps"]:
                print(f"  - [{step['step']}]: {step['result']}")
        print("=" * 60)
        print(f"🎉 專案 {project_name} 處理完畢。")
    else:
        print(f"❌ 流程執行失敗: {report.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    run()

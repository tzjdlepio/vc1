import os
import sys
import argparse
from typing import List

# 確保可以匯入 runbooks 與 asgard
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "src"))

from asgard import AsgardClient
from runbooks.create_project import CreateProjectRunbook
from runbooks.modify_member import ModifyMemberRunbook

def main():
    parser = argparse.ArgumentParser(description="Asgard Runbook Dispatcher")
    
    # 通用參數
    parser.add_argument("--runbook_name", required=True, help="要執行的 Runbook 名稱 (例如: create_project)")
    parser.add_argument("--project_name", required=True, help="目標 Azure DevOps 專案名稱")
    
    # create_project 專用參數
    parser.add_argument("--repo_name", help="要建立的 Repository 名稱")
    parser.add_argument("--manager_email", help="Project Manager 的 Email (多個請用逗號分隔)")
    parser.add_argument("--member_email", help="Project Member 的 Email (多個請用逗號分隔)")
    
    # modify_member 專用參數 (保留擴充性)
    parser.add_argument("--group_type", help="目標群組類型")
    parser.add_argument("--users", help="使用者 Email (多個請用逗號分隔)")
    parser.add_argument("--action", choices=["add", "remove"], default="add", help="執行的動作 (add/remove)")

    args = parser.parse_args()

    # 從環境變數獲取連線資訊
    org_url = os.getenv("ADO_ORG_URL")
    pat = os.getenv("ADO_PAT")

    print("=" * 60)
    print("🔥 模式: [REAL EXECUTION]")
    print(f"🚀 啟動 Runbook: {args.runbook_name}")
    print(f"📂 目標專案: {args.project_name}")
    print("=" * 60)

    if not org_url or not pat:
        print("❌ 錯誤：找不到環境變數 ADO_ORG_URL 或 ADO_PAT")
        sys.exit(1)

    client = AsgardClient(org_url, pat)

    if args.runbook_name == "create_project":
        runbook = CreateProjectRunbook(client)
        
        # 處理 Email 清單
        managers = [e.strip() for e in args.manager_email.split(",")] if args.manager_email else []
        members = [e.strip() for e in args.member_email.split(",")] if args.member_email else []
        
        report = runbook.execute(
            project_name=args.project_name,
            repo_name=args.repo_name,
            managers=managers,
            members=members
        )
    
    elif args.runbook_name == "modify_member":
        runbook = ModifyMemberRunbook(client)
        
        if not args.group_type or not args.users:
            print("❌ 錯誤：modify_member 需要 --group_type 與 --users 參數")
            sys.exit(1)
            
        users_list = [e.strip() for e in args.users.split(",")]
        report = runbook.execute(
            project_name=args.project_name,
            group_type=args.group_type,
            users=users_list,
            action=args.action
        )
    
    else:
        print(f"❌ 錯誤：不支援的 Runbook 名稱: {args.runbook_name}")
        sys.exit(1)

    # 輸出結果
    print("-" * 60)
    if report.get("status") == "success":
        print(f"✅ Runbook '{args.runbook_name}' 執行成功！")
        if "steps" in report:
            for step in report["steps"]:
                print(f"  - [{step['step']}]: {step['result']}")
        print("=" * 60)
    else:
        print(f"❌ 執行失敗: {report.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()

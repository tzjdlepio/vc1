import os
from asgard.client import AsgardClient
from asgard.projects import ProjectManager
from asgard.repos import RepoManager
from asgard.members import MemberManager

def main():
    # 1. 初始化 Client (會自動讀取 .env)
    # 你也可以手動傳入：client = AsgardClient(org_url="...", pat="...")
    try:
        client = AsgardClient()
        project_mgr = ProjectManager(client)
        repo_mgr = RepoManager(client)
        member_mgr = MemberManager(client)

        print("--- Azure DevOps Asgard Demo ---")

        # 2. 列出所有專案
        projects = project_mgr.list_projects()
        print(f"Found {len(projects)} projects.")
        for p in projects:
            print(f"- {p['name']} ({p['id']})")

        if projects:
            target_project = projects[0]
            p_name = target_project['name']
            p_id = target_project['id']

            # 3. 列出該專案下的 Repos
            repos = repo_mgr.list_repos(p_name)
            print(f"\nRepos in {p_name}:")
            for r in repos:
                print(f"  - {r['name']}")

            # 4. 列出專案成員
            members = member_mgr.list_project_members(p_id)
            print(f"\nMembers in {p_name}:")
            for m in members:
                identity = m.get('identity', {})
                print(f"  - {identity.get('displayName')} ({identity.get('uniqueName')})")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

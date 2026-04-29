import os
from typing import List, Dict, Any
from asgard import AsgardClient, MemberManager

class ModifyMemberRunbook:
    def __init__(self, client: AsgardClient):
        self.members = MemberManager(client)
        self.dry_run = os.getenv("ASGARD_DRY_RUN", "false").lower() == "true"

    def execute(self, project_name: str, group_type: str, users: List[str], action: str = "add") -> Dict[str, Any]:
        """
        ## modify_member runbook
        支援 Dry Run 模式
        """
        if self.dry_run:
            print(f"\n[DRY RUN] 👥 模擬修改成員: {project_name} | 群組: {group_type} | 動作: {action}")
            return {"status": "simulated_success", "mode": "dry_run", "processed": users}

        groups = self.members.find_groups(project_name)
        target_group = groups.get(group_type)
        if not target_group:
            return {"status": "failed", "error": f"Group type '{group_type}' not found."}

        results = {"status": "success", "processed": []}
        for user in users:
            if action == "add":
                self.members.add_user_to_group(user, target_group)
            else:
                self.members.remove_user_from_group(user, target_group)
            results["processed"].append(user)
        return results

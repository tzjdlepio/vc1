import os
from typing import List, Dict, Any
from asgard import AsgardClient, MemberManager

class ModifyMemberRunbook:
    def __init__(self, client: AsgardClient):
        self.members = MemberManager(client)

    def execute(self, project_name: str, group_type: str, users: List[str], action: str = "add") -> Dict[str, Any]:
        """
        ## modify_member runbook
        執行真實成員修改流程。
        """
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

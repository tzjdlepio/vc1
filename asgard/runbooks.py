from typing import List, Dict, Any
from .client import AsgardClient
from .projects import ProjectManager
from .repos import RepoManager
from .members import MemberManager
from .pipelines import PipelineManager

class AsgardRunbooks:
    def __init__(self, client: AsgardClient):
        self.projects = ProjectManager(client)
        self.repos = RepoManager(client)
        self.members = MemberManager(client)
        self.pipelines = PipelineManager(client)

    def create_project_runbook(self, 
                                project_name: str, 
                                managers: List[str] = None, 
                                members: List[str] = None,
                                template_repo_id: str = None,
                                template_path: str = "azure-pipelines.yml") -> Dict[str, Any]:
        """
        ## create_project runbook
        -> 預檢查 (專案是否存在 & Repo 名稱是否與專案名稱相同)
        -> 建立 Project
        -> 建立 Repo
        -> 將專案名下的 Repo 都設定大小為 5MB
        -> 將 pipeline.yml 複製到 repo 之中(路徑: pipelines/main.yml)
        -> 將上述的 yaml 檔案建立成 build 
        --> 建立 [develop, uat, master, hotfix] 的 branch 
        ---> 建立這些 branch 的 br_policy
        --> 將對應人員加進 "ProjectManager" 與 "ProjectMember" 的群組中
        """
        results = {"status": "success", "steps": []}

        # 1. 預檢查
        if self.projects.exists_project(project_name):
            results["status"] = "failed"
            results["error"] = f"Project '{project_name}' already exists."
            return results

        # 2. 建立 Project
        project_op = self.projects.create_project(project_name)
        results["steps"].append({"step": "create_project", "result": project_op})
        
        # 註：專案建立是異步的，這裡假設已經建立完成或後續 API 會等待。
        # 實作中可能需要 polling operation status。
        
        # 3. 建立 Repo (預設通常會建立一個同名的，但明確建立以符合需求)
        repo = self.repos.create_repo(project_name, project_name)
        repo_id = repo["id"]
        results["steps"].append({"step": "create_repo", "result": repo})

        # 4. 設定 repo 大小為 5MB
        size_limit = self.repos.set_repo_size_limit(repo_id, limit_mb=5)
        results["steps"].append({"step": "set_size_limit", "result": size_limit})

        # 5. 複製 pipeline.yml
        # 從 template 取得內容 (假設從另一個 repo 取得)
        if template_repo_id:
            yml_content = self.repos.get_file_content(project_name, template_repo_id, template_path)
        else:
            yml_content = "# Sample Pipeline\npool:\n  vmImage: 'ubuntu-latest'\nsteps:\n- script: echo Hello Asgard!"
        
        push = self.repos.push_file_content(
            project_name, repo_id, "pipelines/main.yml", yml_content, "main", "Add pipeline.yml"
        )
        results["steps"].append({"step": "push_pipeline_yml", "result": push})

        # 6. 建立 Build
        pipeline = self.pipelines.create_pipeline_from_yml(
            project_name, f"{project_name}-CI", repo_id, "/pipelines/main.yml"
        )
        results["steps"].append({"step": "create_pipeline", "result": pipeline})

        # 7. 建立 Branches [develop, uat, master, hotfix]
        branches = ["develop", "uat", "master", "hotfix"]
        for br in branches:
            self.repos.create_branch(project_name, repo_id, br)
            # 8. 設置分支 Policy
            self.repos.set_branch_policy(project_name, repo_id, f"refs/heads/{br}")
        results["steps"].append({"step": "create_branches_and_policies", "branches": branches})

        # 9. 將人員加入群組
        groups = self.members.find_groups(project_name)
        if managers and "ProjectManager" in groups:
            for m in managers:
                self.members.add_user_to_group(m, groups["ProjectManager"])
        if members and "ProjectMember" in groups:
            for m in members:
                self.members.add_user_to_group(m, groups["ProjectMember"])
        results["steps"].append({"step": "assign_members", "groups_found": list(groups.keys())})

        return results

    def modify_member_runbook(self, project_name: str, group_type: str, users: List[str], action: str = "add") -> Dict[str, Any]:
        """
        ## modify_member runbook
        將對應人員加進或移除 "ProjectManager" 與 "ProjectMember" 的群組中
        """
        groups = self.members.find_groups(project_name)
        target_group = groups.get(group_type)
        
        if not target_group:
            return {"status": "failed", "error": f"Group type '{group_type}' not found for project '{project_name}'."}

        results = {"status": "success", "processed": []}
        for user in users:
            if action == "add":
                self.members.add_user_to_group(user, target_group)
            else:
                self.members.remove_user_from_group(user, target_group)
            results["processed"].append(user)
            
        return results

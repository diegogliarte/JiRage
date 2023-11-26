import os

from jira import JIRA


class JiraService:

    def __init__(self):
        basic_auth = (os.environ.get("JIRA_EMAIL"), os.environ.get("JIRA_API_TOKEN"))
        self.jira = JIRA("https://diegogliarte.atlassian.net", basic_auth=basic_auth)

    def post_issue(self, summary, description, issue_type, priority):
        issue_dict = {
            'project': {'id': 10000},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type},
            'priority': {'name': priority},
        }

        return self.jira.create_issue(fields=issue_dict)

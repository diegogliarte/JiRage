import json
import logging
import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

from jira_service import JiraService
from prompter_service import PrompterService

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return "Hello World!"


@app.route('/create_issue', methods=['POST'])
def create_issue():
    data = request.json
    user_input = data.get("user_input")

    if not user_input:
        return jsonify({"error": "No user input provided"}), 400

    prompter = PrompterService()
    response = prompter.prompt(user_input)

    try:
        response_dict = json.loads(response)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid response format"}), 500

    # jira = JiraService()
    # issue = jira.create_issue(
    #     summary=response_dict["summary"],
    #     description=response_dict["description"],
    #     issue_type=response_dict["issue_type"],
    #     priority=response_dict["priority"],
    # )
    #
    # issue = {
    #     'project': {'id': 10000},
    #     'summary': "Page crashes when submitting form on mobile and desktop versions",
    #     'description': "Every time I try to submit my form, the page crashes on both the mobile and desktop versions of the website. This issue has been consistently occurring and is a major hindrance to user experience.",
    #     'issuetype': {'name': "Bug"},
    #     'priority': {'name': "Low"},
    # }

    return jsonify({"message": "Jira issue created successfully", "issue": response_dict}), 200


@app.route('/post_issue', methods=['POST'])
def post_issue():
    data = request.json
    issue_dict = data.get("issue_dict")

    if not issue_dict:
        return jsonify({"error": "No issue_dict provided"}), 400

    jira = JiraService()
    jira.post_issue(
        summary=issue_dict["summary"],
        description=issue_dict["description"],
        issue_type=issue_dict["issue_type"],
        priority=issue_dict["priority"],
    )

    return jsonify({"message": "Jira issue created successfully"}), 201


if __name__ == "__main__":
    load_dotenv()
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000))

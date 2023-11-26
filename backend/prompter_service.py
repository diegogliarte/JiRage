import os

from openai import OpenAI


class PrompterService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def prompt(self, user_input):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
Analyze the following user feedback and structure the information for creating a Jira ticket. The analysis should include:

1. **Summary:** A concise summary of the issue or feature request.
2. **Description:** Detailed information about the feedback, including any specific details that are relevant.
3. **Issue Type:** Classify as 'Bug', 'Feature' or 'Improvement' based on whether it's a problem or a feature request.
4. **Priority:** Determine the priority (Highest, High, Medium, Low or Lowest) based on the urgency and impact.

User Feedback:
{user_input}
""" + """
Format the response as a JSON object with keys 'summary', 'description', 'issue_type', and 'priority'. Example format:
{
  "summary": "Example summary",
  "description": "Example description",
  "issue_type": "Bug",
  "priority": "High"
}
"""
                }
            ],
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
        )

        return chat_completion.choices[0].message.content

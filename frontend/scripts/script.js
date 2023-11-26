let currentIssue = null; // Global variable to store the current issue

function submitFeedback() {
    var userInput = document.getElementById("userInput").value;
    var successCard = document.getElementById("successCard");
    var issueSummary = document.getElementById("issueSummary");
    var issueDescription = document.getElementById("issueDescription");

    fetch('http://localhost:5042/create_issue', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({user_input: userInput})
    })
        .then(response => response.json())
        .then(response => {
            console.log('Success:', response);
            let issue = response["issue"]
            currentIssue = issue;
            issueSummary.textContent = issue["summary"]
            issueDescription.textContent = issue["description"]

            let issueTypeElement = document.getElementById("issueType");
            let issueType = issue["issue_type"];
            issueTypeElement.textContent = issueType
            issueTypeElement.className = ''; // Reset class
            issueTypeElement.classList.add(`issue-${issueType.toLowerCase()}`);

            let issuePriorityElement = document.getElementById("issuePriority");
            let issuePriority = issue["priority"];
            issuePriorityElement.textContent = issuePriority;
            issuePriorityElement.className = ''; // Reset class
            issuePriorityElement.classList.add(`priority-${issuePriority.toLowerCase()}`);

            successCard.style.display = "block";
        })
        .catch((error) => {
            console.error('Error:', error);
            successCard.style.display = "none";
            alert("An error occurred while submitting feedback.");
        });
}

function postIssue() {
    if (!currentIssue) {
        alert("No issue to post");
        return;
    }

    fetch('http://localhost:5042/post_issue', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({issue_dict: currentIssue})
    })
        .then(response => response.json())
        .then(data => {
            console.log('Issue Posted:', data);
            alert("Issue posted successfully!");
            currentIssue = null;
            document.getElementById("successCard").style.display = "none";
            document.getElementById("userInput").value = "";
        })
        .catch((error) => {
            console.error('Error:', error);
            alert("An error occurred while posting the issue.");
        });
}


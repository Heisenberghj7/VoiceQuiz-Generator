from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage('token.json')
creds = None
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
    creds = tools.run_flow(flow, store)

form_service = discovery.build('forms', 'v1', http=creds.authorize(
    Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

questions = []
options = []
answers = []

# Read the text file
with open('ChatGPT_Answer.txt', 'r') as file:
    # Read the lines
    lines = file.readlines()
    
    # Iterate over the lines
    for line in lines:
        # Strip leading/trailing whitespaces and newline characters
        line = line.strip()
        
        # Check if the line is empty
        if not line:
            continue
        
        # Check if it's a question
        if line.startswith(str(len(questions) + 1) + '.'):
            # Extract the question and append it to the questions list
            question = line.split('.', 1)[1].strip()
            questions.append(question)
        
        # Check if it's an answer line
        elif line.startswith('Answer:'):
            # Extract the answers and append them to the answers list
            answer = line.split(':', 1)[1].strip().split(' and ')
            answers.append(answer)
        
        # Otherwise, it's an option line
        else:
            # Extract the option and append it to the options list
            option = line.strip()
            options.append(option)

# Print the lists
print("Questions:", questions)
print("Options:", options)
print("Answers:", answers)

# Request body for creating a form
NEW_FORM = {
    "info": {
        "title": "Quiz",
    }
}

# Creates the initial form
result = form_service.forms().create(body=NEW_FORM).execute()

# Request body to add a multiple-choice question
update = {
        "requests": [
            {
                "updateSettings": {
                    "settings": {
                        "quizSettings": {
                            "isQuiz": True
                        }
                    },
                    "updateMask": "quizSettings.isQuiz"
                }
            }
        ]
    }
for i in range(len(questions)):
    NEW_QUESTION = {
        "requests": [{
            "createItem": {
                "item": {
                    "title": questions[i],
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [{"value": j} for j in options[i]],
                                "shuffle": True
                            }
                        }
                    },
                },
                "location": {
                    "index": 0
                }
            }
        }]
    }



    # Adds the question to the form
    question_setting = form_service.forms().batchUpdate(formId=result["formId"], body=NEW_QUESTION).execute()

    # Prints the result to show the question has been added
get_result = form_service.forms().get(formId=result["formId"]).execute()
print(get_result)


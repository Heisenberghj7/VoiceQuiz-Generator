from __future__ import print_function
import re
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

def Quiz(s_file):
    
    store = file.Storage(s_file)
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
        creds = tools.run_flow(flow, store)

    form_service = discovery.build('forms', 'v1', http=creds.authorize(
        Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

    questions = []
    options = []
    answers = []

    # Read the text file
    with open('ChatGPT_Answer.txt', 'r') as f_file:
        # Read the lines
        lines = f_file.readlines()
        quest = re.compile(r'^\d+(?:\)|\.|\-)(.+\?$)')
        opt = re.compile(r'^[a-zA-Z](?:\)|\.|\-)(.+$)')
        ans = re.compile(r'Answer:\s([a-zA-Z])')

        current_question = None
        current_options = []

        # Iterate over the lines
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespaces

            if line:
                if quest.match(line):
                    if current_question:
                        questions.append(current_question)
                        options.append(current_options)
                        current_options = []

                    current_question = line

                if opt.match(line):
                    current_options.append(line)

                if ans.match(line):
                    answers.append(ans.match(line).group(1))

        # Add the last question and its options
        if current_question:
            questions.append(current_question)
            options.append(current_options)

    # Verify that the three lists have the same length
    assert len(questions) == len(options) == len(answers)

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
                        "title": questions[len(questions)-1-i],
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [{"value": option} for option in options[len(questions)-1-i]],
                                    "shuffle": False
                                }
                            },
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
    return get_result['responderUri']


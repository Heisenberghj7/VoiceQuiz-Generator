import openai

with open("openai_key.txt",'r') as f:
    openai.api_key=f.readline()

message_history = []

def chat(file, role="user"):
    content=""
    with open(file,'a') as f:
       f.write("\nthe Quiz should be written in the following format:\n(number)(- or .)Question\n(numbers or letters))Options\n'(numbers or letters)Answer:'")
    with open(file,'r') as f:
       input_text= f.readlines()
       for text in input_text:
           content+=text
    message_history.append({"role": role, "content": f"{content}"})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )
    reply_content = completion.choices[0].message.content
    message_history.append({"role": "assistant", "content": f"{reply_content}"})
    return reply_content

# if __name__ == '__main__':
def chatAnswer(file1,mode):
    with open(file1, mode) as f:
      f.write(chat('transcript.txt'))
    
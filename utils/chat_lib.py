import json, time

# return content of file messages.json as JSON object
def getHistory(file_name):
    data = []
    # Open the existing file and read its content
    try:
        with open(file_name, 'r') as json_file:
            # Check if file is empty
            try:
                data = json.load(json_file)  # Load existing data
            except json.JSONDecodeError:
                data = []  # If file is empty or invalid, start with an empty list
    except FileNotFoundError:
        data = []  # If file does not exist, start with an empty list
    
    if not isinstance(data, list):
        data = [] # If file is empty or invalid, start with an empty list
    
    return data

# add message to file messages.json and return the file content as JSON object
def appendMessage(payload):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    user = payload['user']
    content = payload['content']
    payload['timestamp'] = timestamp
    print(f'({timestamp}) Message from {user} received: {content}')

    file_name = 'messages.json'
    data = getHistory(file_name)
    data.append(payload)
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)  # Write updated data back to the file

    return data


def appendUser(user):
  file_name = 'userdata.json'
  data = getHistory(file_name) # reuse function for messages
  data.append(user)

  with open(file_name, 'w') as file:
    json.dump(data, file, indent=4)  # Write updated data back to the file

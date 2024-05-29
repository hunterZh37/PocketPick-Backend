import json


def load_previous_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def detect_changes(new_file, old_file):
    new_entries = [entry for entry in new_file if entry not in old_file]
    return new_entries

def save_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def notify_changes(changes):
    if changes:
        print("New entries detected:")
        for change in changes:
            print(change)

def convert_to_dict(headers,data): 
    return dict(zip(headers, data))
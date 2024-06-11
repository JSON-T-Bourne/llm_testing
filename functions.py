from gpt4all import GPT4All
from datetime import date
import os
import re
import ollama
from ollama import Client

def ollama_chat(prompt, model = "llama3"):
    client = Client(host='http://localhost:11434')
    response = client.chat(model='llama3', messages=[
      {
        'role': 'user',
        'content': prompt,
      },
    ])
    return response["message"]["content"]


def get_ollama_models():
    list_of_ollama_models = []
    ollama_models = ollama.list()
    for num in range(len(ollama_models["models"])):
        list_of_ollama_models.append(ollama_models["models"][num]["name"][:-7])
    return list_of_ollama_models

def clean_string0(s):
    # Remove everything up to the first capital letter
    s = re.sub(r'^.*?([A-Z])', r'\1', s)
    # Remove everything after the last punctuation mark (., !, ?)
    s = re.sub(r'([.!?]).*$', r'\1', s)
    return s

def process_text0(text):
    try:
        start_pattern = r'\['
        end_pattern = r'\]'
        alt_end_pattern = r'\.'
        
        start_match = re.search(start_pattern, text, re.DOTALL)
        text = text[start_match.start(0):]
        text = text[::-1]
        end_matches = re.search(end_pattern, text, re.DOTALL)
        print(end_matches)
        if end_matches == None:
            end_matches = re.search(alt_end_pattern, text, re.DOTALL)
            print(end_matches)
        text = text[end_matches.start(0):]
        text = text[::-1]
        quest_list = text.split("', '")
        clean_quests = []
        for quest in quest_list:
            new_string = clean_string(quest)
            clean_quests.append(new_string)
        return clean_quests
    except:
        print(text)
def clean_string(s):
    s = re.sub(r"^.*?([A-Z])", r"\1", s)
    s = re.sub(r"([.!?]).*$", r"\1", s)
    return s

def process_text(text):
    try:
        pattern = r"\[.*\]"
        match = re.search(pattern, text, re.DOTALL)
        quest_list = match.group(0).split("\n")
        clean_quests = []
        for quest in quest_list:
            new_string = clean_string(quest)
            clean_quests.append(new_string)
    except:

        start_pattern = r'\['
        start_match = re.search(start_pattern, text, re.DOTALL)
        end_pattern = r'[\]\n]'
        end_matches = re.search(end_pattern, text, re.DOTALL)
        text = text[start_match.start():end_matches.start()]
        quest_list = text.split(",")
        clean_quests = []
        for quest in quest_list:
            new_string = clean_string(quest)
            clean_quests.append(new_string)
        return clean_quests

    return clean_quests

def chat_response(model_name, prompt, system_prompt, temp=0.9):
    """

    """
    model = GPT4All(model_name, allow_download=False)
    with model.chat_session(system_prompt=system_prompt):
        return model.generate(prompt=prompt, temp=temp, max_tokens=3950)

def save_dataframe_to_csv(df, model_name, folder='saved_responses'):
    # Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Get today's date
    today_date = date.today().strftime('%Y-%m-%d')
    
    # Initial filename
    base_filename = f"{today_date}_{model_name}.csv"
    file_path = os.path.join(folder, base_filename)
    
    # Check if file already exists and adjust filename if necessary
    if os.path.exists(file_path):
        # Get list of files in the folder
        existing_files = os.listdir(folder)
        
        # Filter files that match the date pattern and are CSV files
        matching_files = [f for f in existing_files if f.startswith(today_date) and f.endswith('.csv')]
        
        # Determine the new filename with incremented number
        new_filename = f"{today_date}_{model_name}-{(len(matching_files)-1)}.csv"
        file_path = os.path.join(folder, new_filename)
    
    # Save the DataFrame to CSV
    df.to_csv(file_path, index=False)
    print(f"DataFrame saved as {file_path}")

# Example usage:
#save_dataframe_to_csv(df)

def list_to_string(string_list):
    """

    """ 
    output_string = ""
    for item in string_list:
        output_string = output_string + "\n" + item

    return output_string
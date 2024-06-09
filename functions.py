from gpt4all import GPT4All
from datetime import date
import os
import re

def clean_string(s):
    s = re.sub(r"^.*?([A-Z])", r"\1", s)
    s = re.sub(r"([.!?]).*$", r"\1", s)
    return s

def process_text(text):
    pattern = r"\[.*\]"
    match = re.search(pattern, text, re.DOTALL)
    quest_list = match.group(0).split("\n")
    clean_quests = []
    for quest in quest_list:
        new_string = clean_string(quest)
        clean_quests.append(new_string)

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
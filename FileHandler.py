import os

# Define the fixed path to the folder where files will be stored
folder_path = "E:\\Uni(worst)y\\7th Semester\\Cyber Security\\Project\\GuardianVault\\Notes"


# Function to create a text file and write data to it
def create_text_file(file_name, data):
    file_path = os.path.join(folder_path, file_name)
    try:
        with open(file_path, 'w') as file:
            file.write(data)
        return True
    except IOError as e:
        return False
    

def find_files_for_email(email):
    email_files = []
    print("func ",email)
    # Ensure the folder path exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return email_files
    
    # Split the email address to get the username
    email_username = email.split("@")[0]
    print("func ",email_username)
    # Iterate through files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if "_" in file:
                parts = file.split("_")
                file_username = parts[0]  # Extract the username part from the filename
                if email_username == file_username:
                    file_path = os.path.join(root, file)
                    email_files.append(file_path)
    
    return email_files

def display_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"File '{file_path}' not found."

def delete_files_for_email(email):
    try:
        email_files = []
        # Ensure the folder path exists
        if not os.path.exists(folder_path):
            print(f"The folder '{folder_path}' does not exist.")
            return email_files
        
        # Split the email address to get the username
        email_username = email.split("@")[0]
        
        # Iterate through files in the folder
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if "_" in file:
                    parts = file.split("_")
                    file_username = parts[0]  # Extract the username part from the filename
                    if email_username == file_username:
                        file_path = os.path.join(root, file)
                        email_files.append(file_path)
                        # Delete the file
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
        
        return email_files  # Return the list of deleted files

    except Exception as e:
        print(e)
        return email_files  # Return the list of deleted files, even if some deletion operations failed

import os

# Notes are stored in the "Notes" folder next to this file
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Notes")


# Function to create a text file and write data to it
def create_text_file(file_name, data):
    file_path = os.path.join(folder_path, file_name)
    try:
        os.makedirs(folder_path, exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(data)
        return True
    except IOError as e:
        return False
    

def find_files_for_email(email):
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
            # Files are named <username>_<note name>
            if file.startswith(email_username + "_"):
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
                # Files are named <username>_<note name>
                if file.startswith(email_username + "_"):
                    file_path = os.path.join(root, file)
                    email_files.append(file_path)
                    # Delete the file
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
        
        return email_files  # Return the list of deleted files

    except Exception as e:
        print(e)
        return email_files  # Return the list of deleted files, even if some deletion operations failed

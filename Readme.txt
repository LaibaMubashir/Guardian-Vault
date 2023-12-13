 breakdown of each HTML and Python file in the GuardianVault project:

HTML Files:
index.html
Purpose: Represents the main page of the application after a successful login.
Features:
Displays options to add notes or view existing notes.
Likely contains placeholders for notes display and creation.

SignIn.html
Purpose: Provides a form for user login.
Features:
Contains input fields for email and password.
Offers links for password recovery and user registration.

SignUp.html
Purpose: Presents a form for user registration.
Features:
Includes fields for full name, email, password, and confirmation password.

about.html
Purpose: Renders details about user notes.
Features:
Likely showcases the existing notes or prompts users to create new notes.

notes.html
Purpose: Represents a page where users can write and save notes.
Features:
Contains input fields for note titles and text content.
Provides a form to create and save notes.

Python Files:
app.py
Purpose: Implements the Flask application and defines various routes for user authentication, note handling, and rendering HTML templates.

crypto.py
Purpose: Contains functions for encrypting and decrypting text using a Caesar cipher.
file_handler.py

Purpose: Handles file operations such as file creation, deletion, and retrieval within a specified directory.

DBHandle.py
Purpose: Contains a DBHandler class responsible for executing database operations using pymysql.

Each HTML file represents a different view or functionality within the application, while the Python files handle backend logic, database interactions, and encryption/decryption operations. Together, they form the GuardianVault application, encompassing user authentication, note management, and file handling functionalities.
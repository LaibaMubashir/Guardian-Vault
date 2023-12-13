#Guardian Vault-BITF20M025 & BITF20M020
from flask import Flask,render_template,request,session
from DBHandle import DBHandler
from crypto import caesar_encrypt,caesar_decrypt
import FileHandler 
app=Flask(__name__)
app.secret_key="bsjvhusdhg5565645"
app.config["SESSION_TYPE"]="filesystem"
app.config["SESSION_PERMANENT"]=False

key = 5

@app.route('/')
def sIn():
    return  render_template("SignIn.html")

@app.route('/submitSignInForm', methods=["POST"])
def submitSignInForm():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        email=caesar_encrypt(email,key)
        password=caesar_encrypt(password,key)
        print("Encrypted text:", email)

        dbHandle=DBHandler("localhost","root","LM@282003!","guardianvault")

        found=dbHandle.login(email,password)
        if found:
            session['email']=email
            return render_template("index.html")
        else:
            return  render_template("SignIn.html" , message="Email or Password is Incorrect")

@app.route('/signUp')
def sUp():
    return  render_template("SignUp.html")

@app.route('/submitSignUpForm', methods=["POST"])
def submitSignUpForm():
    if request.method == "POST":
        name=request.form["FName"]
        email = request.form["email"]

        encrypted_email = caesar_encrypt(email,key)

        print("Plaintext:", email)
        print("Encrypted text:", encrypted_email)


        password = request.form["password"]
        conPassword=request.form["conPassword"]

        if len(password) >=8 and len(conPassword) >=8 :
            if password ==  conPassword:
                dbHandle=DBHandler("localhost","root","LM@282003!","guardianvault")

                encrypted_pass = caesar_encrypt(password,key)

                print("Plaintext:", password)
                print("Encrypted text:", encrypted_pass)    
                
                user=[name, encrypted_email,encrypted_pass]

                inserted=dbHandle.signUp(user)
                if inserted:
                    session['email']=email
                    return render_template("index.html")
                else:
                    return  render_template("SignIn.html" , message="Email Already Exist")
            else:
                return  render_template("SignIn.html" , message="Password not Match")
        else:
            return  render_template("SignIn.html" , message="Password must be at least 8 characters long")

@app.route('/Home', methods=['GET', 'POST'])
def new_page():
    email = session.get('email')
    if email:
        return render_template('index.html')
    else:
        return render_template("SignIn.html",message="Log In First")

@app.route('/Note')
def note():
    email = session.get('email')
    if email:
        return render_template('notes.html')
    else:
        return render_template("SignIn.html",message="Log In First")

    
@app.route('/NewNote', methods=['POST'])
def newNote():
    try:
        email = session.get('email')

        if email:
            noteName=request.form["notesname"]
            dbHandle=DBHandler("localhost","root","LM@282003!","guardianvault")
            parts = email.split("@")
            filename=parts[0]+"_"+noteName
            note_input=request.form["noteInput"]
            note_input=caesar_encrypt(note_input,key)
            result=FileHandler.create_text_file(filename,note_input)
            if result:
                print(f"File '{filename}' created successfully with the given data.")
                inserted=dbHandle.enterNoteName(email,noteName)
                if inserted:
                    return render_template("index.html")
            else:
                print(f"An error occurred while creating the file: {e}")
    except Exception as e :
        return render_template("index.html")

@app.route('/MyNotes')
def mynotes():
    try:
        email = session.get('email')
        if email:
            allfiles=FileHandler.find_files_for_email(email)
            dbHandle=DBHandler("localhost","root","LM@282003!","guardianvault")
            files=dbHandle.get_note_names_for_user(email)
            content=[]
            for file in allfiles:
                content.append(caesar_decrypt(FileHandler.display_file_content(file),key))
        
            length=len(files)
            if(files!=[] and content!=[]):
                print("kjsadkajwd")
                return render_template('about.html',file=files,cont=content,leng=length)
            else:
                print("jkdkajwdg")
                return render_template('about.html',message="Create A New Note Right Now!",file=[])
        else:
            return render_template("SignIn.html",message="Log In First")
    except Exception as e :
        print(e)
        return render_template("index.html")


@app.route('/deleteNotes')
def delete():
    email = session.get('email')
    if email:
        dbHandle=DBHandler("localhost","root","LM@282003!","guardianvault")
        if(dbHandle.delete_all_notes_for_user(email) and FileHandler.delete_files_for_email(email)):
            return render_template('about.html',message="Create A New Note Right Now!",leng=0)


@app.route('/logout')
def logout():
    session.clear()
    return render_template('SignIn.html')
    
if __name__ == "__main__":
    app.run()
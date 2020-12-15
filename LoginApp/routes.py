from flask import Flask, render_template, redirect, url_for, request, session
import re
from datetime import datetime


def isCommonPassword(password):
    fcp=open('CommonPassword.txt','r')

    # Read the common password file and remove all newline characters
    commonPasswords = [s.strip() for s in fcp.readlines()]
    fcp.close()

    if password in commonPasswords:
        return True
    else:
        return False

app = Flask(__name__)
app.config['SECRET_KEY'] = ' supersecret key 2020'
email_text=""
flag_found=False
count=0

def validate_password(password):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{12,25}$"
    pattern = re.compile(reg)
    match = re.search(pattern, password)
    fcp=open('CommonPassword.txt','r')
    data=fcp.readlines()
    fcp.close()
    if match:
        return True
    else:
        return False
@app.route('/')
@app.route('/index.html')
def index():
    if 'visited' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', the_title='Console Wars: Xbox vs Playstation')
@app.route('/xbox.html')
def xbox():
    if 'visited' not in session:
        return redirect(url_for('login'))
    return render_template('xbox.html', the_title='Console Wars: Xbox Specs')
@app.route('/playstation.html')
def playstation():
    if 'visited' not in session:
        return redirect(url_for('login'))
    return render_template('playstation.html', the_title='Console Wars: Playstation Specs')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        f = open("database.txt", "a")
        tname = ""
        for sub in username.split(" "):
            tname = tname + "_" + sub
        if not validate_password(password):
            message = "Password does not match requirements"
            return render_template("register.html", error=message)
        else:
            f.write("%s %s %s\n" % (tname, email, password))
            f.close()
            return render_template("register.html", error="successfully registered")
    else:
            return render_template("register.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    global flag_found
    global email_text
    if request.method == 'POST':
        f = open("database.txt", "r")
        data = f.readlines()
        email_text=request.form['email']
        f.close()
        print("Email: ",request.form['email'])
        print("Password: ",request.form['password'])
        data = [x.split() for x in data]
        print(data)
        for item in data:
            #item=item.split()
            print(item[1])
            print(item[2])
            if email_text == item[1].strip() and request.form['password'] == item[2].strip():
                print("TREEEE")
                flag_found=True
                break
            else:
                flag_found=False
        if(flag_found==True):
            session['visited'] = True
            print("TRUEEEEEE")
            return redirect(url_for('index'))
        else:
             error = "wrong credentials"
             return render_template("login.html", error=error)


    else:
        return render_template("login.html")
@app.route('/changepassword',methods=['GET','POST'])
def changepassword():
    count=0
    str_data =""
    replecedText=""
    global email_text
    print("Email Text: ",email_text)
    if 'visited' in session:
        if request.method=='POST':
            email=session['visited']
            new_password=request.form['new_password']
            if not validate_password(new_password):
                message="Password doesnot match requirements"
                return render_template("changepassword.html",error=message,email_text=email_text)
            fcp=open('CommonPassword.txt','r')
            data=fcp.readlines()
            fcp.close()
            for item in data:
                if request.form['new_password']==item.strip():
                    return render_template("changepassword.html",error="Please type another password. This password is most commnly used or compromised")

                file1= open("database.txt",'r')
                Data1=file1.readlines()
                print("Data1 = ", Data1[1])
                file1.close()

                fdpin=open("database.txt","r")
                for line in fdpin:
                    text = line.split(" ")
                    # return text[0]+text[1]+text[2]
                    print("comp Text:",text[1]," GetText: ",email_text)
                    if text[1].strip() == email_text.strip():
                        replecedText = line.replace(text[2], new_password)
                        del Data1[count]
                        Data1.append(replecedText)
                        print("Count: ",count)
                    print("Data1 New:",Data1)
                    count=count+1
                fdpin.close()
                fdpout = open("database.txt", "w")
                for item1 in Data1:
                    fdpout.write(item1.strip()+"\n")
                #fdpout.write(replecedText)
                fdpout.close()
                return render_template("changepassword.html", error="Password changed successfully")
            else:
                return render_template("index.html")
        return render_template("login.html",error="Please login first to access this page")
@app.route('/logout',methods=["GET","POST"])
def logout():
    """End the current user session"""
    session.clear()
    return render_template("login.html")
@app.route('/chngpass',methods=["GET","POST"])
def chngPass():
    global email_text
    return render_template("changepassword.html",email_text=email_text)
if __name__ == '__main__':
    app.run()
import random
import time
from flask import Flask, flash, jsonify, make_response, redirect, render_template, request, session, url_for
import os
import sys
import pymongo
from werkzeug.utils import secure_filename
import jwt
sys.path.insert(0, 'D:\\fyp\\saif fyp')
from Code import TexttoSpeech

USERS = {
  "jon@doe.com" : "123456"
}
JWT_KEY = "YOUR-SECRET-KEY"
JWT_ISS = "YOUR-NAME"
JWT_ALGO = "HS512"

# *** Backend operation

# WSGI Application
# Defining upload folder path
UPLOAD_FOLDER = os.path.join('uploads')
# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
app = Flask(__name__, template_folder='templates', static_folder='uploads')

# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'
object = TexttoSpeech()
#plot1 = object.convert()
#plot1_img = secure_filename("plot1.png")
#plot1.save(os.path.join(app.config['UPLOAD_FOLDER'], plot1_img))

count = 0
visited = []
client = pymongo.MongoClient("mongodb+srv://afrasyab:afra123@cluster0.d6xcmev.mongodb.net/?retryWrites=true&w=majority")
db = client["users"]
print(db)

def jwtSign(email):
  rnd = "".join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~!@#$%^_-") for i in range(24))
  now = int(time.time())
  return jwt.encode({
    "iat" : now,
    "nbf" : now,
    "exp" : now + 3600,
    "jti" : rnd, 
    "iss" : JWT_ISS,
    "data" : { "email" : email }
  }, JWT_KEY, algorithm=JWT_ALGO)

def jwtVerify(cookies):
  try:
    token = cookies.get("JWT")
    decoded = jwt.decode(token, JWT_KEY, algorithms=[JWT_ALGO])
    return True
  except:
    return False

@app.route("/login")
def login():
  if jwtVerify(request.cookies):
    return redirect(url_for("index"))
  else:
    return render_template("Login.html")


    
@app.route("/in", methods=["POST"])
def lin():
  data = dict(request.form)
  print(data)
  users = list(db['users'].find())
  index = 0
  for (i) in range(len(users)):
    valid = data["email"] in users[i]['email']
    index = i
    if valid:
      break
  if valid:
    if data["password"] == users[index]["password"]:
        valid = True
    else:
        valid = False 
  msg = "OK" if valid else "Invalid email/password"
  res = make_response(msg, 200)
  if valid:
    res.set_cookie("JWT", jwtSign(data["email"]))
  return res

@app.route("/up", methods=["POST"])
def sup():
  users = list(db['users'].find())
  data = dict(request.form)
  index = 0
  for (i) in range(len(users)):
    valid = data["email"] in users[i]['email']
    if(valid):
      break
    print(valid, data["email"] in users[i]['email'])
  if valid:
    res = make_response("User Already Exists", 200)
  else:
    print(data)
    db["users"].insert_one(data)
    res = make_response("OK", 200)
  return res



@app.route('/get_data', methods=("POST","GET"))
def StartTest():
    object.convert()
    processed_text=object.output
    print(processed_text)
    return render_template('Quiz.html', processed_text=processed_text)

@app.route('/quiz', methods=["POST"])
def Quiz():
    global count
    data = dict(request.form)
    print(int(data['Flag']))
    if(int(data['Flag']) == 1):
        object.count = (object.count + 1)
    print(object.count)
    res = make_response("OK", 200)
    return res

@app.route('/record', methods=["POST"])
def Record():
    object.convert()
    if(object.output.split(":")[-1].find("DAD") != -1 | object.output.split(":")[-1].find("dad") != -1):
      object.count += 1
    if(object.output.split(":")[-1].find("BAD") != -1 | object.output.split(":")[-1].find("bad") != -1):
      object.count += 1
    if(object.output.split(":")[-1].find("bid") != -1 ):
      object.count += 1
    if(object.output.split(":")[-1].find("did") != -1 ):
      object.count += 1
    if(object.output.split(":")[-1].find("cut") != -1 ):
      object.count += 1
    if(object.output.split(":")[-1].find("but") != -1 ):
      object.count += 1
    
    print(object.count)
    res = make_response("OK", 200)
    return res




@app.route('/')
def index():
    if jwtVerify(request.cookies):
        return render_template('index.html')
    else:
        return redirect(url_for("login"))

@app.route('/SignUp')
def Signup():
    #session['plot1'] = os.path.join(app.config['UPLOAD_FOLDER'], plot1_img)
    #print(session.get("plot1", None))
    return render_template('SignUp.html')

@app.route('/Quiz1')
def takeQuiz1():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz.html')
  else:
        return redirect(url_for("login"))

@app.route('/Quiz2')
def takeQuiz2():
  x = request.referrer
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz1.html')
  else:
      return redirect(url_for("login"))

@app.route('/Quiz3')
def takeQuiz3():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz2.html')
  else:
        return redirect(url_for("login"))

@app.route('/Quiz4')
def takeQuiz4():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz3.html')
  else:
        return redirect(url_for("login"))

@app.route('/Quiz5')
def takeQuiz5():   
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz4.html')
  else:
    return redirect(url_for("login"))

@app.route('/Quiz6')
def takeQuiz6():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz5.html')
  else:
    return redirect(url_for("login"))

@app.route('/Quiz7')
def takeQuiz7():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz6.html')
  else:
    return redirect(url_for("login"))
    
@app.route('/Quiz8')
def takeQuiz8():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz7.html')
  else:
    return redirect(url_for("login"))

@app.route('/Quiz9')
def takeQuiz9():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz8.html')
  else:
    return redirect(url_for("login"))

@app.route('/Quiz10')
def takeQuiz10():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz9.html')
  else:
    return redirect(url_for("login"))

@app.route('/Quiz11')
def takeQuiz11():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz10.html')
  else:
    return redirect(url_for("login"))

@app.route('/Quiz12')
def takeQuiz12():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz11.html')
  else:
    return redirect(url_for("login"))

@app.route('/Quiz13')
def takeQuiz13():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz12.html')
  else:
    return redirect(url_for("login"))

@app.route('/Quiz14')
def takeQuiz14():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz13.html')
  else:
    return redirect(url_for("login"))

@app.route('/Quiz15')
def takeQuiz15():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz14.html')
  else:
    return redirect(url_for("login"))

@app.route('/Quiz16')
def takeQuiz16():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Quiz15.html')
  else:
    return redirect(url_for("login"))


@app.route('/Result')
def takeResult():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  if jwtVerify(request.cookies):
    return render_template('Result.html', score=object.count)
  else:
    return redirect(url_for("login"))

@app.route("/out", methods=["POST"])
def lout():
  if(request.referrer == None ):
    return redirect(url_for("login"))
  res = make_response("OK", 200)
  res.delete_cookie("JWT")
  return res

if __name__ == '__main__':
    app.run(debug=True)



# @app.route('/upload', methods=("POST", "GET"))
# def uploadFile():
#     # print(app.config['UPLOAD_FOLDER'])
#     #if request.method == 'POST':
#     #    # Upload file flask
#     #    uploaded_img = request.files['uploaded-file']
#     #    # Extracting uploaded data file name
#     #    img_filename = secure_filename(uploaded_img.filename)
#         # Upload file to database (defined uploaded folder in static path)
#     #    uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
#         # Storing uploaded file path in flask session
#     #    session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
#     #    filepath = session.get('uploaded_img_file_path', None)
#     #    object.fileDialog(filepath)
#     return render_template('index.html')


# @app.route('/show_image')
# def displayImage():
#     # Retrieving uploaded file path from session
#     #img_file_path = session.get('uploaded_img_file_path', None)
#     # Display image in Flask application web page
#     return render_template('inner-page.html')


# @app.route('/plot1')
# def displayPlot1():
#     # Retrieving uploaded file path from session
#     # Display image in Flask application web page
#     #plot_file_path = session.get('plot1', None)
#     #text=object.output
#     #processed_text=text.upper()
#     return render_template('inner-page.html')




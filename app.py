#python -m flask run
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/recipes.html')
def recipes():
    return render_template('recipes.html')                        

@app.route('/login.html')
def login():
    return render_template('login.html')                        

@app.route('/signup.html')
def signup():
    return render_template('signup.html')  

@app.route('/recipes.json')
def recipesJSON():
    return render_template('recipes.json') 

@app.route('/login', methods=['POST'])
def dashboard():
   email = request.form['email']
   password = request.form['password']

   if email == "":
    return 'Please add a valid email address'
     
   elif password == "":
    return 'Please add a valid password'
   elif password !="james" or email!="rob_cutmore@hotmail.com":
    return "Invalid account details"
   else:
    return render_template('dashboard.html')                       



if __name__ == '__main__':
    app.debug = True
    app.run() #go to http://localhost:5000/ to view the page.
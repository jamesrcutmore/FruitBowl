#python -m flask run
import os
from flask import Flask, url_for, jsonify
from flask import render_template
from flask import request
from flask import redirect
from random import randint
from flask import  session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt


import json
app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'
app.config['MONGO_URI'] = os.getenv("MONGO_URI", "mongodb+srv://smoothie:sm00thieUser@cluster0.kuaea3o.mongodb.net/supersmoothie?retryWrites=true&w=majority")
mongo = PyMongo(app)

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/index.html')
def home():
   
    return render_template('index.html' )

@app.route('/login.html')
def login():
    if 'email' in session:
        return redirect(url_for('show_dashboard'))
    return render_template('login.html')                        

@app.route('/signup.html')
def signup():
    if 'email' in session:
        return redirect(url_for('show_dashboard'))
    return render_template('signup.html')  

@app.route('/recipes')
def recipes():
    recipes_data = mongo.db.recipes.find()
    return render_template('recipes.html', data={'recipes': recipes_data})  

@app.route('/users.json')
def usersJSON():
    return render_template('users.json') 


@app.route('/login', methods=['POST'])
def dashboard():
   if 'email' in session:
        return redirect(url_for('show_dashboard'))

   message = ''

   email = request.form['email']
   password = request.form['password']

   user_found = mongo.db.users.find_one({'email': email})

   if user_found:
    db_password =  user_found["password"]

    if bcrypt.checkpw(password.encode('utf-8'), db_password):
        session['admin'] = user_found['admin']
        session['firstname'] = user_found['firstname']
        session['email'] = user_found['email']

        return redirect(url_for('show_dashboard'))
    
    else:
        message = 'Invalid Password'
        return render_template('login.html', message=message)

   else:
    message = ' User not Found'
    return render_template('login.html',message = message)
     


@app.route('/deleteRecipe.html')
def delete_recipe():
   
    id = request.args['id']
    with open(app.root_path+'/templates/recipes.json') as f:
        print(id)
        recipes = json.load(f)
        newReceipes=[]
        for recipe in recipes:
            if int(recipe['id'])!=int(id):
                print(recipe['id'])
                newReceipes.append(recipe)
               
        with open(app.root_path+'/templates/recipes.json', "w") as jsonFile:
            json.dump(newReceipes, jsonFile)
    return "recipes deleted"
      
@app.route('/addrecipe', methods=['POST'])
def addrecipe():
    user_email = session['email']
    recipe_dict = request.form.to_dict()
    recipe_dict['user_email'] = user_email
    recipe_dict['ingredients'] = request.form.get("ingredients").split(',')
    recipe_dict['method'] = request.form.get("method").split(',')
    mongo.db.recipes.insert_one(recipe_dict)
    return redirect(url_for('recipes'))
    
    
@app.route('/dashboard')
def show_dashboard():
    if 'email' in session:
        user = {'email' : session['email'], 'admin':session['admin'],'firstname':session['firstname']}
        return render_template('dashboard.html',user = user)
    else:
        return redirect(url_for('dashboard'))

@app.route('/edit-recipe/<id>')
def edit_recipe(id):
   
    
    if 'email' in session:
        user = {'email' : session['email'], 'admin':session['admin'],'firstname':session['firstname']}
        recipeFound = mongo.db.recipes.find_one({"_id": ObjectId(id), 'user_email': user['email']})

        if recipeFound:
            return render_template('edit-recipe.html',recipe=recipeFound, user=user)
        else:
            return redirect(url_for('recipes'))
            
    else:
        return redirect(url_for('dashboard'))


@app.route('/signUp', methods=['POST'])
def signUpSubmit():
   message = ''

   surname = request.form['surname']
   firstname = request.form['firstname']
   email = request.form['email']
   password = request.form['password']
   cpassword = request.form['cpassword']
   admin = 0

   user_found = mongo.db.users.find_one({'email': email})

   if user_found:
    message = 'A User with this email already exists'
    return render_template('login.html', message=message)

   if password != cpassword:
        message = 'Password Not matching'
        return render_template('login.html', message=message)
   else:
        hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = {"firstname": firstname, "surname": surname, "email": email, "password": hash,"admin": admin}
        mongo.db.users.insert_one(new_user)
        user_data =  mongo.db.users.find_one({"email": email})

        session['admin'] = user_data['admin']
        session['firstname'] = user_data['firstname']
        session['email'] = user_data['email']

        return redirect(url_for('show_dashboard'))

   



@app.route('/editrecipe/<id>', methods=['POST'])
def editrecipe(id):
    newvalues = { "$set": { "title": request.form['title'],  'description' : request.form['description'], 'imageURL' : request.form['imageURL'],
    'ingredients':request.form.get("ingredients").split(','),
    'method': request.form.get("method").split(',') }}
    recipeFound = mongo.db.recipes.update_one({"_id": ObjectId(id)}, newvalues)
    return redirect('/recipes')
   
	
    

@app.route('/logout', methods=["POST", "GET"])
def logout():
    if 'email' in session:
        session.pop('email', None)
        session.pop('admin', None)
        session.pop('firstname', None)
        session.pop('user_id', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True
    app.run() #go to http://localhost:5000/ to view the page.
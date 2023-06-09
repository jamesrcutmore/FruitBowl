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
# app.config['MONGO_DBNAME'] = 'supersmoothie'
app.config['MONGO_URI'] = os.getenv("MONGO_URI", "mongodb+srv://smoothie:sm00thieUser@cluster0.kuaea3o.mongodb.net/supersmoothie?retryWrites=true&w=majority")
mongo = PyMongo(app)


@app.route('/')
def index():
    # user = {'email' : session['email'], 'admin':session['admin'],'firstname':session['firstname']}
    return render_template('index.html')

@app.route('/index.html')
def home():
    # user = {'email' : session['email'], 'admin':session['admin'],'firstname':session['firstname']}
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
    user = {'email' : session['email'], 'admin':session['admin'],'firstname':session['firstname']}
    recipes_data = mongo.db.recipes.find()
    return render_template('recipes.html', data={'recipes': recipes_data}, user=user)  

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
     
#    elif password == "":
#     return 'Please add a valid password'
#    with open(app.root_path+'/templates/users.json') as f:
#         users = json.load(f)
#         for user in users:
#             print(user)
#             if(user['email']==email and user['password']==password):
#                 session['id'] = user['id']
#                 session['admin'] = user['admin'] 
#                 return render_template('dashboard.html',user = user)                       
        
#         return "User not found."

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
                #app.logger.info('testing info log')
        with open(app.root_path+'/templates/recipes.json', "w") as jsonFile:
            json.dump(newReceipes, jsonFile)
    return "recipes deleted"
      
@app.route('/addrecipe', methods=['POST'])
def addrecipe():
    user_email = session['email']
    recipe_dict = request.form.to_dict()
    recipe_dict['user_email'] = user_email
    mongo.db.recipes.insert_one(recipe_dict)
    return redirect(url_for('recipes'))
    # newRecipe = {}
    # newRecipe.update({'title' : request.form['title']})
    # newRecipe.update({'description' : request.form['description']})
    # newRecipe.update({'imageURL' : request.form['imageURL']})
    # newRecipe.update({'id' : randint(0, 10000)})


    # for value in newRecipe.values():
	#     print(value)
    # with open(app.root_path+'/templates/recipes.json') as f:
    #     allRecipes = []
    #     recipes = json.load(f)
    #     for recipe in recipes:
    #         allRecipes.append(recipe)
    #     allRecipes.append(newRecipe)
    #     with open(app.root_path+'/templates/recipes.json', "w") as jsonFile:
    #         json.dump(allRecipes, jsonFile)
    #     return redirect("dashboard", code=303)
    
@app.route('/dashboard')
def show_dashboard():
    if 'email' in session:
        user = {'email' : session['email'], 'admin':session['admin'],'firstname':session['firstname']}
        return render_template('dashboard.html',user = user)
    else:
        return redirect(url_for('dashboard'))

@app.route('/edit-recipe/<id>')
def edit_recipe(id):
   
    # id = request.args['id']
    # with open(app.root_path+'/templates/recipes.json') as f:
    #     print(id)
    #     recipes = json.load(f)
    #     recipeFound = None
    #     for recipe in recipes:
    #         if int(recipe['id'])==int(id):
    #             recipeFound = recipe
            
    #     print(recipeFound)
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
#    if email == "":
#     return 'Please add a valid email address'
     
#    if password == "":
#     return 'Please add a valid password'
   
#    if firstname == "":
#     return 'Please add a valid First name'

#    if surname == "":
#     return 'Please add a valid Surname'

    
#    newUser = {}
#    newUser.update({'firstname' : firstname})
#    newUser.update({'surname' : surname})
#    newUser.update({'email' : email})
#    newUser.update({'password' : password})
#    newUser.update({'id' : randint(0, 10000)})
#    newUser.update({'admin' : admin})
   

#    with open(app.root_path+'/templates/users.json') as f:
       
#         allUsers = []
#         users = json.load(f)
#         for user in users:
#             allUsers.append(user)
#         allUsers.append(newUser)
#         print(allUsers)
#         with open(app.root_path+'/templates/users.json', "w") as jsonFile:
#          json.dump(allUsers, jsonFile)

#         return "signup completed."

@app.route('/editrecipe/<id>', methods=['POST'])
def editrecipe(id):
    newvalues = { "$set": { "title": request.form['title'],  'description' : request.form['description'], 'imageURL' : request.form['imageURL']} }
    recipeFound = mongo.db.recipes.update_one({"_id": ObjectId(id)},newvalues)
    return redirect('/recipes')
    # editRecipe = {}
    # editRecipe.update({'title' : request.form['title']})
    # editRecipe.update({'description' : request.form['description']})
    # editRecipe.update({'imageURL' : request.form['imageURL']})
    # editRecipe.update({'id' : request.form['id']})
    # editRecipe.update({'userid' :1})

    # for value in editRecipe.values():
	#     print(value)
    # with open(app.root_path+'/templates/recipes.json') as f:
    #     allRecipes = []
    #     recipes = json.load(f)
    #     for recipe in recipes:
    #         if int(recipe['id'])==int(editRecipe['id']):
    #             recipe = editRecipe
    #         allRecipes.append(recipe)
    #     with open(app.root_path+'/templates/recipes.json', "w") as jsonFile:
    #         json.dump(allRecipes, jsonFile)
    
    # return redirect("dashboard", code=303)

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
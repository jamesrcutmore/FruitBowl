#python -m flask run
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from random import randint
from flask import  session


import json
app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

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

@app.route('/users.json')
def usersJSON():
    return render_template('users.json') 


@app.route('/login', methods=['POST'])
def dashboard():
   email = request.form['email']
   password = request.form['password']

   if email == "":
    return 'Please add a valid email address'
     
   elif password == "":
    return 'Please add a valid password'
   with open(app.root_path+'/templates/users.json') as f:
        users = json.load(f)
        for user in users:
            print(user)
            if(user['email']==email and user['password']==password):
                session['id'] = user['id']
                session['admin'] = user['admin'] 
                return render_template('dashboard.html',user = user)                       
        
        return "User not found."

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
    newRecipe = {}
    newRecipe.update({'title' : request.form['title']})
    newRecipe.update({'description' : request.form['description']})
    newRecipe.update({'imageURL' : request.form['imageURL']})
    newRecipe.update({'id' : randint(0, 10000)})

    for value in newRecipe.values():
	    print(value)
    with open(app.root_path+'/templates/recipes.json') as f:
        allRecipes = []
        recipes = json.load(f)
        for recipe in recipes:
            allRecipes.append(recipe)
        allRecipes.append(newRecipe)
        with open(app.root_path+'/templates/recipes.json', "w") as jsonFile:
            json.dump(allRecipes, jsonFile)
        return redirect("dashboard", code=303)
    
@app.route('/dashboard')
def show_dashboard():
   user = {'id' : session['id'], 'admin':session['admin']}
   return render_template('dashboard.html',user = user)

@app.route('/edit-recipe.html')
def edit_recipe():
   
    id = request.args['id']
    with open(app.root_path+'/templates/recipes.json') as f:
        print(id)
        recipes = json.load(f)
        recipeFound = None
        for recipe in recipes:
            if int(recipe['id'])==int(id):
                recipeFound = recipe
            
        print(recipeFound)
    return render_template('edit-recipe.html',recipe=recipeFound)

@app.route('/signUp', methods=['POST'])
def signUpSubmit():
  
   email = request.form['email']
   password = request.form['password']
   firstname = request.form['firstname']
   surname = request.form['surname']
   admin = 0
   
   if email == "":
    return 'Please add a valid email address'
     
   if password == "":
    return 'Please add a valid password'
   
   if firstname == "":
    return 'Please add a valid First name'

   if surname == "":
    return 'Please add a valid Surname'
  
   newUser = {}
   newUser.update({'firstname' : firstname})
   newUser.update({'surname' : surname})
   newUser.update({'email' : email})
   newUser.update({'password' : password})
   newUser.update({'id' : randint(0, 10000)})
   newUser.update({'admin' : admin})
   

   with open(app.root_path+'/templates/users.json') as f:
       
        allUsers = []
        users = json.load(f)
        for user in users:
            allUsers.append(user)
        allUsers.append(newUser)
        print(allUsers)
        with open(app.root_path+'/templates/users.json', "w") as jsonFile:
         json.dump(allUsers, jsonFile)

        return "signup completed."

@app.route('/editrecipe', methods=['POST'])
def editrecipe():

    editRecipe = {}
    editRecipe.update({'title' : request.form['title']})
    editRecipe.update({'description' : request.form['description']})
    editRecipe.update({'imageURL' : request.form['imageURL']})
    editRecipe.update({'id' : request.form['id']})
    editRecipe.update({'userid' :1})

    for value in editRecipe.values():
	    print(value)
    with open(app.root_path+'/templates/recipes.json') as f:
        allRecipes = []
        recipes = json.load(f)
        for recipe in recipes:
            if int(recipe['id'])==int(editRecipe['id']):
                recipe = editRecipe
            allRecipes.append(recipe)
        with open(app.root_path+'/templates/recipes.json', "w") as jsonFile:
            json.dump(allRecipes, jsonFile)
    
        return redirect("dashboard", code=303)

if __name__ == '__main__':
    app.debug = True
    app.run() #go to http://localhost:5000/ to view the page.
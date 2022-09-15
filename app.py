#python -m flask run
from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
                        
                        

if __name__ == '__main__':
    app.debug = True
    app.run() #go to http://localhost:5000/ to view the page.
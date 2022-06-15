from flask import Flask, render_template, request
import jinja2
import json

#run this doc in virtenv 'source virt/scripts/activate
#to update changes without restarting flask type 'export FLASK_ENV=development', 'export FLASK_APP=app.py'
#make sure to use virtenv interpereter



app = Flask(__name__)


@app.route('/')
def index():
  
  first_name='Grab first name from database'
  return render_template("index.html", first_name = first_name)




#error pages
#invalid URL
@app.errorhandler(404)
def page_not_found(e):
  return render_template("error_pages/404.html"), 404



@app.errorhandler(500)
def page_not_found(e):
  return render_template("error_pages/500.html"), 500











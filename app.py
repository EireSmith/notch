from website import create_app
from website import db
#use virtenv interpereterr
#run this doc in virtenv 'source virt/scripts/activate
#export FLASK_ENV=development 
#export FLASK_APP=app.py
db = db
app = create_app()


if __name__ == '__main__': #run web server
  app.run(debug=True)

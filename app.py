from website import create_app

app = create_app()


if __name__ == '__main__': #run web server
  app.run(debug=True)



#run this doc in virtenv 'source venv/scripts/activate'
#export FLASK_ENV=development 
#export FLASK_APP=app.py
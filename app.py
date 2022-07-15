from website import create_app
#use virtenv interpereter
#run this doc in virtenv 'source virt/scripts/activate
#export FLASK_ENV=development 
#c

app = create_app()


if __name__ == '__main__': #run web server
  app.run(debug=True)

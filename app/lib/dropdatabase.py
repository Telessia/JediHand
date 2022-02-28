from pymongo import MongoClient
#Connection to running database
client = MongoClient('localhost', 27017,
                     username='root',
                 password='root')
db = client['jedihand_development'] #name of the database, see docker-compose

models = db.models
models_test = db.models_test

# you want to reset your base collection uncomment the line under
#models.drop()

# you want to reset your test collection uncomment the line under
#models_test.dro()
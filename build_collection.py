from db.db_init import db_init

# Connection informatino for the mongo server
db_ip = 'localhost'
db_port = 27017

# Magic api connection
api_connection_str = 'https://api.magicthegathering.io/v1/cards'

# Database and collection names
db_name = 'cards'
coll_name = 'cards'

# Initialize the db updated
db = db_init(connection_str=f'{db_ip}:{db_port}', db_name=db_name,
        coll_name=coll_name, api_connection_str=api_connection_str)
print('here')
db.update_db()
print('here again')
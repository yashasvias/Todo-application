import json


with open('config.json', 'r') as f:
    config = json.load(f)



dburl = config['db']['url']
dbport = config['db']['port']
db = config['db']['db']
dbuser = config['db']['user']
dbpass = config['db']['pass']


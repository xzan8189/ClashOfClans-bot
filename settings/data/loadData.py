import json
from decimal import Decimal
from replit import db

def load_users(data):
    db['staff'] = data['staff']
  

if __name__ == '__main__':
    with open("data.json") as json_file:
        data = json.load(json_file, parse_float=Decimal)
        load_users(data)
        
    username = "Xzan8189"

    print("Staff di Telegram: ")
    for item in db['staff']:
        print(item)
        #print(item['username_telegram'])
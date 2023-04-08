import json
from decimal import Decimal



if __name__ == '__main__':
    with open("data.json") as json_file:
        data = json.load(json_file, parse_float=Decimal)

        username = "Xzan8189"

        print("Staff di Telegram: ")
        for item in data:
            print(item)
            #print(item['username_telegram'])
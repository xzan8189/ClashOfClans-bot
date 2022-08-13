import os
import requests
from datetime import datetime

COC_TOKEN = os.environ['Clash_of_clans_API_token']


headers = {
  'Accept': 'application/json',
  'authorization': 'Bearer ' + COC_TOKEN
}

class Clash_of_clans:

    @staticmethod
    def search_clan():
        response = requests.get(
            'https://api.clashofclans.com/v1/clans/%232LGL9JPJY',
            headers=headers
        )
        clan_json = response.json()
        print("Persone presenti nel clan:")
        for user in clan_json['memberList']:
            print(user['name'], end=" ")

    @staticmethod
    def current_war():
        response = requests.get(
            'https://api.clashofclans.com/v1/clans/%232LGL9JPJY/currentwar',
            headers=headers
        )
        clan_json = response.json()
        if 'members' not in clan_json['clan']:
            date_format = "%Y%m%dT%H%M%S.%fZ" 
            current_date = datetime.strptime(datetime.today().strftime(date_format), date_format)
            startTime = datetime.strptime(clan_json['startTime'], date_format)
            time_remaining = startTime - current_date
            minuti = int(time_remaining.total_seconds()/60)
            ore = int(minuti/60)
            
            string = "```\nLa war non è ancora iniziata\.\n"
            string += "Giorno dei preparativi termina dopo " + str(ore) + " Ore " +  str(minuti) + " Minuti\n"
            string += '```'
            return string

        formattazione1 = "{0:4s} {1:14s} {2:10s}"
        formattazione2 = "{0:4s} {1:18s} {2:1d}"
        string = "```\n"
        #print(formattazione1.format("#", "Nome", "Attacchi_rimanenti"))
        string += formattazione1.format("\#", "Nome", "Attacchi") + '\n'

        def mapPosition(user):
            return user['mapPosition']

        list_mia = list(clan_json['clan']['members'])
        list_mia.sort(key=mapPosition)

        i = 1
        for user in list_mia: # Calcolo degli attacchi rimanenti di ogni giocatore
            if 'attacks' not in user:
                #print(formattazione2.format(user['name'], 2))
                string += formattazione2.format(str(i)+'\.', user['name'], 2)
            elif len(user['attacks']) == 1:
                #print(formattazione2.format(user['name'], 1))
                string += formattazione2.format(str(i)+'\.', user['name'], 1)
            elif len(user['attacks']) == 2:
                #print(formattazione2.format(user['name'], 0))
                string += formattazione2.format(str(i)+'\.', user['name'], 0)
            else:
                print("C'è qualche problema")

            string += '\n'
            i += 1

        return string + '```'

if __name__ == '__main__':
    string = Clash_of_clans.current_war()
    print(string)
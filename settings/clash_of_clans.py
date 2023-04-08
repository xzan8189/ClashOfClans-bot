import os
import requests
from datetime import datetime

COC_TOKEN = process.env.Clash_of_clans_API_token

headers = {
    'Accept': 'application/json',
    'authorization': 'Bearer ' + COC_TOKEN
}


class Clash_of_clans:

    @staticmethod
    def search_clan():
        response = requests.get(
            'https://api.clashofclans.com/v1/clans/%232LGL9JPJY',
            headers=headers)
        clan_json = response.json()
        print("Persone presenti nel clan:")
        for user in clan_json['memberList']:
            print(user['name'], end=" ")

    @staticmethod
    def current_war():
        response = requests.get(
            'https://api.clashofclans.com/v1/clans/%232LGL9JPJY/currentwar',
            headers=headers)
        clan_json = response.json()
        print(clan_json)
        if clan_json['state'] == 'notInWar':  # Nessuna WAR
            return "```\nNon c'è nessuna WAR al momento\.\n```"

        elif clan_json['state'] == 'preparation':  # Preparativi WAR
            date_format = "%Y%m%dT%H%M%S.%fZ"
            current_date = datetime.strptime(
                datetime.today().strftime(date_format), date_format)
            startTime = datetime.strptime(clan_json['startTime'], date_format)
            time_remaining = startTime - current_date
            totale = int(time_remaining.total_seconds() / 60)
            ore = int(totale / 60)
            minuti = int(totale - (ore * 60))

            string = "```\nLa War non è ancora iniziata\.\n"
            string += "Giorno dei preparativi termina dopo " + str(
                ore) + " Ore " + str(minuti) + " Minuti\n"
            string += '```'
            return string

        else:  # WAR INIZIATA
            formattazione1 = "{0:4s} {1:14s} {2:10s}"
            formattazione2 = "{0:4s} {1:18s} {2:1d}"
            string = "```\n"
            string += Clash_of_clans.getTimeRemainingWar(clan_json)[0] + "\n\n"
            #print(formattazione1.format("#", "Nome", "Attacchi_rimanenti"))
            string += formattazione1.format("\#", "Nome", "Attacchi") + '\n'

            def mapPosition(user):
                return user['mapPosition']

            list_mia = list(clan_json['clan']['members'])
            list_mia.sort(key=mapPosition)

            i = 1
            for user in list_mia:  # Calcolo degli attacchi rimanenti di ogni giocatore
                if 'attacks' not in user:
                    #print(formattazione2.format(user['name'], 2))
                    string += formattazione2.format(
                        str(i) + '\.', user['name'], 2)
                elif len(user['attacks']) == 1:
                    #print(formattazione2.format(user['name'], 1))
                    string += formattazione2.format(
                        str(i) + '\.', user['name'], 1)
                elif len(user['attacks']) == 2:
                    #print(formattazione2.format(user['name'], 0))
                    string += formattazione2.format(
                        str(i) + '\.', user['name'], 0)
                else:
                    print("C'è qualche problema")

                string += '\n'
                i += 1

            return string + '```'

    @staticmethod
    def result_last_war():
        response = requests.get(
            'https://api.clashofclans.com/v1/clans/%232LGL9JPJY/warlog',
            headers=headers)
        clan_json = response.json()['items'][0]

        my_clan = clan_json['clan']
        opponent_clan = clan_json['opponent']
        formattazione1 = "{0:15s} {1:2s}"
        string = '```\n'

        # MY CLAN
        string += "Risultato: " + clan_json['result'].upper() + "\n\n"
        string += "*Il Gallo Unisce*\n"
        string += formattazione1.format('Stelle:',
                                        str(my_clan['stars']) + "\n")
        string += formattazione1.format(
            '% distruzione:',
            str(my_clan['destructionPercentage']) + "\n")
        string += formattazione1.format('Attacchi:',
                                        str(my_clan['attacks']) + "\n")
        string += formattazione1.format('ExpEarned:',
                                        str(my_clan['expEarned']) + "\n")

        # OPPONENT CLAN
        string += "\n*" + opponent_clan['name'] + "*\n"
        string += formattazione1.format('Stelle:',
                                        str(opponent_clan['stars']) + "\n")
        string += formattazione1.format(
            '% distruzione:',
            str(opponent_clan['destructionPercentage']) + "\n")
        return string + '\n```'

    # Metodi ausiliari
    @staticmethod
    def getTimeRemainingWar(clan_json):
        date_format = "%Y%m%dT%H%M%S.%fZ"
        current_date = datetime.strptime(
            datetime.today().strftime(date_format), date_format)
        endTime = datetime.strptime(clan_json['endTime'], date_format)
        time_remaining = endTime - current_date
        totale = int(time_remaining.total_seconds() / 60)
        ore = int(totale / 60)
        minuti = int(totale - (ore * 60))
        war_terminata = None

        if clan_json['state'] != "warEnded":
            string = "La war termina tra " + str(ore) + " Ore " + str(
                minuti) + " Minuti"
            war_terminata = False
        else:
            string = "WAR TERMINATA"
            war_terminata = True

        return string, war_terminata


if __name__ == '__main__':
    string = Clash_of_clans.current_war()
    print(string)

import json
from decimal import Decimal


class Telegram:

    @staticmethod
    def get_staff():

        formattazione1 = "{0:15s} {1:10s}"
        formattazione2 = "{0:15s} {1:10s}"
        string = "```\n"
        string += formattazione1.format("STAFF", "RUOLO") + '\n\n'

        with open("data.json") as json_file:
            staff = json.load(json_file, parse_float=Decimal)
        for staffer in staff: # Calcolo degli attacchi rimanenti di ogni giocatore
            string += formattazione2.format(staffer['username_telegram'], staffer['role'])

            string += '\n'

        return string + '```'

    @staticmethod
    def info():
        string = "Il mio creatore è quest'uomo, vi linko il suo profilo Github: https://github.com/xzan8189"

        return string

if __name__ == '__main__':
    staff = Telegram.get_staff()
    print(staff)
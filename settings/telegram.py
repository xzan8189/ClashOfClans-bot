from replit import db


class Telegram:

    @staticmethod
    def get_staff():

        formattazione1 = "{0:15s} {1:10s}"
        formattazione2 = "{0:15s} {1:10s}"
        string = "```\n"
        string += formattazione1.format("STAFF", "RUOLO") + '\n\n'

        staff = db['staff']
        for staffer in staff: # Calcolo degli attacchi rimanenti di ogni giocatore
            string += formattazione2.format(staffer['username_telegram'], staffer['role'])

            string += '\n'

        return string + '```'

if __name__ == '__main__':
    staff = Telegram.get_staff()
    print(staff)
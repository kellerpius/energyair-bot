import sys
from lxml import html
import requests
import os
import time

rounds = 0
phoneNumber = os.environ["PHONE_NUMBER"]
print("using " + str(phoneNumber) + " as phone number")
print("helloworld")
questions = {
    'Was verlangte Nena am Energy Air 2016?' : 'Eine komplett weisse Garderobe',
    'Welcher Act stand beim ersten Energy Air 2014 und auch im letzten Jahr auf der Bühne?' : 'Pegasus',
    'Wer stand am letzten Energy Air als Überraschungsgast auf der Bühne?' : 'Bastian Baker',
    'Energy Air ist der einzige Energy Event, …' : '…bei dem nationale und internationale Künstler auftreten.',
    'Welche Fussballmannschaft ist im Stade de Suisse zuhause?' : 'BSC Young Boys',
    'Wie breit ist die Energy Air Bühne?' : '70 Meter',
    'Wen nahm Knackeboul am Energy Air 2014 mit backstage?' : 'Sein Mami',
    'Wie schwer ist die Energy Air Bühne?' : '450 Tonnen',
    'Welcher Act interviewte vor dem letzten Energy Air das Publikum?' : 'Baba Shrimps',
    'Wer war der letzte Act beim Energy Air 2017?' : 'Kodaline',
    'Welche amerikanische Band trat am Energy Air 2016 auf?' : 'One Republic',
    'Welcher Schweizer Shootingstar spielt in DAS SCHÖNSTE MÄDCHEN DER WELT die Hauptrolle?' : 'Luna Wedler',
    'Mit welchem dieser Tickets geniesst du die beste Sicht zur Energy Air Bühne?' : 'XTRA-Circle',
    'Auf welcher Social-Media-Plattform kann man keine Energy Air Tickets gewinnen?' : 'Twitter',
    'Auf welchem Weg kann man KEINE Energy Air Tickets gewinnen?' : 'per Mail',
    'Wie reiste Kygo im Jahr 2015 ans Energy Air?' : 'Im Privatjet',
    'Welcher berühmte DJ-Act stand 2017 auf der Bühne des Energy Air?' : 'Dimitri Vegas & Like Mike',
    'Wie viele Acts waren beim letzten Energy Air dabei?' : '15',
    'Wo erfährst du immer die neusten Infos rund um Energy Air?' : 'im Radio, auf der Website und über Social Media',
    'Welcher Schauspieler/Rapper trägt im Film eine goldene Maske?' : 'Cyril',
    'Wann fand Energy Air zum ersten Mal statt?' : '2014',
    'Wer spielt die Mutter von Cyril?' : 'Anke Engelke',
    'Die wievielte Energy Air Ausgabe findet dieses Jahr statt?' : 'Die fünfte',
    'Wo findet das Energy Air statt?' : 'Stade de Suisse (Bern)',
    'Welche Farbe haben die Haare des Social Media Stars Julia Beautx im Film?' : 'Pink',
    'Wie viele Konfetti-Kanonen gibt es am Energy Air?' : '20',
    'Welchen Song performte Dodo am Energy Air mit den Überraschungsgästen Lo & Leduc?' : 'Jung verdammt',
    'Wie viele Spotlights gibt es am Energy Air?' : '250',
    'Mit welchem Preis wurde der Nachwuchsstar Luna Wedler dieses Jahr ausgezeichnet?' : 'Shootingstar Berlinale 2018',
    'Wann ist der offizielle Filmstart von DAS SCHÖNSTE MÄDCHEN DER WELT in den Schweizer Kinos?' : '6. September 2018',
    'Das NRJ-Gefährt ist ein…' : 'Tuk Tuk',
    'Energy Air Tickets kann man…' : 'gewinnen',
    'Wann beginnt das Energy Air 2018?' : 'Um 17 Uhr',
    'Was passiert, wenn es am Eventtag regnet?' : 'Energy Air findet trotzdem statt',
    'Was ist Cyrils (Aaron Hilmer) Markenzeichen im Film?' : 'Seine grosse Nase',
    'Wann findet das Energy Air 2018 statt?' : '8. September 2018',
    'Wie heisst der aktuelle Sommerhit von Energy Air Act Alvaro Soler?' : 'La Cintura',
    'Was ist Cyrils besondere Begabung?' : 'Texte schreiben und rappen',
    'Wer eröffnete das erste Energy Air?' : 'Bastian Baker',
    'Welcher dieser Acts hatte einen Auftritt am Energy Air 2017?' : 'Aloe Blacc',
    'Woher kommt Energy Air Act Max Giesinger?' : 'Deutschland',
    'Wohin führt die Klassenfahrt?' : 'Berlin'
}

def get_answer(question):
    answer = questions.get(question, 0)
    if answer == 0:
        return 1
    return answer

def next_question(antwort):
    antwort = tree.xpath('//form[@id="'+antwort+'"]/h3/value()')[0]
    print('DenoTest:')
    print(antwort)
    data = {'question': antwort}
    q2 = session.post('https://game.energy.ch/', data)
    tree = html.fromstring(q2.content)
    frage = tree.xpath('//form[@class="questions"]/h3/text()')[0]
    return frage

try:
    while True:
        try:
            print('startsssssssss')
            rounds += 1
            session = requests.session()
            data = {'mobile': phoneNumber}
            q1 = session.post('https://game.energy.ch/', data)
            tree = html.fromstring(q1.content)
            print(tree)

            frage = tree.xpath('//form[@class="questions"]/h3/text()')[0]
            print("answering questions...")
            for i in range(9):
                time.sleep(0.5)
                antwort = get_answer(frage)
                frage = next_question(antwort)
            antwort = get_answer(frage)

            data = {'question': antwort}
            q2 = session.post('https://game.energy.ch/', data)
            print("all questions answered!")

            tree = html.fromstring(q2.content)
            verloren = tree.xpath('//div[@id="content"]/h2/text()')
            if verloren[0] == "Glückwunsch!":
                data = {'site': 'win'}
                q2 = session.post('https://game.energy.ch/', data)
                q2 = session.get('https://game.energy.ch/?ticket=10')
                tree = html.fromstring(q2.content)
                verloren = tree.xpath('//div[@id="wingame"]/h1/text()')
                if len(verloren) == 1:
                    if verloren[0] != "Das war das falsche Logo, knapp daneben! Versuche es erneut!":
                        f = open('win.txt', 'wb')
                        f.write(q2.content)
                        f.close()
                        print("code 5")
                        print("restart...")
                    else:
                        print("code 4")
                        print("restart...")
                else:
                    print("code 3")
                    print("restart...")
            else:
                print("code 2")
                print("restart...")

        except Exception:
            print("code 1")
            print("restart...")
            pass
finally:
    print("\n\n------see ya------")
    print("Rounds: " + str(rounds))
    print("------------------")
    sys.exit(0)

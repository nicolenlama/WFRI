import json
import urllib.request, urllib.parse, urllib.error
import ssl
import re
import sqlite3


#create sql table
conn = sqlite3.connect('towncouncil.db')
c = conn.cursor()
c.execute('''CREATE TABLE votes 
        (town_name varchar(100), name varchar(100), 
        party_code varchar (100),
        votes varchar(10))''')

#certification settings
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#url and confirmation it's working
url = 'https://www.ri.gov/election/results/2020/general_election/data/'
print('Retrieving', url)

#open up
uh = urllib.request.urlopen(url, context=ctx)

#extract all the lines that include .json and add to list
interest = []
for line in uh:
    line = line.decode().strip()
    if ".json" in line: #format to having online link
        no_end = line.split('">')[0]
        nostart = (no_end[13:])
        interest.append(nostart)

for link in interest:
    #open each link
    uh = urllib.request.urlopen(link, context=ctx)
    data = uh.read().decode()
    #load data
    js = json.loads(data)
    #subsets contests and set search key to include only Town Council data
    contests = js['contests']
    search_key = 'Town Council' 

    #separate into for all contests
    for each in contests:
        if search_key in each['name']:
            town_name = each['name']
            votes_a = each['votes_allowed'] #how many people will be elected
            candidates = each['candidates'] #the candidates
            town_name = town_name.replace(" ", "_") #didnt work with space
            final = candidates[:int(votes_a)] #add the top candidates according to how many were allowed
            #insert values from candidates who were elected into sql table
            for nested in final:
                c.execute("INSERT INTO votes VALUES (?, ?,?,?)", [town_name, nested["name"], nested["party_code"], nested["votes"]])
                conn.commit()

conn.close()
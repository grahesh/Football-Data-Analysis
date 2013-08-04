#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      GRSP
#
# Created:     30-05-2013
# Copyright:   (c) GRSP 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------


from bs4 import BeautifulSoup
import requests
import csv
import pandas as p
import sys
import os

df = p.read_csv("All_Matches.csv")
newpath = r'Match Details'
if not os.path.exists(newpath): os.makedirs(newpath)

for i in df.index:
    url= df.ix[i]['MatchLink']

##    url='http://www.11v11.com/matches/warmley-v-southampton-03-october-1891-219170/'

    html = requests.get(url).text

    soup = BeautifulSoup(html)

    fileEntry=[]
    match=''
    date=''

    fileEntry.append(["League", df.ix[i]['League']])

    #match name and date
    head = soup.html.head.title

    try:
        match,date=head.text.split("-")[0].strip().split(",")
        fileEntry.append(["Match",match.strip()])
        fileEntry.append(["Date",date.strip()])
    except:
        print 'No Match Details.'
        fileEntry.append(["Match",""])
        fileEntry.append(["Date",""])

    print "Count: ",i+1,' Match: ',match+date

    #match details
    try:
        matchDet=soup.find("div", {"class":"basicData"})
        table = matchDet.find('table')
        rows = table.findAll('tr')
        for tr in rows:
          cols = tr.findAll('td')
          op=[]
          for td in cols:
              text = ''.join(td.find(text=True))
              op.append(text)
          fileEntry.append(op)
    except:
        print 'No Match Basic Details present.'

    # home team
    homegoals='0'
    home=match.split('v')[0].strip()
    try:
        homeTeam=soup.find("div", {"class":"home"})
        try:
            home= homeTeam.find("a").text.strip()
        except:
            home= match.split('v')[0]

        fileEntry.append(["Home Team",home])
        homegoals= homeTeam.find("span").text.strip()
        fileEntry.append(["Home Team Goals",homegoals])
    except:
        print 'No goals HOME TEAM.'
        fileEntry.append(["Home Team",home])
        fileEntry.append(["Home Team Goals",homegoals])

    # away team
    awaygoals='0'
    away=match.split('v')[1].strip()
    try:
        awayTeam=soup.find("div", {"class":"away"})
        try:
            away=awayTeam.find("a").text.strip()
        except:
            away=match.split('v')[1].strip()

        fileEntry.append(["Away Team",away])
        awaygoals=awayTeam.find("span").text.strip()
        fileEntry.append(["Away Team Goals",awaygoals])
    except:
        print 'No Goals AWAY TEAM.'
        fileEntry.append(["Away Team",away])
        fileEntry.append(["Away Team Goals",'0'])

    if((int)(homegoals)==(int)(awaygoals)):
        fileEntry.append(["Result","Draw"])
    elif((int)(homegoals)>(int)(awaygoals)):
        fileEntry.append(["Result",home])
    elif((int)(homegoals)<(int)(awaygoals)):
        fileEntry.append(["Result",away])

    # players
    home=soup.find("div", {"class":"lineup"})
    ##
    # home team players
    try:
        homeTeamPlayers=home.find("div", {"class":"home"})
        homeTeamPlayers= homeTeamPlayers.findAll("div")
        pl=[]
        pl.append("Home Team Players")
        for player in homeTeamPlayers:
            name=player.find("a").text
            position=player.find("span").text
            country=''
            try:
                country= (str)(player).split("/")[4].split(".")[0]
            except:
                print 'no mention of player country'

            pl.append(name+'-'+position+'-'+country)

        fileEntry.append(pl)
    except:
        print 'Home team players not mentioned.'
        fileEntry.append(['Home Team Players'])

    ##
    # away team players
    try:
        awayTeamPlayers=home.find("div", {"class":"away"})
        awayTeamPlayers= awayTeamPlayers.findAll("div")

        pl=[]
        pl.append("Away Team Players")
        for player in awayTeamPlayers:
            name=player.find("a").text
            position=player.find("span").text
            country=''
            try:
                country= (str)(player).split("/")[4].split(".")[0]
            except:
                print 'no mention of player country'

            pl.append(name+'-'+position+'-'+country)

        fileEntry.append(pl)
    except:
        print 'Away Team players not mentioned.'
        fileEntry.append(['Away Team Players'])

    # substitutions
    substitutions=soup.find("div", {"class":"substitutions"})
    ##
    #home
    try:
        homeSubst=substitutions.find("div", {"class":"home"})
        table = homeSubst.find('table')
        rows = table.findAll('tr')
        op=[]
        op.append("Home Team Substitutions")
        for tr in rows:
            cols = tr.findAll('td')
            op2=''
            for td in cols:
                op2=op2+td.text+"-"
            op.append(op2)

        fileEntry.append(op)
    except:
        print 'Home Team No Substitutions.'
        fileEntry.append(['Home Team Substitutions'])

    #away
    try:
        awaySubst=substitutions.find("div", {"class":"away"})
        table = awaySubst.find('table')
        rows = table.findAll('tr')
        op=[]
        op.append("Away Team Substitutions")
        for tr in rows:
            cols = tr.findAll('td')
            op2=''
            for td in cols:
                op2=op2+td.text+"-"
            op.append(op2)

        fileEntry.append(op)
    except:
        print 'Away Team No Substitutions.'
        fileEntry.append(['Away Team Substitutions'])

    # goals
    goals=soup.find("div", {"class":"goals"})

    op=[]
    op.append("Home Team Goal Scorers")

    #home
    try:
        homeGoals=goals.find("div", {"class":"home"})
        table = homeGoals.find('table')
        rows = table.findAll('tr')

        for tr in rows:
          cols = tr.findAll('td')
          op2=''
          for td in cols:
            op2=op2+td.text.strip()+"-"
          op.append(op2)
    except:
        print 'No Home Team Goal Scorers.'
        fileEntry.append(op)

    else:
        fileEntry.append(op)

    #away
    op=[]
    op.append("Away Team Goal Scorers")

    try:
        awayGoals=goals.find("div", {"class":"away"})
        table = awayGoals.find('table')
        rows = table.findAll('tr')

        for tr in rows:
          cols = tr.findAll('td')
          op2=''
          for td in cols:
            op2=op2+td.text.strip()+"-"
          op.append(op2)
    except:
        print 'No Away Team Goal Scorers.'
        fileEntry.append(op)

    else:
        fileEntry.append(op)

    #
    # cards
    cards=soup.find("div", {"class":"cards"})
    op=[]
    op.append("Home Team Cards")

    try:
        #home
        homecards=cards.find("div", {"class":"home"})
        table = homecards.find('table')
        rows = table.findAll('tr')

        for tr in rows:
            cols = tr.findAll('td')
            op2=''
            for td in cols:
                op2=op2+td.text.strip()+"-"
            op.append(op2)
    except:
        print 'No cards for home team'
        fileEntry.append(op)

##    else:
##        fileEntry.append(op)

    op=[]
    op.append("Away Team Cards")
    try:
        #away
        awaycards=cards.find("div", {"class":"away"})
        table = awaycards.find('table')
        rows = table.findAll('tr')

        for tr in rows:
          cols = tr.findAll('td')
          op2=''
          for td in cols:
            op2=op2+td.text.strip()+"-"
          op.append(op2)

    except:
        print 'No cards for away team'
        fileEntry.append(op)

##    else:
##        fileEntry.append(op)


    # on the bench


    # home team players
    try:
        home=soup.findAll("div", {"class":"lineup"})[1]
        homeTeamPlayers=home.find("div", {"class":"home"})
        homeTeamPlayers= homeTeamPlayers.findAll("div")
        pl=[]
        pl.append("Home Team Players on Bench")
        for player in homeTeamPlayers:
            name=player.find("a").text
            position=player.find("span").text
            country=''
            try:
                country= (str)(player).split("/")[4].split(".")[0]
            except:
                print 'No mention of players country'

            pl.append(name+'-'+position+'-'+country)
        fileEntry.append(pl)
    except:
        print 'No home team players on bench.'
        fileEntry.append(['Home Team Players on Bench'])


    # away team players
    try:
        home=soup.findAll("div", {"class":"lineup"})[1]
        awayTeamPlayers=home.find("div", {"class":"away"})
        awayTeamPlayers= awayTeamPlayers.findAll("div")
        pl=[]
        pl.append("Away Team Players on Bench")
        for player in awayTeamPlayers:
            name=player.find("a").text
            position=player.find("span").text
            country=''
            try:
                country= (str)(player).split("/")[4].split(".")[0]
            except:
                print 'players country not mentioned.'

            pl.append(name+'-'+position+'-'+country)
        fileEntry.append(pl)
    except:
        print 'No away team players on bench.'
        fileEntry.append(['Away Team Players on Bench'])

    try:
        fp = open(newpath+'\\'+match+'_'+date+'.csv',"wb")
        cot=csv.writer(fp)
        for entry in fileEntry:
            cot.writerow(entry)
        fp.close()
    except:
        print "File Writing Error."

##    sys.exit()

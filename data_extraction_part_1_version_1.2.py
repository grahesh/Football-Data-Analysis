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
import collections
import sys
import os
import traceback
import unicodedata
import urllib2

# Extracts match details for all teams for all years.

def fetch_all_teams(soup):
    teamsList=dict()
    print '"""""""""""""""""""""""Fetching All Teams""""""""""""""""""""""""""""""'

    teams=soup.find('ul',{"class":"team-links"})
    for li in teams.findAll('li'):
        team= li.find('a')['href']
##        print team
        if team.startswith("http://www.11v11.com"):
            teamlink=team+'tab/matches/'
        elif(team.strip()[-1]=="/"):
            teamlink='http://www.11v11.com'+team.strip()+'tab/matches/'
        else:
            teamlink='http://www.11v11.com'+team.strip()+'/tab/matches/'

        tm=li.find('a').text
        teamsList[tm]=teamlink

    teamsList = collections.OrderedDict(sorted(teamsList.items()))
##    print teamsList
##    sys.exit()
##    print teamsList
    return teamsList


def fetch_all_years(teamsoup):
    yearList=dict()
##    print teamsoup
##    teamhtml = requests.get("http://www.11v11.com/teams/aston-villa/tab/matches").text
##    teamsoup = BeautifulSoup(teamhtml)

    seasons=teamsoup.find('ul',{"id":"season"})
##    print seasons

    for li in seasons.findAll('li'):
        yearlink =  li.find('a')['href']

##        print yearlink

        yr=li.find('a').text
        yearList[yr]=yearlink

    yearList = collections.OrderedDict(sorted(yearList.items()))
##    print yearList
##    sys.exit()
    return yearList

def fetch_all_matches(yearsoup):
    matchlist=dict()
    table=yearsoup.find("table","width580 sortable")
    try:
        matches = table.findAll('tr')
        for tr in range(1,len(matches)):
            cols = matches[tr].findAll('td')
            dt=cols[0].text.strip()
            match=cols[1].find('a').text.strip()
            matchlink= 'http://www.11v11.com'+cols[1].find("a")['href']
            result=cols[2].find('span').text.strip()
            score=cols[3].text.strip().split("-")
            league= cols[4].text.strip()
            matchlist[match+dt]=[dt,match,result,score[0]+' and '+score[1],league,matchlink]
    except:
        print 'NO MATCHES.fetching match list error.'

    return matchlist


# def internet_on():
#     try:
#         response=urllib2.urlopen('http://stackoverflow.com/questions/3764291/checking-network-connection')
#         print response
#         return response
#     except urllib2.URLError as err: pass
#     return False

def main():
    allmatches=[]
    newpath = r'Results'
    # result=False
    # while result==False:
    #     try:
    #         result=internet_on()
    #         print result
    #     except:
    #         continue

    if not os.path.exists(newpath): os.makedirs(newpath)

    url='http://www.11v11.com/league-two/'
    html = requests.get(url).text
    soup = BeautifulSoup(html)

    #fetching all teams
    teamsList=fetch_all_teams(soup)

    fp = open('All_Matches.csv',"wb")
    cot=csv.writer(fp)
    cot.writerow(['Date', 'Match', 'Result', "Score", 'League', 'MatchLink'])

    # fetching all years for a team
    print '"""""""""""""""""""""""""""""Fetching all years""""""""""""""""""""""""""""""""""""'
    for team in teamsList.keys():
        print "Team: ",team
        teamhtml = requests.get(teamsList[team]).text
##        print teamsList[team]
##        print "Team Html: ",teamsList[team]
        teamsoup = BeautifulSoup(teamhtml)
        yearList=fetch_all_years(teamsoup)

        # fetching matches per year of team
        print '"""""""""""""""""""""""""""""Fetching all matches for year""""""""""""""""""""""""""""""""""""'
        for year in reversed(yearList.keys()):
            print team,' : ',year

            fp2 = open(newpath+'\\'+team+'_'+year+'_All_Matches.csv',"wb")
            cot2=csv.writer(fp2)
            cot2.writerow(['Date', 'Match', 'Result', "Score", 'League', 'MatchLink'])

            yearhtml = requests.get(yearList[year]).text
            yearsoup = BeautifulSoup(yearhtml)
            matchList=fetch_all_matches(yearsoup)


            if(len(matchList.keys())>0):
                for match in matchList.keys():

                    try:
                        if(match not in allmatches):
                            cot.writerow(matchList[match])
                            allmatches.append(match)

                            cot2.writerow(matchList[match])
                        else:
                            cot2.writerow(matchList[match])

                    except Exception,e:
                        print traceback.print_exc()

                        matchList[match][1] = unicodedata.normalize('NFKD', matchList[match][1]).encode('ascii','ignore')
                        matchList[match][5] = unicodedata.normalize('NFKD', matchList[match][5]).encode('ascii','ignore')
                        print matchList[match]

                        if(match not in allmatches):
                            cot.writerow(matchList[match])
                            allmatches.append(match)

                            cot2.writerow(matchList[match])
                        else:
                            cot2.writerow(matchList[match])

##                        sys.exit()

            else:
                print 'No Matches for this year.'



            fp2.close()
    fp.close()

    print 'Code Execution Finished.'

if __name__ == '__main__':
    main()

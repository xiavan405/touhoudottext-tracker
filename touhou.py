#!/usr/bin/env python

from twitter import *
import socket
import random

#twitter config
conKey='<consumer_secret>'
conSecret='<consumer_secret>'
userToken='<user_token>'
tokenSecret='<user_secret>'

twitterTuple=[conKey,conSecret,userToken,tokenSecret]

#network config
network='irc.rizon.net'
port=6667
channel='#bot700059679'
nick='touhoudottxt'

networkTuple=[network,port,channel,nick]

#bot settings
botname='touhoudottxt-tracker'
version='2.0 \'Hermit Purple\''
#changelog='Added error handling. Added @reply,RT,link, and note filters. Refactored twitter code (now 20% worse!). Added a small history buffer. Changed nick. Removed stability. Removed fun.'
changelog='Maybe fixed twitter filters, shouldn\'t have to flush. Removed history buffer because it was worthless. Didn\'t fix timeline calls. Refactored irc methods to be extensible! Disabled auto refresh. Added manual refresh. Added s3cr3ts.'
helptext='Available commands: <!txt>/<le touhou memes>, <!latest>, <!tttrefresh>, <!tttcl>, <!ttthelp>'

botTuple=[botname,version,changelog,helptext]

def getLatest(screenName):
  
  t=Twitter(auth=OAuth(consumer_key=conKey,consumer_secret=conSecret,token=userToken,token_secret=tokenSecret))

  rawStatuses=t.statuses.user_timeline(screen_name=screenName,count=10,exclude_replies=True,include_rts=False)
  
  output=[]

  for entry in rawStatuses:
    output.append(entry['text'].replace('\n',' ').replace('\r',' '))
  return(output)

def generateTweets(screenName):
  
  t=Twitter(auth=OAuth(consumer_key=conKey,consumer_secret=conSecret,token=userToken,token_secret=tokenSecret))

  rawStatuses=t.statuses.user_timeline(screen_name=screenName,count=200)

  cleanStatuses=[]
  filterStatuses=[]

  for entry in rawStatuses:
    cleanStatus=entry['text'].replace("\n"," ").replace("\r"," ")
    cleanStatuses.append(cleanStatus)

  for entry in cleanStatuses:
    if entry[0] == "@":
      pass
    elif entry[0] == "[":
      pass
    elif entry[0:2] == "RT":
      pass
    elif entry[0:4] in ['http','Http','HTTP']:
      pass
    else:
      filterStatuses.append(entry)
  
  return(filterStatuses)

def runBot(twitterTuple,networkTuple,botTuple):
  
  #setup vars
  conKey,conSecret,userToken,tokenSecret=twitterTuple[0:len(twitterTuple)]
  network,port,channel,nick=networkTuple[0:len(networkTuple)]
  botname,version,changelog,helptext=botTuple[0:len(botTuple)]
  
  #setup twitter respknses
  dioTriggers=['!dio','!DIO','it was me, Dio!']
  dioResponses=['Mudada!','Muda Muda Muda!','How many breads have you eaten in your life?','Would a monkey dare fight a man?','Toki wa tomare. Time has stopped.','Checkmate da!','Road roller da!','WRYYYYYYYYYYYYYYYYYYYYYYYYY','Useless!','Za warudo!','ZA WALDO','The World. Time has stopped.','It\'s not enough that I should succeed -- others should fail.','*spits on father\'s grave*']
  
  txtTriggers=['!txt','le touhou memes']
  txtResponses=generateTweets('touhoudottxt')
  
  latestTriggers=['!latest']
  latestResponses=getLatest('touhoudottxt')

  sackTriggers=['!sack','!gamesack']
  sackResponses=generateTweets('GameSack')
 
  drilTriggers=['!dril','!wint']
  drilResponses=generateTweets('dril')

  deuxTriggers=['!deux','!molydeux']
  deuxResponses=generateTweets('petermolydeux')
   
  #setup irc connection
  irc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  irc.connect((network,port))
  print(irc.recv(4096))

  irc.send(bytes('NICK '+nick+'\r\n','UTF-8'))
  irc.send(bytes('USER 2humemes 2humemes 2humemes :Python IRC\r\n','UTF-8'))
  irc.send(bytes('JOIN '+channel+'\r\n','UTF-8'))
  irc.send(bytes('PRIVMSG '+channel+' :Take it easy!\r\n','UTF-8'))

  #generic bot behavior
  def respondTo(irc,channel,data,triggerArray,responseArray):
    for trigger in triggerArray:
      if data.find(bytes(trigger,'UTF-8'))!=-1:
        irc.send(bytes('PRIVMSG '+channel+' :'+random.choice(responseArray)+'\r\n','UTF-8'))
 
  while True:
    data=irc.recv(4096)
    if data.find(bytes('PING','UTF-8'))!=-1:
      irc.send(bytes(('PONG '+data.split()[1].decode('UTF-8')+'\r\n'),'UTF-8'))
    if data.find(bytes('!tttrefresh','UTF-8'))!=-1:
      irc.close()
      runBot(twitterTuple,networkTuple,botTuple)
    if data.find(bytes('!tttcl','UTF-8'))!=-1:
      irc.send(bytes('PRIVMSG '+channel+' :'+botname+' v'+version+'\r\n','UTF-8'))
      irc.send(bytes('PRIVMSG '+channel+' :'+changelog+'\r\n','UTF-8'))
    respondTo(irc,channel,data,['!ttthelp'],[helptext])
    respondTo(irc,channel,data,dioTriggers,dioResponses)
    respondTo(irc,channel,data,txtTriggers,txtResponses)
    respondTo(irc,channel,data,latestTriggers,latestResponses)
    respondTo(irc,channel,data,sackTriggers,sackResponses)
    respondTo(irc,channel,data,drilTriggers,drilResponses)
    #respondTo(irc,channel,data,wolfpupyTriggers,wolfpupyResponses)
    respondTo(irc,channel,data,deuxTriggers,deuxResponses)
    #respondTo(irc,channel,data,joeTriggers,joeResponses)
    #respondTo(irc,channel,data,daveTriggers,daveResponses)
    print(data)

runBot(twitterTuple,networkTuple,botTuple)


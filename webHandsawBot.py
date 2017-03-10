from commands import getoutput
from HTMLParser import HTMLParser
from datetime import datetime
from time import sleep

# John Hakala, 3/10/2017

class webHandsawParser(HTMLParser):

    def __init__(self):
         HTMLParser.__init__(self)
         self.data = []
    def handle_data(self, data):
         if not data.isspace() and not "Showing last 50000 lines of logcollector logs" in data :
              self.data.append(data.strip())
    def clearLogs(self):
         self.data = []
parser = webHandsawParser()

def checkPage():
  parser.clearLogs()
  # you need to set up a tunnel on port 1081 for this
  page = getoutput('curl --proxy socks5h://localhost:1081 "http://hcalmon.cms/cgi-bin/webHandsaw_beta/viewLogs.py?numberOfLines=50000&systemName=P5_beta&filter=ERROR"')
  # Sort of hackish, but I couldn't figure out to get urllib2 to work with a socks proxy....
  
  lineNumber = 0;
  foundBeginning = False
  foundEnd = False
  for line in page.splitlines():
    if not "<tt>" in line and not foundBeginning:
      continue
    elif "</tt>" in line:
      break
    else:
      foundBeginning = True
      lineNumber += 1
      parser.feed(line)

def sendSlackMessage(message):
  incantation = "curl -X POST -H 'Content-type: application/json' --data '{"
  incantation += '"text":"Found this new error in webHandsaw! ```%s```"}' % message
  # this needs to point to the slack url for our websocket
  #incantation += "' https://hooks.slack.com/services/###SANITIZED###''"
  print getoutput(incantation)
  
cachedLogs = []
firstTime = True
while True:
  sleep(2)
  print "cachedLogs is:"
  print cachedLogs
  print "all logs:"
  checkPage()
  print parser.data
  newLogs = []
  foundNewLogs=False
  for log in parser.data: 
    if not log in cachedLogs or foundNewLogs:
      newLogs.append(log) 
      foundNewLogs = True
  if newLogs:
    print "new logs!"
    print newLogs
  else:
    print "no new logs!"
  if not firstTime:
    if newLogs:
      print "now send a slack message!"
      sendSlackMessage(''.join(newLogs))
  else:
    firstTime = False
    #sendSlackMessage("John is starting up a webHandsaw bot trial run! Skynet construction underway.")
  cachedLogs = parser.data

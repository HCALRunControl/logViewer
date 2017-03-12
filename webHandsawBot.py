from commands import getoutput
from HTMLParser import HTMLParser
from datetime import datetime
from HTMLParser import HTMLParser
from time import sleep

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
  #curl -k --socks5-hostname localhost:1080 http://hcalmon.cms/index.html
  page = getoutput('curl -s -k --socks5-hostname localhost:1080 "http://hcalmon.cms/cgi-bin/webHandsaw_beta/viewLogs.py?numberOfLines=75000&systemName=P5_beta&filter=ERROR"')
  
  lineNumber = 0;
  foundBeginning = False
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
  incantation += "' https://hooks.slack.com/services/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''"

  print getoutput(incantation)
  
cachedLogs = []
firstTime = True
while True:
  sleep(10)
  checkPage()
  newLogs = []
  foundNewLogs=False
  for log in parser.data: 
    if not log in cachedLogs or foundNewLogs:
      newLogs.append(log) 
      foundNewLogs = True
  if newLogs:
    print "new logs!"
    print newLogs
  if not firstTime:
    if newLogs:
      print "now send a slack message!"
      sendSlackMessage(' '.join(newLogs))
  else:
    print "webHandsawBot is up! parser has this:"
    print parser.data
    firstTime = False
    #sendSlackMessage("John is starting up a webHandsaw bot trial run! Skynet construction underway.")
  cachedLogs = parser.data

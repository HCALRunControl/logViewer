import sys
from commands import getoutput
from HTMLParser import HTMLParser
from datetime import datetime
from HTMLParser import HTMLParser
from time import sleep
import json
import requests
reload(sys)
sys.setdefaultencoding('utf-8')


class webHandsawParser(HTMLParser):

    def __init__(self):
         HTMLParser.__init__(self)
         self.data = []
    def handle_data(self, data):
         print "handling data:", data
         if not data.isspace() and not "Showing last 75000 lines of LogCollector logs." in data :
              self.data.append(data.strip())
    def clearLogs(self):
         self.data = []
parser = webHandsawParser()

webHandsawDown = False;
def checkPage():
  global webHandsawDown
  parser.clearLogs()
  #curl -k --socks5-hostname localhost:1080 http://hcalmon.cms/index.html
  page = getoutput('curl -s -k --socks5-hostname localhost:1080 "http://hcalmon.cms/cgi-bin/webHandsaw_beta/viewLogs.py?numberOfLines=75000&systemName=P5_beta&filter=ERROR"')
  if page == "" and not webHandsawDown:
    webHandsawDown = True
    sendSlackMessage("webHandsawBot was unable to contact webHandsaw! Please check that webHandsaw is working and that the ssh tunnel from cmshcalweb01 to hcalmon is up.")
    
  else: 
    if webHandsawDown is True:
      sendSlackMessage("webHandsawBot has reestablished a connection to webHandsaw.")
    webHandsawDown=False;
    lineNumber = 0;
    foundBeginning = False
    for line in page.splitlines():
      if not "<tt>" in line and not foundBeginning:
        continue
      elif "</tt>" in line:
        break
      else:
        print "found beginning of logs:", line
        foundBeginning = True
        lineNumber += 1
        parser.feed(line)
        print "fed line to parser, parser has", parser.data

def sendSlackMessage(message):
  #incantation = "curl -X POST -H 'Content-type: application/json' --data '{"
  #incantation += '"text":"Found this new error in webHandsaw! ```%s```"}' % message
  #incantation += "' https://hooks.slack.com/services/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''"

  #print getoutput(incantation)
  
  # Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
  webhook_url = 'https://hooks.slack.com/services/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'
  slack_data = {'text': "Found this new error in webHandsaw! ```%s```" % message}
  
  response = requests.post(
      webhook_url, data=json.dumps(slack_data),
      headers={'Content-Type': 'application/json'}
  )
  if response.status_code != 200:
    print 'Request to slack returned an error %s, the response is:\n%s' % (response.status_code, response.text)
    return False
  else:
    return True
  
cachedLogs = []
firstTime = True
webHandsawStale = False;
while True:
  sleep(10)
  checkPage()
  newLogs = []
  foundNewLogs=False
  for log in parser.data: 
    if "WEBHANDSAW WARNING" in log and not webHandsawStale:
      webHandsawStale = True
      print "webHandsawStale = True" 
      newLogs.append(log)
      foundNewLogs = True
    elif webHandsawStale and "Logs shown were last updated at" in log:
      print "unstale message found"
      if webHandsawStale:
        newLogs.append("webHandsaw logs have updated and no longer appear stale.")
      webHandsawStale = False
      if not ("WEBHANDSAW WARNING" in log or "Logs shown were last updated at" in log) and (not log in cachedLogs or foundNewLogs):
        newLogs.append(log) 
        foundNewLogs = True
    else: 
      print "log:", log
    
  if newLogs:
    print "new logs!"
    print newLogs
  if not firstTime:
    if newLogs:
      print "now send a slack message!"
      for i in range(0,5):
        print " --> send attempt %i" % i
        formattedMessage = '\n'.join(newLogs)
        formattedMessage = formattedMessage.replace("ERROR\n", "ERROR: ")
        if sendSlackMessage(formattedMessage):
          break
  else:
    print "webHandsawBot is up! parser has this:"
    print parser.data
    firstTime = False
    sendSlackMessage("\n John is hacking at webHandsaw_bot. Pay no attention to the man behind the curtain.")
  cachedLogs = parser.data

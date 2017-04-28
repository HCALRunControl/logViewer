#!/usr/bin/python
import re
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
from datetime import datetime
from commands import getoutput
from ansi2html import ansi2html
from logHtml import *
from ConfigParser import ConfigParser

# John Hakala, 2/25/17
# this pyCGI script looks at the log copy (symlink) from logCopy.py
# then, it runs tail to grab a certain number of lines from the log copy's end
# then, it feeds those lines to Handsaw, which spits back an ansi-formatted version of the logs
# ansi2html is used to convert the ansi into html format
# the output from ansi2html gets its colors changed so they're not so ugly
# logHtml's helper functions are called to grab some chunks of html, and the html is assembled
# finally, an html page is printed to stdout (which apache grabs and serves over the web)

#def checkStaleness(staleTime, logCopyName):
def checkStaleness(staleTime, logCopyName):
  logTail =  getoutput("tail -80 %s" % logCopyName)
  timestamp = datetime.fromtimestamp(float(re.findall('(?<=timestamp=).+', logTail)[-1].split(" ")[0].replace('"', ''))/1000)  
  age = (datetime.now()-timestamp).total_seconds()
  if age > staleTime:
    return "\n<br><span style='background-color: brown; color: cyan'> WEBHANDSAW WARNING! The logs appear to be stale. The newest log detected is %f seconds old. <br> Perhaps the logCopyer is down or RCMS is not writing a log at least every two minutes (it usually does this during normal operation even when no configuration is active.) </span><br>\n"  % age
  else:
    return "\n<br>Logs shown were last updated at %s \n" % timestamp.strftime("%H:%M:%S Geneva time.")
    
def getLastLogMessages(lines, filter, logCopy):

  incantation = "tail -%i %s | ~hcalpro/scripts/Handsaw.pl" % (lines, logCopy)
  if filter is not None and filter in ["INFO", "WARN", "ERROR"]:
    incantation += " --FILTER=%s" % filter
  #incantation = "tail -%i /nfshome0/elaird/errors.txt" % lines
  return  getoutput(incantation)

def changeColors(styledLine):
  styledLine = styledLine.replace('background-color:#00CD00', 'background-color:#00ae00; color:#ffffff')
  styledLine = styledLine.replace('background-color:#CD0000', 'background-color:#dd3844; color:#ffffff')
  styledLine = styledLine.replace('background-color:#00CDCD', 'background-color:#4c77aa; color:#ffffff')
  styledLine = styledLine.replace('background-color:#CD00CD', 'background-color:#000000; color:#ff3333')
  styledLine = styledLine.replace('background-color:#CDCD00', 'background-color:#e8e866')
  return styledLine
  
def formatMessages(messages, staleTime, logCopy):
  formattedMessages = "    <br><tt>\n%s    <br>" % checkStaleness(staleTime, logCopy)
  for line in messages.splitlines():
    formattedMessages += changeColors(ansi2html(line, "xterm"))
    formattedMessages+="\n    <br>"
  formattedMessages += "    </tt>"
  return formattedMessages

def getBody(numLines, filtLev, sysName):
  config = ConfigParser()
  config.read("webHandsaw_conf.ini")
  body  = getHeader(config.get(sysName, "webHandsaw html subdirectory" ))
  body +=  "    <!-- begin body -->\n"
  if not sysName in (config.sections()):
    body += "the system specified was not found: <tt>%s</tt>" % sysName
  elif numLines is not None and (isinstance(numLines, int) or isinstance(numLines, str)):
    try: 
      nLines = int(numLines)
      if nLines > 0:
        logCopyName = "%s/log_copy.xml" % config.get(sysName, "Log copy directory")
        body += "    Showing last %i lines of LogCollector logs. <br>" % nLines
        body += formatMessages( getLastLogMessages(nLines, filtLev, 
                                                  logCopyName,
                                                 ),
                                float(config.get(sysName, "Log staleness timeout")),
                                logCopyName
                              )
      else:
        body += "    the numberOfLines submitted seems to be a weird number: <tt> %s </tt>" % str(numLines)
    except ValueError:
        body += "    the numberOfLines submitted does not seem to be a number <tt> %s </tt>" % str(numLines)
  else:
    if numLines is None:
      body += "\n    <strong> you must select a number of lines to display.</strong>"
    else:
      body += "\n    <strong> something looks fishy about the number of lines requested:</strong> <tt>%r</tt>" % numLines
  body += "\n    <!-- body end -->"
  return body

form = cgi.FieldStorage()
numberOfLines =  form.getvalue('numberOfLines')
systemName =  form.getvalue('systemName')
filterLevel =  form.getvalue('filter')

html = getBody(numberOfLines, filterLevel, systemName)
html += getFooter()

print "Content-type: text/html"
print
print html

#!/usr/bin/python
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
from commands import getoutput
from ansi2html import ansi2html
from logHtml import *

# John Hakala, 2/25/17
# this pyCGI script looks at log copy (symlink) from logCopy.py
# then, it runs tail to grab a certain number of liens from the log copy's end
# then, it feeds it to Handsaw, which spits back an ansi-formatted version of the logs
# it uses ansi2html to convert this into html format
# then it changes the colors so they're not so ugly
# and finally it spits out an html page to stdout (which apache grabs and serves over the web)
# some chunks of html are gotten from the helper functions in logHtml.py

def getLastLogMessages(lines, filter):
  logCopyName = "~johakala/logCopyer/log_copy.xml"
  incantation = "tail -%i %s | ~hcalpro/scripts/Handsaw.pl" % (lines, logCopyName)
  if filter is not None and filter in ["INFO", "WARN", "ERROR"]:
    incantation += " --FILTER=%s" % filter
  #incantation = "tail -%i /nfshome0/elaird/errors.txt" % lines
  return getoutput(incantation)

def changeColors(styledLine):
  styledLine = styledLine.replace('background-color:#00CD00', 'background-color:#00ae00; color:#ffffff')
  styledLine = styledLine.replace('background-color:#CD0000', 'background-color:#dd3844; color:#ffffff')
  styledLine = styledLine.replace('background-color:#00CDCD', 'background-color:#4c77aa; color:#ffffff')
  styledLine = styledLine.replace('background-color:#CDCD00', 'background-color:#e8e866')
  return styledLine
  
def formatMessages(messages):
  formattedMessages = "    <br><tt>\n    <br>"
  for line in messages.splitlines():
    formattedMessages += changeColors(ansi2html(line, "xterm"))
    formattedMessages+="\n    <br>"
  formattedMessages += "    </tt>"
  return formattedMessages

def getBody(numLines, filtLev):
  body =  "    <!-- begin body -->\n"
  if numLines is not None and (isinstance(numLines, int) or isinstance(numLines, str)):
    try: 
      nLines = int(numLines)
      if nLines > 0:
        body += "    Showing last %i lines of logcollector logs" % nLines
        body += formatMessages(getLastLogMessages(nLines, filtLev))
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
filterLevel =  form.getvalue('filter')

html =  getHeader()
html += getBody(numberOfLines, filterLevel)
html += getFooter()

print "Content-type: text/html"
print
print html

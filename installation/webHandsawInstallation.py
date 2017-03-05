from os import path, makedirs
from ConfigParser import ConfigParser
from optparse import OptionParser
from pprint import pprint
from socket import gethostbyname, gethostname
import shutil
from generateIndex import generateIndex

# Script to install webHandsaw
# This sets up the directory structure needed for both the httpd machine and the run control machine
# use the --help option for instructions
# this is only so long because it checks very carefully that it doesn't accidentally do something bad
# like e.g. it makes sure not to overwrite anything, it checks whether it's on the correct machine or not
# it makes sure all the directory structures that should already be there are there and those that shouldn't 
# already be there aren't
#
# John Hakala, 3/5/2017

def getConfigParameters(httpdRC):
  rcParameters =    ["Run control machine", "LogCollector log", "Log copy directory"]

  httpdParameters = [
                     "httpd machine"              , "httpd installation directory" ,
                     "httpd cgi-bin directory"    , "httpd html directory"         ,
                     "webHandsaw cgi subdirectory", "webHandsaw html subdirectory" ,
                     "ansi2html.py file"
                    ]
  if not httpdRC in ["httpd", "rc"]:
    print "Error: getConfigDict was expecting 'httpd' or 'rc' to specify what system it's retrieving parameters for, but it got %s" % httpdRC
  else:
    return rcParameters if httpdRC == "rc" else httpdParameters

def getConfiguration(systemName, httpdOrRC):
  config = ConfigParser()
  config.read("webHandsaw_conf.ini")
  if systemName is None:
    print "Error: please specify the system name specified in webHandsaw_conf.ini"
    exit(1)
  elif not systemName in config.sections():
    print "Error: the system name specified was not found in webHandsaw_conf.ini." 
    exit(1)
  else:
    response = {}
    for parameter in getConfigParameters(httpdOrRC):
      response[parameter] = config.get(systemName, parameter)
    return response

def checkHost(target):
  print "requested installation machine : %s (%s)" % (target, gethostbyname(target))
  print "this machine                   : %s (%s)" % (gethostname(), gethostbyname(gethostname()))
  if gethostbyname(target) == gethostbyname(gethostname()):
    print "The requested host seems to match this machine -- good! Continuing installation..."
  else :
    print "Error: Cannot verify that this is the correct host! You should be logged into %s to run this installation!" % target
    exit(1)

def installRC(parameters):
  print "installation parameters are:" 
  pprint(parameters)
  checkHost(parameters["Run control machine"])
  if not path.exists(parameters["LogCollector log"]):
    print "Error: LogCollector log not found on this machine: %s" % parameters["LogCollector log"]
    exit(1)
  else: 
    print "Found LogCollector log at %s -- good! Continuing installation..." % parameters["LogCollector log"]
  if path.exists(parameters["Log copy directory"]):
    print "Error: Log copy directory already exists."
    exit(1)
  else:
    print "Creating log copy directory and filling it with the needed files."
    makedirs(parameters["Log copy directory"])
    for logCopyFile in ["../logCopy.py", "../mkLog1.sh", "../mkLog2.sh", "../forcelink.py"]:
      shutil.copy(logCopyFile, parameters["Log copy directory"])
    print "Installation on RC machine done."
    print "To launch log copying process on the run control machine, please run:"
    print "  cd %s; python logCopy.py &" % parameters["Log copy directory"] 
     
def installHTTPD(parameters, sysName, overwrite):
  print "installation parameters are:" 
  pprint(parameters)
  if not path.exists(parameters["ansi2html.py file"]):
    print "Error: did not find the ansi2html.py file %s" % parameters["ansi2html.py file"]
    print "You can get it from: https://github.com/Kronuz/ansi2html"
    exit(1)
  else:
    print "Found the ansi2html file %s -- good! Continuing installation..." % parameters["ansi2html.py file"]
  checkHost(parameters["httpd machine"])
  if not path.exists(parameters["httpd installation directory"]):
    print "Error: httpd install directory not found on this machine: %s" % parameters["httpd installation directory"]
    exit(1)
  else: 
    "httpd installation directory %s was found on this machine -- good! Continuing installation..." % parameters["httpd installation directory"]
  cgiBinDir = path.join(parameters["httpd installation directory"], parameters["httpd cgi-bin directory"])
  if not path.exists(cgiBinDir):
    print "Error: httpd cgi-bin directory not found on this machine: %s" % cgiBinDir
    exit(1)
  else:
    "httpd cgi-bin directory %s was found on this machine -- good! Continuing installation..."
  htmlDir = path.join(parameters["httpd installation directory"], parameters["httpd html directory"])
  if not path.exists(cgiBinDir):
    print "Error: httpd html directory not found on this machine: %s" % cgiBinDir
    exit(1)
  else:
    "httpd cgi-bin directory %s was found on this machine -- good! Continuing installation..."
  cgiBinSubdir = path.join(cgiBinDir, parameters["webHandsaw cgi subdirectory"]) 
  if overwrite:
    shutil.rmtree(cgiBinSubdir)
  if path.exists(cgiBinSubdir):
    print "Error: webHandsaw cgi subdirectory already exists in the requested location: %s" % cgiBinSubdir
    exit(1)
  else:
    print "Making directory %s for webHandsaw's pyCGI files..." % cgiBinSubdir
    makedirs(cgiBinSubdir)
  htmlSubdir = path.join(htmlDir, parameters["webHandsaw html subdirectory"])
  if overwrite:
    shutil.rmtree(htmlSubdir)
  if path.exists(htmlSubdir):
    print "Error: webHandsaw html subdirectory already exists in the requested location: %s" % htmlSubdir
    exit(1)
  else:
    print "Making directory %s for webHandsaw's pyCGI files..." % cgiBinSubdir
    makedirs(htmlSubdir)
  print "Copying the html and pyCGI files into the directories %s and %s, respectively." % (htmlSubdir, cgiBinSubdir)
  generateIndex("/%s/%s" % (parameters["httpd cgi-bin directory"], parameters["webHandsaw cgi subdirectory"]), sysName)
  htmlFiles = ["/tmp/index.html", "../webHandsaw.css", "../webHandsaw.png", "../webHandsaw_black.png"]
  cgiBinFiles = ["../viewLogs.py", "../logHtml.py", "../forcelink.py", parameters["ansi2html.py file"], "webHandsaw_conf.ini"]
  for htmlFile in htmlFiles:
    shutil.copy(htmlFile, htmlSubdir)
  for cgiBinFile in cgiBinFiles:
    shutil.copy(cgiBinFile, cgiBinSubdir)
  print "Installation on httpd machine done."
  print "The splash page should be visible at: %s.[network]/%s" % (parameters["httpd machine"], parameters["webHandsaw html subdirectory"])

if __name__ == "__main__":
  optParser = OptionParser()
  optParser.add_option("-s", "--system_name", dest="system_name",
                       help = "The system name to install. They are specified in webHandsaw_conf.ini" )
  optParser.add_option("-w", "--httpd_or_rc", dest="httpd_or_rc",
                       help = "What this script will try to install: %s"
                            % "either 'httpd' to install httpd-side stuff %s" 
                            % "or 'rc' to install the run-control machine side stuff"                 )
  optParser.add_option("-o", action="store_true", dest="overwrite", default="False",
                       help = "Use -o during httpd machine installation if you want to overwrite %s"
                            % "a preexisting installation of webHandsaw."                             )
  (options, args) = optParser.parse_args()

  if options.httpd_or_rc is None: 
    print "Error: you must specify whether you are installing on the httpd machine or the rc machine."
    exit(1)
  elif not options.httpd_or_rc in ["httpd", "rc"]:
    print "Error: the httpd_or_rc option must be either 'httpd' or 'rc'. Requested: %s" % options.httpd_or_rc
    exit(1)
        
  installParameters = getConfiguration(options.system_name, options.httpd_or_rc)

  if options.httpd_or_rc == "rc":
    installRC(installParameters)
  elif options.httpd_or_rc == "httpd":
    installHTTPD(installParameters, options.system_name, options.overwrite)

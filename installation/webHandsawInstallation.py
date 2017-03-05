from os import path, makedirs
from ConfigParser import ConfigParser
from optparse import OptionParser
from pprint import pprint
from socket import gethostbyname, gethostname
import shutil

def getConfigParameters(httpdRC):
  rcParameters =    ["Run control machine", "LogCollector log", "Log copy directory"]

  httpdParameters = [
                     "httpd machine"              , "httpd installation directory" ,
                     "httpd cgi-bin directory"    , "httpd html directory"         ,
                     "webHandsaw cgi subdirectory", "webHandsaw html subdirectory"
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
     
def installHTTPD(parameters):
  print "installation parameters are:" 
  pprint(parameters)
  checkHost(parameters["httpd machine"])

if __name__ == "__main__":
  optParser = OptionParser()
  optParser.add_option("-s", "--system_name", dest="system_name",
                       help = "The system name to install. They are specified in webHandsaw_conf.ini")
  optParser.add_option("-w", "--httpd_or_rc", dest="httpd_or_rc",
                       help = "What this script will try to install: %s"
                            % "either 'httpd' to install httpd-side stuff %s" 
                            % "or 'rc' to install the run-control machine side stuff"
                      )
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
    installHTTPD(installParameters)

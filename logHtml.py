# helper functions to spit out chunks of html for viewLogs.py
# John Hakala 3/2/2017

def getHeader(subDir):
  header = """
<html>
  <head>
     <title>webHandsaw -- HCAL logs</title>
     <link href="https://fonts.googleapis.com/css?family=Open+Sans:400italic,600italic,700italic,400,600,700" rel="stylesheet" type="text/css">
     <link rel="stylesheet" type="text/css" href="/%s/webHandsaw.css"> 
     <link rel="icon" type="image/png" href="/%s/webHandsaw_black.png">
     <script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
     <!-- <script src="/%s/contrast.js"></script> -->
  </head>
  <!-- <body onload="setContrast();">
         do this in the python -->
  <body>
    <div id="top"><img src="/%s/webHandsaw.png" width="50px"><h1>webHandsaw</h1></div>
    <div id="wrapper">
    <!-- end header -->
""" % (subDir, subDir, subDir, subDir)
  return header

def getFooter():
  footer =  """
    <!-- begin footer -->
    </div>
  </body>
</html>
"""
  return footer



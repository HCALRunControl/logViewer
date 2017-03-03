# helper functions to spit out chunks of html for viewLogs.py
# John Hakala 3/2/2017

def getHeader():
  header = """
<html>
  <head>
     <link href="https://fonts.googleapis.com/css?family=Open+Sans:400italic,600italic,700italic,400,600,700" rel="stylesheet" type="text/css">
     <link rel="stylesheet" type="text/css" href="/jhakala/webHandsaw.css"> 
     <script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
     <!-- <script src="/jhakala/contrast.js"></script> -->
  </head>
  <!-- <body onload="setContrast();">
         do this in the python -->
  <body>
    <div id="top"><img src="/jhakala/webHandsaw.png" width="50px"><h1>webHandsaw</h1></div>
    <div id="wrapper">
    <!-- end header -->
"""
  return header

def getFooter():
  footer =  """
    <!-- begin footer -->
    </div>
  </body>
</html>
"""
  return footer



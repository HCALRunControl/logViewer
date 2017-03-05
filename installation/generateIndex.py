def generateIndex(relativeURL, systemName):
  oldIndex = open("../index.html", "r")
  newIndex = open("/tmp/index.html", "w")
  for line in oldIndex.readlines():
    if "__REPLACE_ME__" in line:
      line = line.replace("__REPLACE_ME__", relativeURL)
    if "__ALSO_REPLACE_ME__" in line:
      line = line.replace("__ALSO_REPLACE_ME__", systemName)
    newIndex.write(line)
  oldIndex.close()
  newIndex.close()
  

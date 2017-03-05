## webHandsaw

To install webHandsaw on a system like P5 or 904, one must edit `webHandsaw_conf.ini` to specify the installation setup. Then, one must run the webHandsawInstallation.py script on both the httpd machine and the run control machine.

On the httpd machine:
```
python webHandsawInstallation.py -w httpd -s MY_System_Name
```
On the run control machine:
```
python webHandsawInstallation.py -w rc -s MY_System_Name
```
The `ansi2html.py` file can be taken from [here](https://github.com/Kronuz/ansi2html).

To start the tool, the apache server must be running on the apache httpd machine, and the logCopy script must be started on the run control machine:
```
python logCopy.py &
```

Technical notes are in code comments.

The source files are arranged like this after running the install script:
```
httpd machine:
  /var/www
    /cgi-bin/<webHandsawDirsName>
      viewLogs.py
      logHtml.py
      ansi2html.py
    /html/<webHandsawDirsName>
      index.html
      shifterHomePage.css

run control machine:
  <nfshome0Dir>
     logCopy.py
     mkLog1.sh
     mkLog2.sh
     forcelink.py
```

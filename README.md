## webHandsaw

To install webHandsaw on a system like P5 or 904, one must edit `webHandsaw_conf.ini` to specify the installation setup. Then, one must run the `webHandsawInstallation.py` script on both the httpd machine and the run control machine.

On the httpd machine:
```
python webHandsawInstallation.py -w httpd -s My_System_Name
```
On the run control machine:
```
python webHandsawInstallation.py -w rc -s My_System_Name
```
The `ansi2html.py` file can be taken from [here](https://github.com/Kronuz/ansi2html).

To start the tool, the apache server must be running on the apache httpd machine, and the logCopy script must be started on the run control machine:
```
python logCopy.py &
```

The webHandsawBot can be run on cmshcalweb01 as follows:
```
ssh -f -ND 1080 <your_cmsusr_username>@cmsusr
nohup python -u webHandsawBot.py > webHandsawBot.log 2>&1 &
```
Note that the webhook url has to be changed in the code for the bot to work (it has been removed from the code in github to prevent random flooding).



Technical notes are in code comments.

The source files for webHandsaw and the logCopyer are arranged like this after running the install script:
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



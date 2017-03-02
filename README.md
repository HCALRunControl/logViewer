## webHandsaw

To deploy at systems like P5 or 904, the source files must be arranged like this:
```
httpd machine:
  /var/www:
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

The `ansi2html.py` file can be taken from [here](https://github.com/Kronuz/ansi2html).

The way it is currently set up at P5 has `<nfshome0Dir> == ~johakala/logCopyer` and `<webHandsawDirsName> == jhakala` pending an official release. These are currently hardcoded in, so deploying webHandsaw elsewhere requires edits to the code to point at the right directories.

To start the tool, the apache server must be running on the apache httpd machine, and the logCopy script must be started on the run control machine:
```
python logCopy.py &
```

Technical notes are in code comments.

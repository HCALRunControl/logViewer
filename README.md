## webHandsaw

To deploy at systems like P5 or 904, the source files must be arranged like this:
```
apache machine:
  /var/www:
    /cgi-bin/<webHandsawDir>
      viewLogs.py
      logHtml.py
      ansi2html.py
    /html/<logViewerDir>
      index.html
      shifterHomePage.css

run control machine:
  <nfshome0Dir>
     logCopy.py
     mkLog1.sh
     mkLog2.sh
```

The way it is currently set up at P5 has `<nfshome0Dir> == ~johakala/logCopyer` and `<webHandsawDir> == jhakala` pending an official release. These are currently hardcoded in, so deploying webHandsaw elsewhere requires edits to the code to point at the right directoriess.

Technical notes are in code comments.

#!/usr/bin/env python
'''This is a test to parse a form with data that was pre-filled.'''

import sys
import os
import sqlite3
import mycgi
from MyFile import *

form = mycgi.Form()

# "term" "fname" and "thoughts" are the fields we'll parse

def return_page(term,fname,thoughts):
    w('Got to return_page()')
    myfile.close()
    myhtml = '''
<html><head>
  <meta charset="utf-8" />
  <title>Test form input</title>
  <link rel="stylesheet" href="/css/change.css"/>
  <script>
    function verify_del(fileid)  {
       alert("He made the call to verify_del!");
       return false;
    }
    function verify_edit(fileid) {
       alert("He called verify_edit!");
       return false;
    }
  </script></head>'''

    myhtml += f'''
    <body>
    <h2>This is what was returned by the form in &quot;testform&quot;</h2>
    <table>
    <tr><th>form label</th><th>default</th><th>actual value</th></tr>
    <tr><td>term</td><td>Insurance</td><td>{term}</td></tr>
    <tr><td>fname</td><td>Fred</td><td>{fname}</td></tr>
    <tr><td>thoughts</td><td>This is just filler substance because I don&apos;t know &quot;lorem ipsum sicut alium,&quot; and do not care to learn now.</td><td>{thoughts}</td></tr>
    </table>
    <hr /><br />
    </body></html>'''

    print('Content-type: text/html\n\n')
    print(myhtml)
    return 0 # never reached, so who cares?



def main():
    w('I hope this writes a debug file. I just entered main()\n')
    term = form.getvalue('term')
    fname = form.getvalue('fname')
    thoughts = form.getvalue('thoughts')
    w('...about to call "return_page()"')
    return_page(term, fname, thought)
    return 0

if __name__ == '__main__':
    rv=main()

#!/usr/bin/env python
'''This program will receive a fileid argument as a get string, viz. "<url>?fileid=1009".
   Then it looks up that record in the files database. It displays that record.
   Later, we want this program to handle Edit and Delete requests. '''

import sys
import os
import mycgi
import sqlite3

from MyFile import *

# form = mycgi.Form()

def parse_GET():
    q = os.environ.get('QUERY_STRING','There is no query string')
    if not q.startswith('fileid='):
        # Do some kind of error message
        w('** We errored out on the fileid int conversion.\n')
   
        return None
    else:
        n = q.index('=')
        fileident = q[n+1:]
        return int(fileident)

def return_html_page(record: tuple):
    w('In return_html_page, loading up all the values...\n')
    fileid = int(record[0])
    sd = record[1]
    ld = record[2]
    lo = record[3]
    dt = record[4]
    owner = record[5]
    comments = record[6]
    w('\n...finished loading the values.\n')
    w('\n...about to start creating the html page...\n')
    myhtml = '''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8" />
<title>onerec</title>
<link rel="stylesheet" href="/css/entry.css" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Sriracha&display=swap');
	
    body {
		margin: 10px;
		box-sizing: border-box;
		background-color: #e1e1e1;
    }
	
    header {
      display: flex; 
      background-color: rgb(75,70,70);
      color: #e1f1f1;
      font-size:10pt;
      font-family: Arial,sans-serif;
    }	


	h1 {
		color: #004066;
	}
	
	h2 {
		color: #004066;
	}
    
    table,th,td { border: 1px solid black; color: #004066; }
        th,td { padding-left: 15px;
                padding-right: 15px; color: #004066; }
	p {
		color: #004066;
		font-size: 16pt;
		margin: 12px;
	}

	a {
		text-align: left;
		padding-right: 25px;
		padding-left: 0;
		color: navy;
	}
	.main {
/*		display: flex; */
		justify-content: center;
		align-items: center;
/*		width: 50% */
		color: #004066;
		padding: 20px 10px;
	}
	.main h1 {
		color: #004066;
		text-align: center;
		font-family: 'Sriracha', cursive;
		text-decoration: none;
		margin-left: 75px;
	}
	.main p {
		color: #004066;
		font-size: 20px;
		text-align: left;
		font-family: 'Sriracha', cursive;
		left-margin: 75px;
	}
	.copy {
		position: relative;
		justify-content: left;
		align-items: bottom;
		padding: 0px 20px;
	}
	.copy-text p {
		position: absolute;
		font-size: 7pt;
		font-weight: bold;
		color: black;
		margin: 10px 0;
		bottom: auto;
	}
     </style>
    <script>
    function gohome() {
      location.href = "/menu.html";
    }
    </script>
   </head>'''

    w('...wrote out the header of the new page.\n')
    
    myhtml += f'''
 <body><nav><a href="/menu.html">Home (Menu)</a><a href="/lookup.html">Look up a file</a>
<a href="/report.html">View all files</a></nav>
<header>This form will prompt you to delete the record in the sql database</header>
<h2>Record {fileid}</h2>'''
    
    w('\n...about to create the table.\n')
    
    myhtml += f'''
<table><tr><th>Field</th><th>Value</th></tr>
       <tr><td>File id:</td><td>{fileid}</td></tr>
       <tr><td>Contents:</td><td>{sd}</td></tr>
       <tr><td>More details:</td><td>{ld}</td></tr>
       <tr><td>Location:</td><td>{locations[lo]}</td></tr>
       <tr><td>Created on:</td><td>{dt}</td></tr>
       <tr><td>Owner:</td><td>{owner}</td></tr>
       <tr><td>Comments:</td><td>{comments}</td></tr>
</table>'''
    w('...created the table!\n')
    myhtml += f'''
<hr /><p>Are you sure you want to delete this record?</p>
<form method="post" action="deleterec.py">
  <input type="submit" id="submit" name="submit" value="yes" />&nbsp;
  <input type="submit" id="submit" name="submit" value="no" /><br />
  <input type="hidden" id="fileid" name="fileid" value={fileid} />
        </form>
    	<br />
	<button name="menu" id="menu" onclick="location.href='/menu.html';">Menu</button>
		<br />
	<div class="copy">
          <div class="copy-text">
	    <p>&copy; 2024 Kevin Baumgarten, All rights reserved.</p>
	  </div>
       </div>
'''
    print('Content-type: text/html\n\n')
    print(myhtml)

     
def onerec(fileid: int):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        sql = f"SELECT * FROM newfiles WHERE fileid={fileid}"
        cur.execute(sql)
        row = cur.fetchone()
        con.close()
    except Exception as e:
        tup = sys.exc_info()
        return_simple_error_page(e)
        sys.exit(1)
    else:
        return_html_page(row)

def main():
    w(f'Starting main() in {prog}.\n')
    fileid = parse_GET()
    w(f'{fileid=}\n')
    if fileid:
        rv=onerec(fileid)
    else:
        return 99


def return_simple_error_page(e,tup):
    myhtml = f'''
<html><body style="bgcolor: black; color:lightred">
    <h1><center>An Exception has been encountered.</center></h1>
    <h5><center>Please try again later</center></h5>
    <p>{e}</p>
    <p>{tup[0]}: {tup[1]}</p>
    <hr />
</body><html>'''
    print('Content-type: text/html\n\n')
    print(myhtml)

############################################################################################

if __name__ == '__main__':
    w('-' * 66)
    w('\n')
    w(f'Debugging {prog} on {longdate} at {thetime()}.\n\n')
    rv = main()
    sys.exit(rv)

#!/usr/bin/env python
'''This program will receive a fileid argument as a get string, viz. "<url>?fileid=1009".
   Then it looks up that record in the files database. It displays that record.
   Later, we want this program to handle Edit and Delete requests. '''

import sys
import os
import mycgi
import sqlite3

from MyFile import *


# Updated on: Friday, July	 5, 2024 17:44:11  .
# Updated: Thursday, July 11, 2024 15:51:53  .

form = mycgi.Form()

def parse_GET():
	w('...entered parse_GET()\n')
	q = os.environ.get('QUERY_STRING','There is no query string')
	w(f'GET string = {q}\n')
	if not q.startswith('fileid='):
		# Do some kind of error message
		w('** We errored out on the fileid int conversion.\n')
		w(f'Query String = {q}\n')
		return None
	else:
		n = q.index('=')
		fileident = q[n+1:]
		return int(fileident)
	
def next_fileid(fid: int) -> int:
#	 w(f'\n..entering next_fileid on {today} at {now()}\n')
#	 w(f'curr. fileid = {fid}\n\n)'
	con = sqlite3.connect(db)
	cur = con.cursor()
	sql = f'SELECT fileid FROM newfiles WHERE fileid > {fid} LIMIT 1'
	cur.execute(sql)
	t = cur.fetchone()
	con.close()
#	 return t[0]
	return fid if t is None else int(t[0])
  
def prev_fileid(fid: int):
	con = sqlite3.connect(db)
	cur = con.cursor()
	sql = f'SELECT fileid FROM newfiles WHERE fileid < {fid}'
	cur.execute(sql)
	l = cur.fetchall()
	con.close()
	return fid if not l else int(l[-1][0])

def main_menu():
	redirect='<html><head><meta http-equiv="refresh" content="0;url=/menu.html"></head><body><p>Redirecting to menu.html...</p></body></html>'
	
	print('Content-Type: text/html\n\n')
	print(redirect)
	return 0
	
def report_py():
	redirect='<html><head><meta http-equiv="refresh" content="0;url=/cgi-bin/report.py"></head><body><p>Redirecting to menu.html...</p></body></html>'
	
	print('Content-Type: text/html\n\n')
	print(redirect)
	return 0
	
	
def htmlpage(thefile):
	w('\n...entered htmlpage()\n')
	
	myhtml = '''
<!DOCTYPE html><html lang="en"><head><meta charset="utf-8" /><title>onerec</title>
<link rel="stylesheet" href="/css/entry.css" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
  <style>
	@import url('https://fonts.googleapis.com/css2?family=Sriracha&display=swap');
body { margin: 10px; box-sizing: border-box; background-color: #e1e1e1; }
header { display: flex; background-color: #navy; color: #e1e1e1; font-size:10pt;
		 font-family: "Georgia","Verdana","Sriracha",cursive,sans-serif; align-items: left; padding-top: 5px;
		 padding-left: 5px; }
nav { display: flex; background-color: lightblue; color: #004066;
	  font-family: ""Georgia","Sriracha",cursive,sans-serif;
	  font-size: 12pt; }								
a { color: #004066;	 background-color:	lightblue; padding-right: 20px; font-size: 12pt; }
nav.nav { display: flex; background-color: lightblue; color: #004066; font-family: "Georgia","Lucida Sans",sans-serif;
	font-size: 12pt; }
/*	background-color: #81f0b0; */
a.nav {	color: #004066;	padding-right: 20px; font-size: 12pt;
		background-color:  lightblue; }

h1,h2,h3,h4,h5 { color: #004066; }
table,th,td { border: 2px solid black; color: #004066; }
th,td { justify: center; padding-left: 20px; padding-right: 20px; }
table.navbuttons, td.navbuttons { border: 0; }
p { color: #004066; font-size: 16pt; margin: 12px; }
.copy {	position: relative; justify-content: left; align-items: bottom;	padding: 50px 10px; }
.copy-text p { position: absolute; font-size: 7pt; font-weight: bold; color: black; margin: 10px 0; bottom: auto; }
</style></head>'''

	w('...wrote out the header of the new page.\n')
	
	myhtml += f'''
 <body>
	<header>Details of the file and options to change or delete the file from the database</header>
	<nav><a href="/menu.html">Home</a><a href="/lookup.html">Look up a file</a>
	<a href="/cgi-bin/report.py">View all files</a><a href="/cgi-bin/report.py">Edit or Delete</a></nav>
	
<h2>Record {thefile.fileid}</h2>'''
	
	w('\n...about to create the table.\n')
	
	# first, get the dates into the correct format
	if thefile.dt is None:
		dt = thefile.dt
	else:
		dt = ymd2dt(thefile.dt)
	cr = ymd2dt(thefile.cr)
	
	myhtml += f'''
<table><tr><th>Field</th><th>Value</th></tr>
  <tr><td>File id:</td><td>{thefile.fileid}</td></tr>
  <tr><td>Contents:</td><td>{thefile.sd}</td></tr>
  <tr><td>More details:</td><td>{thefile.ld}</td></tr>
  <tr><td>Location:</td><td>{locations[thefile.lo]}</td></tr>
  <tr><td>Owner:</td><td>{thefile.owner}</td></tr>
  <tr><td>Comments:</td><td>{thefile.comments}</td></tr>
  <tr><td>Created on:</td><td>{cr}</td></tr>'''
	if dt is not None:
		myhtml += f'<tr><td>Updated on:</td><td>{dt}</td></tr>'
	myhtml += '</table>'
	
	w('...created the table!\n')
	# get the next and previous file ids:
	nextid = next_fileid(thefile.fileid)
	w(f'{nextid = }\n')
	previd = prev_fileid(thefile.fileid)
	w(f'{previd = }\n')
	myhtml += f'''
<hr /><p>Choose the next step:</p>

<table class="navbuttons">
<tr><td class="navbuttons"><center><button id="edit" name="edit" onclick="location.href='/cgi-bin/edit.py?fileid={thefile.fileid}';" />Edit</button></center></td>
<td class="navbuttons"><center><button id="del" name="del" onclick="location.href='/cgi-bin/confirmdel.py?fileid={thefile.fileid}';" />Delete</button></center></td></tr>
<tr><td class="navbuttons" colspan="2"></td></tr>
<tr><td class="navbuttons"><center><button id="prev" name="prev" onclick="location.href='/cgi-bin/onerec.py?fileid={previd}';">&lArr;Previous</button></center></td>
<td class="navbuttons"><center><button id="next" name="next" onclick="location.href='/cgi-bin/onerec.py?fileid={nextid}';">Next&rArr;</button></center></td></tr>
<tr><td class="navbuttons" colspan="2"></td></tr>
<tr><td class="navbuttons"><center><button name="menu" id="menu" onclick="location.href='/menu.html';">Home</button></center></td><td class="navbuttons"><center><button id="print" name="print" onclick="location.href='/cgi-bin/temppage.py';">Print</button></center></td></tr>
</table>
<br /><br /><br />
<div class="copy"><div class="copy-text">
<p>&copy; 2024 Kevin Baumgarten, All rights reserved.</p>
</div></div></body></html>'''
	
	print('Content-type: text/html\n\n')
	print(myhtml)
	return 0


def return_simple_error_page(e,tup):
	myhtml = f'''
<html><body style="bgcolor: black; color: lightred;">
	<h1><center>An Exception has been encountered.</center></h1>
	<h5><center>Please try again later</center></h5>
	<p>{e}</p>
	<p>{tup[0]}: {tup[1]}</p>
	<p>{tup[2]}</p>
	<hr />
</body><html>'''
	print('Content-type: text/html\n\n')
	print(myhtml)

def main():
	w(f'Starting main() in {prog}.\n')
	button = form.getvalue('submit')
	w(f'{button = }\n')
	
	fileid = parse_GET()
	w(f'{fileid = }\n')
	if fileid:
		thisfile = makeonefile(fileid)
		htmlpage(thisfile)
	else:
		return 99


if __name__ == '__main__':
	w('-' * 66)
	w('\n')
	w(f'Debugging {prog} on {today} at {now()}.\n\n')
	rv = main()
	sys.exit(rv)

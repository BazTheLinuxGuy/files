#!/usr/bin/python

import os
import sys
import sqlite3
import mycgi
from MyFile import *

form = mycgi.Form()

def fetch_records(page_number, records_per_page):
    w('\n...in fetch_records.\n')
    w(f'{page_number=}, {records_per_page=}\n')
    dt = thedate()
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    # Calculate the offset based on the page number and records per page
    offset = (page_number - 1) * records_per_page
    # Execute the query with LIMIT and OFFSET
    sql = f'SELECT * FROM newfiles ORDER BY fileid LIMIT {records_per_page} OFFSET {offset}'
    w(f'The sql statement in fetch_records is:\n{sql}\n')
    c = cur.execute(sql)
    # Fetch the results
    records = c.fetchall()
    w(f'..after fetchall there are {len(records)} records.\n')
    # Close the connection
    con.close()
    return records

def return_html(records: list, page: int):
    '''This function lays out the page generated when the user chooses "Report" '''
    w('\n\nin return_html, we are starting to construct an html page.\n')
    
    htmlpage='''\
    <html><head>
    <style>
    header {
       display: flex;
       background-color: #004066;
       color: #e1e1e1;
       font-size:10pt;
       font-family: Arial;
       align-items: left;
       padding: 0 20px;
    }
    body {
/*       display: flex; */
      background-color: lightblue;
      padding: 50px; 75px;
    }
    .main h1, .main h2, .main p, .main input { color: #004066: }
    .main table, .main th, .main td { border: 2px solid black; }
    .main thead { color: green; }
    .main th, .main td { padding: 0 15px; left-margin: 15 px; }
/*    .main table { width: 65%; } */
    .form1 { color: black; }
    .copy {
      position: absolute;
      justify-content: bottom;
      align-items: bottom;
      padding: 0px 20px;
    }
    .copy-text p {
      position: relative;
      font-size: 7pt;
      font-weight: bold;
      color: black;
      margin: 10px 0;
      bottom: auto;
    }
    </style></head><body>
    <title>Data Entered</title>
    <header>Report for dkfiles: files and descriptions.</header>
    <br /><hr />
    <div class="main" width="100%" style="width: 100%">
    <table class="main">'''
  
    w(f'we\'re crteating an html page, so far it\'s {len(htmlpage)} characters.\n')
    
    htmlpage += f'''
    <thead class="main"><tr class="main"><th class="main" colspan="2" style="text-align: left;">Page: {page}</th><th class="main" colspan="2" style="color:#004066;"></tr>
    <tr class="main"><th class="main">File id:</th><th class="main">Contents</th>
        <th class="main">Location</th><th class="main">Created</th></tr>
    <tr><th colspan="4" style="background-color: darkblue;"</th></tr>
    </thead>'''

    w('\nOK, going to enumerate the records now.\n')

    w('...is there a problem here?\n')
    
    for i,v in enumerate(records):
        w('...enumerating the records:\n')
        fid = v[0]
        w(f'...{fid=}\n')
        sd = v[1]
        w(f'...{sd=}\n')
        ld = v[2]
        w(f'...{ld=}\n')
        lo = v[3]
        w(f'...{lo=}\n')
        dt = v[4].strftime('%a, %b %d, %Y')
        w(f'...{dt=}\n')
        owner = v[5]
        w(f'...{owner=}\n')
        comments = v[6]
        w(f'...{comments=}\n')
        htmlpage += f'''
        <tr><td class="main"><td class="main"><b>{fid}</b></td><td>{sd}</td>
            <td class="main">{locations[lo]}</td><td class="main">{dt}</td></tr>
        <tr><td class="main" colspan="4">{ld}</td></tr>
<!--        <tr><td class="main">{owner}</td><td class="main" colspan="3">{comments}</td></tr> -->
        <tr><td style="background-color:darkblue;" colspan="4"</td></tr>'''
        w(f'Enumeration {i}: page has {len(htmlpage)} characters.\n')
        
    htmlpage += '''</table><hr /><br /><br />
    <div class="form1">
    <form class="form1" method="POST" action="/cgi-bin/report.py">
    <input type="submit" id="submit" name="submit" value="Next"><br />
    <input type="submit" id="submit" name="submit" value="Previous">
    <br />'''
    htmlpage += f'''\
    <input  class="form1" type="hidden" id="hidden" name="hidden" value="{page+1}" />
    <input  class="form1" type="hidden" id="hidden2" name="hidden2" value="{i+1}" />    
    </form></div>'''
    htmlpage += '''\
    <hr /><br />
    <button onclick='location.href="/menu.html";'>Menu</button>
    <br />
    <div class="copy" align="bottom" >
      <div class="copy-text">
        <p>&copy; 2024 Kevin Baumgarten, All rights reserved.</p>
      </div>
    </div></body></html>'''
    
    w('We finished creating the page and now we\'re displaying all\n')
    w(f'{len(htmlpage)} charaters of it.\n')
    myfile.close()
    print('Content-type: text/html\n\n')
    print(htmlpage)

def menu():
    print('Content-Type: text/html\n\n')
    print('''<html><head>
<meta http-equiv="refresh" content="0;url=/menu.html"></head>
<body>
    <p>Redirecting to menu.html...</p>
</body>
</html>''')

def quitnow2(myfile=None,button=None):
    w('quitnow() has been entered.\n')
    w(f'myfile is {myfile}, button is {button}\n')
    w('Closing now...\n')
    myfile.close()
    print('Content-type: text/html\n\n')
    print('<html><head>')
#    print('<script>function gotomenu() { location.href="http://10.0.0.151/menu.html; return false; " } function log(msg) { console.log(msg); }</script>')
    print('</head><body style="background-color: lightblue;">')
    print('<h2>End of report</h2>')
    print(f'<p><b>Button is {button}</b></p>\n')
    print('<hr />')
    print('<h4>You can leave this page or go to the menu</h4>')
    print('<p style="font-size: 12pt; margin-left: 20px; text-align: left;" />')
    print('<p> Click here:</p>')
    print('<br /><form method="post" action="/menu.html"><input type="submit" name="submit" value="Menu" /></form>')
    print('<input type="submit" name="submit" value="Menu">')
    print('</body></html>')
    
    
def main():
    w('\n')
    w('-' * 66)
    w('\n')
    w(f'Report debugging on {today} {now}\n')
    w('\n')
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    sql = 'SELECT COUNT(*) FROM newfiles'
    c = cur.execute(sql)
    numtuple = c.fetchone()
    totalrecs = int(numtuple[0])
    con.close()
    w(f'{totalrecs=}\n')
    records_per_page = 5
    submit = form.getvalue('submit')
    w(f'Submit value is {submit}\n')
    if submit == None:   # it is None when entering from the main menu
        w(f'Inside report "{submit=}"\n')
        page_number = 1
        result = fetch_records(page_number, records_per_page)
        if (len(result)):
            w(f'We got back from a trip to fetch_records, and got {len(result)} records back.\n')
            w('we\'re about to display the page...\n')
#            myfile.close()
            return_html(result, page_number)
    elif submit == 'Report':
        w(f'Inside report "{submit=}"\n')
        page_number = 1
        result = fetch_records(page_number, records_per_page)
        if (len(result)):
 #           myfile.close()
            return_html(result, page_number)
    elif submit == 'Next':
        h = form.getvalue("hidden")
        srecs = form.getvalue("hidden2")
        recs = int(srecs)
        w(f'Inside {submit}\n')
        page_number =  int(h)
        w(f'hidden value is {page_number}, recs is {recs}\n')
        rec_count = (page_number - 1) * records_per_page
        w(f'{recs=}, {rec_count=}\n') 
        if (rec_count) <= totalrecs:
            result = fetch_records(page_number, records_per_page)
            if len(result):
#                myfile.close()
                return_html(result, page_number)
            else:
                page_number -= 1
                result = fetch_records(page_number, records_per_page)
                if len(result):
                    myfile.close()
                    return_html(result, page_number)
        else:
            page_number -= 1
            result = fetch_records(page_number, records_per_page)
            if len(result):
#                myfile.close()
                return_html(result, page_number)

    elif submit == 'Previous':
        w(f'Inside {submit}.\n')            
        h = form.getvalue('hidden')
        page_number = int(h)
        w(f'page number is {page_number}\n')
        if (page_number >= 3):
            page_number -= 2
        else:
            page_number = 1
        w(f'now, page number goes back to {page_number}\n')
        rec_count = (page_number - 1) * records_per_page
        w(f'{rec_count=}, {totalrecs=}, {page_number=}\n')
        if rec_count <= totalrecs:
            w(f'Calling fetch_records from {submit}\n')
            w(f'..as fetch_records({page_number}, {records_per_page}\n')
            result = fetch_records(page_number, records_per_page)
            w(f'After fetch records, len(result) = {len(result)}\n')
            if len(result) > 0:
                w(f'Calling return_html from {submit}...\n')
#                myfile.close()
                return_html(result, page_number)
            else:
                result = fetch_records(1, records_per_page)
#                myfile.close()
                return_html(result, page_number)
    elif submit == 'Menu':
        w(f'Inside {submit}\n')
        w ('About to enter menu()\n')
        myfile.close()
        menu()
    else:
        w(f'Oddly, the submit button was {submit}\n.')
        myfile.close()
        menu()
    return 0
          
if __name__ == '__main__':

# ALL THIS IS FLUFF! BUT THE SYSTEM WON'T BEHAVE AS TOLD!
    
    do = '/var/www/cgi-bin/report_debug.txt';
    myfile = open(do,'a')
    w = myfile.write
    w('We got as far as __name__ == \'__main__\':\n')
    myfile.close()
    print('Content-type: text/html\n\n')
    print('<html><body><h1>This is report.py</h1>')
    print('</body></html>

    
#    input('[Enter] continues, [Ctrl-c] breaks: ')
#    rv = main()
    

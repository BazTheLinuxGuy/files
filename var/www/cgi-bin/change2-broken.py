 #!/usr/bin/env python
''' This cgi program will change or delete a file record in the database'''

# Updated: Friday, June 28, 2024 5:00 AM   .



mynotes = r'''
1. Need to refactor return_html() so that parts of it can be used
   for the returned search list and not just the sequential "All"
   configuration. The foundit() routine, borrowed from lookup.py,
   just isn't appropriate enough.
'''


import os
import sys
import sqlite3
import mycgi

from MyFile import *

DEBUG = 0

global form
form = mycgi.Form()

def database_transaction(sql: str) -> list:
    '''This routine does a "SELECT" type sql transaction
       and returns the result as a list of tuples.
       A tuple represents a row of a table.'''
    
    
    w('...entered database_transaction\n')
    w(f'sql is {sql}\ndbname={db}\n')
    lst = []
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute(sql)
        lst = cur.fetchall()
        if DEBUG:
            if len(lst):
                for i,item in enumerate(lst):
                    w(f'{i}: {item}\n')
                    w('\n')
                else:
                    w('Empty')
        con.close()
    except sqlite3.Error as er:
        rv = sqlite3_error(er)
        sys.exit(rv)
    except Exception as e:
        tup = sys.exc_info()
        w(f'...caught exception \'{e}\'\n')
        w(f'{tup[0]}: {tup[1]}')
        rv = error_page(e)
        sys.exit(rv)
        
#    w(f'leaving dbt() with lst {lst}\n')
    w(f'leaving dbt() with a lst: {lst[0][0]}\n')
    return lst

dbt = database_transaction

def fetch_records(page_number: int, records_per_page: int) -> list:
    w(f'{page_number = }, {records_per_page = }\n')

    # Calculate the offset based on the page number and records per page
    offset = (page_number - 1) * records_per_page

    # Execute the query with LIMIT and OFFSET
    sql = f'SELECT * FROM newfiles ORDER BY fileid LIMIT {records_per_page} OFFSET {offset}'
    records = dbt(sql)
    return records


def sqlite3_error():
    myhtml = '''
    <html><head><meta charset="utf-8"><title>Sqlite3 Error</title>
    <link rel="stylesheet" href="/css/entry.html" />
    <style>
      body {
        text-align: left; 
        background-color: lightblue;
        padding-left:100px;
        color: #004066;
      }
      header {
         background-color: #004066; color: #e1e1e1; padding 0;
      }
      img { padding: 10px 10px; }
      button { left-margin: 100px; }
      table, th, td { border: 2px solid black; }
    </style></head>
    <body>
    <header>Details of the sqlite3 error that we have just encountered</header>
    <nav>
      <a href="/menu.html">Home (Menu)</a>
      <a href="/lookup.html">Lookup</a>
      <a href="/thankyou.html>Quit entirely</a>
      <a href="/change.html">Edit or Delete</a>
    <nav>
    <h2>You have encountered an error</h2><hr />'''

    htmlstr += f'''
    <table>
    <tr><th colspan="2">Details:</th></tr>
    <tr><td>Error code:</td><td>{er.sqlite_errorcode}</td></tr>
    <tr><td>Error name:</td><td>{er.sqlite_errorname}</td></tr>
    </table>
    <p>Please contact the programmer about this issue</p>
    <hr />
    <button name="back" onclick="history.back()">Go Back</button>&nbsp;
    <button onclick="location.href='/menu.html';">Home (Menu)</button><br />
    </body></html>'''
    
    print('Content-type: text/html\n\n')
    print(myhtml)
    return 1
    



def error_page(e):
    e_info: dict = { 
        'type': type(e),    # the exception type
        'args': e.args,     # arguments stored in .args
        'estr': str(e),     # __str__ allows args to be printed directly
    }
    if not e_info['args']:
        e_info['args'] = ''
        tea = None
    else:
        tea = type(e_info['args'])

    htmlstr ='''\
    <DOCTYPE !html>
    <html><head>
    <meta charset="utf-8" />
    <title>General Error</title>
    <link rel="stylesheet" href="/css/entry.html" />
    <style>
      body {
        text-align: left; left-margin: 100px;
        background-color: lightblue; padding: 20px 100px;
      }
      header {
         background-color: darkgreen; color: #e1e1e1; padding 0 100px;
      }
      h1 { color: darkgreen; text-align: left; }
      h2 { color: black; text-align: left; left-margin: 100px; }
      p {
          color: black; text-align:left;
          font-size: 16pt; left-margin: 100px; 
        }
      img { padding: 10px 10px; }
      button { left-margin: 100px; }
      table, th, td { border: 2px solid black; }
      table { width: 50%; }
      th { width: 30%; text-align: center; }
      td { width: 30%; text-align: left; }
    </style></head><body>
    <header>Error information</header>
    <h2>You have encountered an error</h2><hr />'''

    htmlstr += f'''
    <table><thead>
    <tr><th>Details:</th><th /></tr></thead>
    <tr><td>The error:</td><td>{e}</td></tr>    
    <tr><td>Error type:</td><td>{type(e)}</td></tr>
    <tr><td>Error args:</td><td>{e.args}</td></tr>
    <tr><td colspan=2></td><tr>
    </table>
    <p>Please contact the programmer about this issue</p>
    <hr />
    <button onclick="history.back()">Go Back</button>&nbsp;
    <button onclick="location.href='/menu.html';">Menu</button><br />
    </body></html>'''
    
    print('Content-type: text/html\n\n')
    print(htmlstr)
    return 1

def sorry(searchterm):
    myhtml = '''<html><head><meta charset="utf-8"><title>Sorry</title>
<link rel="stylesheet" href="/css/change.css" />
<style>
body { background-color: #e1e1e1; text-align: left; }
h1 { color: darkgreen; }
h4,p { color:black; }
</style></head>'''
    
    myhtml += f'''
<body><h1>Sorry!</h1>
<br /><br /><h4>We couldn't find the search term '{searchterm}'</h4><br />
<p>Please try again</p>
<button id="change" name="change" onclick="location.href='/change.html';">
Edit or Delete</button>
<hr /><br />
<button name="back" onclick="history.back()">Go Back</button>&nbsp;
<button name="menu" onclick="location.href='/menu.html';">Home (Menu)</button><br /></body></html>'''

    print('Content-type: text/html\n\n')
    print(myhtml)


def foundit(term: str, lst: list):
    w('Entered foundit()\n')
    lenlst = len(lst)
    w(f'{lenlst = }\n')

    myhtml = '''
<!DOCTYPE html><html><head lang="en"><meta charset="utf-8"><title>Search Results</title>
<link rel="stylesheet" href="/css/change.css" /></head>'''
    
    w('We have now written the <head> section of the page to be returned.\n')

    myhtml += f'''
<body>
<header>Lookup results for '{term}'. &quotMore Details&quot; will allow you to change or delete file records</header>
<nav class="nav">
  <a class="nav" style="padding-right: 25px;" href="/menu.html">Home (Menu)</a>
  <a class="nav" style="padding-right: 25px;" href="/lookup.html">Lookup</a>
  <a class="nav" style="padding-right: 25px;" href="/thankyou.html">Quit Entirely</a>
</nav>'''
    
    w(f'list length: {lenlst}, list: {lst}\n')
    if lenlst == 1:
        myhtml += f'<p>We found one match</p>'
        w('Found a match.\n')
    else:
        myhtml += f'<p>We found {lenlst} matches</p>'
        myfile.write(f'Found {lenlst} matches.\n')

    myhtml += '''
<p style="margin-left: 50px; margin-right: 50px;">The &quot;More Details&quot; GO button will show you<br />
the entire record, from which you can change or delete it.</p>
<hr />'''

    
    myhtml += '''<table>
 <tr>
    <th>File ID</th><th>Contents</th><th>Location</th><th>More Details?</th>
 </tr>'''
    
    w('We are now going to enumerate the record from the database.\n')

    for i, v in enumerate(lst):
        e = eachfile = onefile._make(v)
        location = locations[e.lo]
        myhtml += f'''
<tr><td><b>{e.fileid}</b></td><td>{e.sd}</td><td>{location}</td>
  <td><center><button onclick="location.href='/cgi-bin/onerec.py?fileid={e.fileid}';">GO</center></button></td></tr>'''
        
    myhtml += '''
<!-- <tr><td colspan="4">
  <img src="/hanging-office-file-folders.png" alt="Hanging File Folders" /></td></tr> -->
<tr><td class="navbuttons"><center><button id="prev" name="prev" onclick="location.href='/cgi-bin/onerec.py?fileid={previd}';">&lArr;Previous</button></center></td>
<td class="navbuttons"><center><button id="next" name="next" onclick="location.href='/cgi-bin/onerec.py?fileid={nextid}';">Next&rArr;</button></center></td></tr>
<tr><td class="navbuttons" colspan="2"></td></tr>
<tr><td class="navbuttons"><center><button name="menu" id="menu" onclick="location.href='/menu.html';">Home</button></center></td><td class="navbuttons"><center><button id="print" name="print" onclick="location.href='/cgi-bin/temppage.py';">Print</button></center></td></tr>
</table>
<hr /><br /><br />
<button name="back" onclick="history.back();">Back</button>&nbsp;
<button name="menu" onclick="location.href='/menu.html';">Home (Menu)</button><br />
<br /><br /><br />
<div class="copy">
  <div class="copy-text">
    <p>&copy; 2024 Kevin Baumgarten, All rights reserved.</p>
  </div>
</div>
</body></html>'''
    
    w(f'\nClosing {df} (this file).\n')
    w('-' * 66)
    w('\n\n')
    myfile.close()
   
    print('Content-type: text/html\n\n')
    print(myhtml)
    
    return 0 # We don't ever get here, do we? so why not?


def html_head() -> str:
    return '''<!DOCTYPE html><html><head><meta charset="utf-8" /><title>Make changes</title><link rel="stylesheet" href="/css/change.css"/></head>'''

def body_and_table_header(page: int) -> str:
    return f'''<body>
<header>Choose a record. &quotMore Details&quot; will allow you to change or delete file records</header>
<nav class="nav">
  <a class="nav" href="/menu.html">Home (Menu)</a>
  <a class="nav" href="/lookup.html">Lookup</a>
  <a class="nav" href="/thankyou.html">Quit Entirely</a>
</nav>
<p>&quot;More Details&quot; will show you the entire record<br />
from which you can change or delete the record.</p>
<hr />
<p>Page: {page}</p>
<table><tr><th>File ID</th><th>Contents</th><th>Location</th><th>More Details?</th></tr>'''

def eachrow(t) -> str:   # 't' is a named tuple, for each row
    '''Returns an html table row that has our required 4 fields
       from the named tuple passed as the argument.'''
    
    s = f'''<tr><td style="padding: 0 15px 0 15px;"><b>{t.fileid}</b></td><td style="padding: 0 15px 0 15px;">{t.sd}</td><td style="padding: 0 15px 0 15px;">{locations[t.lo]}</td><td><center><button onclick="location.href='/cgi-bin/onerec.py?fileid={t.fileid}';">GO</button></center></td></tr>'''
    return s


def html_image() -> str:
    '''Returns the image to display at the bottom of our table.'''
    return f'''<tr><td colspan="4"><img src="/hanging-office-file-folders.png" alt="Hanging File Folders" /></td></tr>'''


def finish_table() -> str:
    return '</table><hr /><br /><br />'

def formdiv(pagenum: int) -> str:
    return f'''
<div class="form1">
<button style="color:navy;padding: 0;justify: center; padding: 0;" name="back" onclick="history.back()">&lt;Back</button><br />
<form method="post" action="/cgi-bin/change.py">
  <input type="submit" id="submit" name="submit" value="Previous">&nbsp;
  <input type="submit" id="submit" name="submit" value="Next"><br />
  <hr />
  <input type="submit" id="submit" name="submit" value="Home" /><br />
  <input type="hidden" id="pagenum" name="pagenum" value="{pagenum+1}"/>
</form></div>'''


def copyrite() -> str:
    return '''<br /><br /><br /><div class="copy"><div class="copy-text"><p>&copy; 2024 Kevin Baumgarten, All rights reserved.</p></div></div>'''


def endhtml() -> str:
    return '''</body></html>'''


def return_html(pagenum: int, records: list) -> int:
    w(f'** Starting return_html in {prog} **\n')
    
    myhtml = html_head()
    w('We have now written the <head> section of the page to be returned.\n')

    myhtml += body_and_table_header(pagenum)

    w('We are now going to enumerate the records from the database.\n')
    for i,tup in enumerate(records):
        t = thisrec = onefile._make(tup)
        location = locations[t.lo]
        w(f'{t = }\n')
        myhtml += eachrow(t)
        
    myhtml += html_image()
    myhtml += finish_table()
    myhtml += formdiv(pagenum)
    myhtml += copyrite()
    myhtml += endhtml()

    w(f'\nClosing {df} (this file).\n')
    w('-' * 66)
    w('\n\n')
    myfile.close()
    
    print('Content-type: text/html\n\n')
    print(myhtml)
    return 0


# Branching back to main menu:

# first method, from microsoft copilot
def main_menu1():
    print("Content-Type: text/html\n")
    print("Location: /menu.html\n\n")  # Redirect to menu.html
    print()  # Empty line to indicate end of headers

# second method, also from copilot
def main_menu():

    w('OK, got a button press for main menu!\n')
    myfile.close()

    redirect='<html><head><meta http-equiv="refresh" content="0;url=/menu.html"></head><body><p>Redirecting to menu.html...</p></body></html>'
    
    print('Content-Type: text/html\n\n')
    print(redirect)
    return 0
    
    
def nrecs() -> int:
    '''Reports how many rows are in the SQL table "newfiles" in "files.db"'''
    
    w('\nin nrecs()...\n')
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        sql = 'SELECT COUNT(*) FROM newfiles'
        w(f'about to try to cur.execute "{sql}"\n')
        cur.execute(sql)
        tup = cur.fetchone()
        con.close()
        nrecs = int(tup[0])
        w(f'nrecs = {nrecs}\n')        
    except sqlite3.Error as er:
        w(f'received sqlite error:\n')
        w(f'code: {er.sqlite_errorcode}: {er.sqlite_errorname}.\n')
        sqlite3_error(er)
        sys.exit(er.sqlite_errorcode)
    except Exception as e:
        w(f'received an Exception: \'{e}\'\n\n')
        tup = sys.exc_info()
        w(f'{tup[0]}: {tup[1]}\n')
        rv = error_page(e)
        sys.exit(rv)
        
    return nrecs # number of records in the SQL newfiles table.


def look_for_searchterm(term: str) -> list:
    
    w(f'...entered look_for_searchterm({term})\n')
    # term = term.strip().lower() already done.
    # fields to search: fileid, sd, ld, locations[lo],  owner, comments, cr, dt
    simple_fields = ('fileid', 'sd', 'ld', 'owner', 'comments')
    complicated_fields = ('lo','cr','dt')
    
    con = sqlite3.connect(db)
    cur = con.cursor()
    lst = []
    fileids = set()
    w(f'\n\nDoing a search on {term}\n\n')

    for field in simple_fields:
        
        w(f'{field = }\n')
        sql = f'SELECT * FROM newfiles WHERE {field} LIKE "%{term}"'
        cur.execute(sql)
        l = cur.fetchall()
        
        for tup in l:
            fileid = tup[0]
            if fileid not in fileids:
                lst.append(tup)
                fileids |= { fileid }
                
    w('\n>>> After "simple" fields:\n{lst = }\n')
    
    # Now, the rest of the fields:

    # Location:   
    for k,v in locations.items():
        if term in v.lower():
            sql = f'SELECT * FROM newfiles WHERE lo = "{k}"'
            cur.execute(sql)
            l = cur.fetchall()
            for tup in l:
                fileid = tup[0]
                if fileid not in fileids:
                    fileids |= { fileid }         
                    lst.append(tup)


    # Creation date
    sql = 'SELECT fileid, cr FROM newfiles'
    cur.execute(sql)
    l = cur.fetchall()
    for tup in l:
        # we're retrieving two fields, the second one is "cr" (creation date)
        someday = ymd2dt(tup[1])
        if term in someday:
            sql = f'SELECT * FROM newfiles WHERE fileid LIKE "%{tup[0]}%"'
            cur.execute(sql)
            t = cur.fetchone()
            if t:
                lst.append(t)

    # Modification date:
    
    sql = 'SELECT fileid, dt FROM newfiles WHERE dt IS NOT NULL'
    cur.execute(sql)
    l = cur.fetchall()
    for tup in l:
        # we're retrieving two fields,
        # the second one is "dt" (modification date)
        someday = ymd2dt(tup[1])
        if term in someday:
            sql = f'SELECT * FROM newfiles WHERE fileid = {tup[0]}'
            cur.execute(sql)
            t = cur.fetchone()
            if t:
                lst.append(t)
    con.close()
    if len(lst):
        # w(f'lst is {lst}\n')
        lst.sort()
        return lst
    else:
        w('\nNo items in list...calling sorry()..\n\n')
        sorry(term) # calls sys.exit()


def handle_searchterm(term: str) -> int:
    w('\n...inside handle_searchterm.\n')
    lst = []
    if term:
        w(f'we\'re going to look_for_searchterm({term})\n')
        lst = look_for_searchterm(term)
        rv = foundit(term, lst)
    else:
        rv = handle_the_all_button()
    return rv

def handle_the_all_button() -> int:
    w('...in handle_the_all_button\n')
    page_number = 1
    records_per_page = 5
    result = fetch_records(page_number, records_per_page)
    if (len(result)):
        w(f'>>> Calling return_html() from All.<<<\n')
        w(f'...with a result of {len(result)} rows,\n{page_number = }.\n')
        rv = return_html(page_number, result)
        return rv
    else:
        try:
            raise ValueError('The list we need is empty!')
        except ValueError as ve:
            error_page(ve)
            return 1
    return 99 # "Programmer Error"


def handle_next(nrecs: int):
    w('...in handle_next()\n')
    w(f'going to get the hidden value\n')
    records_per_page = 5
    p = form.getvalue('pagenum')
    w(f'\n{p = }\n')
    x = type(p)
    w(f'p is type {x}\n')
    page_number =  int(p)
    
    w(f'hidden value is {page_number}\n')
    
    rec_count = (page_number - 1) * records_per_page
 
    w(f'{rec_count = }\n')

    if rec_count <= nrecs:
        
        w(f'About to call fetch records from Next\n')
        result = fetch_records(page_number, records_per_page)
        w('...back from from fetch_records:\n')
        w(f'len(result) is {len(result)}\n')
        
        if (len(result)):
            w(f'Calling return_html from Next.\n')
            rv = return_html(page_number,result)
        else:
            page_number -= 1
            result = fetch_records(page_number, records_per_page)
            if len(result):
                rv = return_html(page_number,result)
            else:
                page_number = 1
                result = fetch_records(page_number, records_per_page)
                if len(result):
                    rv = return_html(page_number,result)

    else:
        rv = 99 # "Programmer Error"
    return rv

def handle_previous(totalrecs: int):
    w(f'Inside handle_previous()\n')
    
    records_per_page = 5
    pagenum = form.getvalue('pagenum')
    page_number = int(pagenum)
    w(f'page number is {page_number}\n')
    
    if (page_number >= 3):
        page_number -= 2
    else:
        page_number = 1
        
    rec_count = (page_number - 1) * records_per_page
        
    if rec_count <= totalrecs:
        result = fetch_records(page_number, records_per_page)
        if (len(result)):
            w(f'Calling return_html from Previous...\n')
            rv = return_html(page_number,result)
            return rv
        else:
            if page_number > 1:
                page_number -= 1
                result = fetch_records(page_number, records_per_page)
                if (len(result)):
                    w(f'Calling return_html from Previous again...\n')
                    rv = return_html(page_number,result)
                    return rv
                else:
                    page_number = 1
                    result = fetch_records(page_number, records_per_page)
                    if (len(result)):
                        w(f'Calling return_html from Previous again again...\n')
                        rv = return_html(page_number,result)

        
def main():
    page_number: int = 1
    records_per_page: int = 5

    w(f'\nin in main() of {prog}.\n')
    
    totalrecs = nrecs()

    button = form.getvalue('submit')
    
# Possible button presses for "submit":
# This could come from change.html
# or from this program calling itself.
#   1. Search   (from change.html)
#   2. All      (from change.html)
#   3. Next     (from change.py, which writes a page with a form, with 'action="change.py"')
#   4. Previous (from change.py)
#   5. Menu     (from change.py)

    w(f'Inside {button}\n')    

# 1) SEARCH
    if button == 'Search':
        term = form.getvalue('term')
        term = term.strip().lower()
        w(f'Got the value of term from caller: {term = }.\n')
        rv = handle_searchterm(term)
        return 0
    
# 2) ALL        
    elif button == 'All':
        handle_the_all_button()
        return 0
    
# 3) NEXT    
    elif button == 'Next':
        handle_next(totalrecs)
        return 0
        
# 4) PREVIOUS
    elif button == 'Previous':
        handle_previous(totalrecs)
        return 0
        
# 5) MENU
    elif button == 'Home':
        w('\nbranching back to main menu from a "Menu" button...\n\n.')
        w('*' * 66)
        w('\n\n')
        main_menu()
        
# 6) COSMIC RAY        
    else:
        w('\nbranching back to main menu from an unknown button press...\n\n.')
        w('*' * 66)
        w('\n\n')
        main_menu()

if __name__ == '__main__':
    w('-' * 66)
    w(f'\nDebugging {prog} on {today} at {now()}.\n')
    w('...about to call main...\n\n')
    rv = main()

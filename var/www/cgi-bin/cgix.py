#!/usr/bin/python

import mycgi 
import sqlite3
import sys
import MyFile
import time

DEBUG = 1

debug_filename = 'cgix_debug.txt'
df = open(debug_filename,'a')

today = MyFile.thedate()
now = time.strftime('%H:%M',time.localtime(time.time()))
df.write('-' * 66)
df.write('\n')
df.write(f'Debug output for: {today} {now}\n')


# Create instance of FieldStorage
form = mycgi.Form()
# Get data from fields 
page = form.getvalue('page')
df.write(f'{page=}\n')
pg = int(page)
records_per_page = 10
# Connect to your SQLite database 
conn = sqlite3.connect('/var/data/files.db')
cursor = conn.cursor() 
# Calculate offset 
offset = (pg - 1) * records_per_page
# Retrieve the specific page of records 
# cursor.execute("SELECT * FROM dkfiles WHERE location LIKE %rf% LIMIT ? OFFSET ?", (records_per_page, offset)) 
# cursor.execute('SELECT * FROM dkfiles WHERE location LIKE "%r" LIMIT 10')
cursor.execute('SELECT * FROM dkfiles ORDER BY id')
rec = cursor.fetchall()
lenrec = len(rec)
df.write(f'{lenrec} records retrieved from dkfiles:\n')
df.write(f'{rec=}\n')
sp = sys.path
df.write('sys.path in the cgi environment:\n')

for p in sp:
    df.write(f'{p=}\n')
    

for r in rec:
    df.write(f'{r[0]=} {r[1]=} {r[3]=} {r[4]=}\n')
    
df.close()
# Generate HTML output 
print('Content-type:text/html\n\n') 
print('<html>') 
print('<head>') 
print('<title>Pagination Example</title>') 
print('</head>') 
print('<body>')
print(f'<h2>Here is sys.path in the cgi environment.')
print('<p>')
for p in sp:
    print(f'{p}&nbsp;&nbsp;')
print('</p>')
print(f'<h2>Records Page: {page}</h2>') 
for r in rec: 
    print(f'<p>{r[0]}, {r[1]}, {r[3]}, {r[4]}</p>')
print('</body></html>')

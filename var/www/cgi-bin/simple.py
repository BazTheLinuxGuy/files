#!/usr/bin/env python
def return_html():
    myhtml = '''
<!DOCTYPE html>
<html lang="en">
  <head>
	<meta charset="utf-8" />
	<title>learning javascript</title>
	<link rel="stylesheet" href="file:///var/www/html/css/lookup.css" />
	
	<script>
	  function getDate() {
		  now = new Date();
		  document.getElementById("demo").innerHTML = now;
		  return now;
	  }
	  
	  function hello() {
		  alert('Hello, world!')
          }
    
	  function rusure(v,w,x,y,z) {
          alert("We got to rusure...");
		  
		  document.getElementById("question").innerHTML =
			  "Make changes to or delete records";
          document.getElementById("fileid").innerHTML =
			  "My file id is  ";
          document.getElementById("a1").innerHTML = v;
          document.getElementById("sd").innerHTML = "My content is ";
          document.getElementById("a2").innerHTML = w;
          document.getElementById("ld").innerHTML =
			  "More details are: " + x + ".";
		  document.getElementById("lo").innerHTML =
			  "My location code is: " + y + ".";
		  document.getElementById("dt").innerHTML =
			  "I was created on: " + z + ".";
		  
	      item1 = 'location.href = "/cgi-bin/delrec.py?fileid="' + v + ";";
          document.getElementById("yes").innerHTML = "<button onclick='${item1}'>Yes</button>";
		  
		  item2 = 'location.href = "/cgi-bin/editrec.py?fileid="' + v + ";";
          document.getElementById("cxl").innerHTML = "<button onclick='${item2}'>&quot;editrec.py&quot;</button>"
		  

	      return true;
	  }
	  
	  </script>
  </head>
  <body>
	<p>This is not an authentic address</p>
	<p id="demo">This should change considerably</p>
	<button onclick="hello();"> Go ahead</button>
	<button onclick="hello();">Hello?</button>
	<button onclick="getDate();">Date-Time</button>
	<button onclick="rusure();">rusure?</button>
	<hr />
	<header>Make changes or delete a record altogether</header>
<h2>This page will lead you to editor delete a record.</h2>
<hr />
<p id="testing"></p>
<table>
<tr><td id="question" colspan="2"></td></tr>
<tr><td id="fileid"></td><td id="a1"></td></tr>
<tr><td id="sd"></td><td id="a2"></td></tr></table>
<p id="ld"></p>
<p id="lo"></p> 
<p id="dt"></p>
<p id="yes"></p>
<p id="cxl"></p>

<footer>&copy; 2024, Kevin Baumgarten. All rights reserved.</footer>
</body></html>'''

    print('Content-type: text/html\n\n')
    print(myhtml)

if __name__ == '__main__':
    return_html()

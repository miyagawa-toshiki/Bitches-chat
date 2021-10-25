#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import cgi
import cgitb
import cgi
import pandas as pd
import json
import re
from janome.tokenizer import Tokenizer
import os
import psycopg2
import datetime
cgitb.enable()
form = cgi.FieldStorage()
text = form.getvalue('content')
#DB接続
con = psycopg2.connect("{secret}")

print('Content-type: text/html')
print('')
print('<html>')
print('<head>')
print('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')
print('<meta name="viewport" content="width=device-width, initial-scale=1">')  
print('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">')  
print('<title>愚痴チャット</title>')  
print('<style>')
print('body {padding-top: 80px;')    
print('padding-bottom:40px;}')     
print('ul.list {')     
print('list-style-type: none;')          
print('padding:40px 120px;')          
print('}')
print('</style>')  
print('</head>')
print('<body>')
print('<body>')
print('<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">')
print('<div class="container-fluid">')      
print('<a class="navbar-brand" href="https://muds.gdl.jp/~s1922033/myapp/cgi-bin/index.py">愚痴まとめ</a>')          
print('<div class="collapse navbar-collapse d-flex justify-content-end">')          
print('<ul class="navbar-nav"> ') 
print('<li class="nav-item active">')              
print('<a class="nav-link " href="https://muds.gdl.jp/~s1922033/myapp/cgi-bin/index.py">入力ページへ</a>')                  
print('</li>')              
print('</ul>')            
print('</div>')            
print('</div>')      
print('</nav>')
print('')
print('<div class="text-center">')
print('<h5 class="text-center">愚痴書き込み</h5>')  
print('<p>')  
print('<h3 class="text-center">ランキング一覧</h3>')
print('</p>')  
print('</div>')

import cgi
import pandas as pd
import json
import re
from janome.tokenizer import Tokenizer
import os
import psycopg2
import datetime
#cgitb.enable()

form = cgi.FieldStorage()
text = form.getvalue('content')
point = ''
#DB接続
con = psycopg2.connect("host=localhost dbname=s1922033 user=s1922033 password=R1wguNbI")

cur = con.cursor()

# ここから処理の内容を書く。


cur.execute('SELECT * FROM sentence ORDER BY score desc LIMIT 5;')
ranking = 1
print("<ul class='list'>")
for row in cur:
    print("<div class='alert alert-primary' role='alert'> %s位</br> %s</br> Score : %s</br> %s</div>"% (ranking,row[0],row[1],row[2]))
    ranking += 1
print("</ul>")
cur.close()

# 実際の表示
#print(html % (lst_str))

print("</body></html>")

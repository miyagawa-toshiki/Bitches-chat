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
con = psycopg2.connect("{secret}")

print('Content-type: text/html')
print()
print('<html>')
print('<head>')
print('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')
print('<meta name="viewport" content="width=device-width, initial-scale=1">')
print('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">')
print('<title>愚痴チャット</title>')
print('<style>')
print('body {padding-top: 80px;')
print('padding-bottom:40px;}')
print()
print('ul.list {')
print('list-style-type: none;')
print('padding:40px 120px;')
print('}')
print('</style>')
print('</head>')
print('<body>')
print('<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">')
print('<div class="container-fluid">')
print('<a class="navbar-brand" href="https://muds.gdl.jp/~s1922033/myapp/cgi-bin/index.py">愚痴まとめ</a>')
print('<div class="collapse navbar-collapse d-flex justify-content-end">')          
print('<ul class="navbar-nav">') 
print('<li class="nav-item active">')     
print('<a class="nav-link " href="http://muds.gdl.jp/~s1922033/myapp/cgi-bin/ranking.py">ランキングへ</a>') 
print('</li>')
print('</ul>')
print('</div> ') 
print('</div>')
print('</nav>')
print('')
print('')
print('<h1 class="text-center h_p">愚痴りたい内容を入力してください</h1>')

text = form.getvalue('content')
word = form.getvalue('search')
point = ''
#DB接続
cur = con.cursor()

print('<div class="text-center">')
print('<form action="index.py" method="POST">')
print('<input type="text" name="content" />')
print('<button type="submit">送信</button>')
print('</form>')
print('<p>')
print('{}</br>'.format(text))

# ここから処理の内容を書く。

"書き込む処理"
if 'content' in form:
  re_and = re.compile(' &[ !]')
  PATH = '/home/s1922033/public_html/myapp/pn.csv.m3.120408.trim'
  with open(PATH) as fd:
      word_dict_noun = {}
      for line in fd:
          word, polarity, word_type = line.split('\t')
          if polarity == 'e':
              continue
          #word = neologdn.normalize(word)
          word_dict_noun.update({word: polarity})


#text = '囚人耳の調子最悪'
  t = Tokenizer()
  tokens = t.tokenize(text)
  docs = []
  for token in tokens:
      if token.part_of_speech.split(',')[0] in ['名詞']:
          docs.append(token.surface)

  point=0
  for word in docs:
      if word in word_dict_noun:
        negaposi = word_dict_noun[word]
        if negaposi == 'n':
            point += 1
        elif negaposi == 'p':
            point -= 1
        else:
            point += 0

 #現在時刻取得
  dt = datetime.datetime.now()
  Year = dt.year
  Month = dt.month
  Day = dt.day
  Hour = dt.hour
  Minute = dt.minute
  second = dt.second

  new_dt = "{}/{}/{} {}:{}".format(Year,Month,Day,Hour,Minute,second)

  cur.execute("INSERT INTO sentence (nline, score , date) VALUES (%s, %s ,%s)", (text,point,new_dt))
  con.commit()
  
print('<font size="7" color="red">{}点です</font>'.format(point))
print('</p>') 
print('</div>')
print('<div class="text-center">')
print('<p>')
print('<h3>検索フォーム</h3>')  
print('<form action="index.py" method="GET">') 
print('<input type="text" name="search" />')
print('<button type="sumbit">送信</button>') 
print('</div>')
#検索の場合
if "search" in form:
  print("<ul class='list'>")
  print('{}'.format(word))
  cur.execute("SELECT * FROM sentence WHERE nline LIKE '%{}%' ORDER BY date desc".format(word))
  for row in cur:
      #lst_str += "<div class='alert alert-primary' role='alert'>%s</br> Score : %s</br> %s</div>" % (row[0],row[1],row[2])
      print("<div class='alert alert-primary' role='alert'>%s</br> Score : %s</br> %s</div>" % (row[0],row[1],row[2]))
  #lst_str += "</ul>"
print("</ul>")


cur.execute('SELECT * FROM sentence ORDER BY date desc')
print("<ul class='list' >")
for row in cur:
    #lst_str += "<div class='alert alert-primary' role='alert'>%s</br> Score : %s</br> %s</div>"% (row[0],row[1],row[2])
    print("<div class='alert alert-primary' role='alert'>%s</br> Score : %s</br> %s</div>"% (row[0],row[1],row[2]))
#lst_str += "</ul>"
print("</ul>")
cur.close()


# 実際の表示
#print(html.format(text,point,lst_str))
print("</body></html>")

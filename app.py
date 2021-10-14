from flask import Flask, request, send_file
from checker import Checker, get_api
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variable from .env

app = Flask(
  __name__, 
  static_folder='.',
  root_path='/home/runner'
  )


@app.route('/')
def root():
  return "App made by Rodrigo E. Principe (fitoprincipe82@gmail.com)"


@app.route('/error')
def error():
  return "An error occurred, sorry =)"


@app.route('/error2')
def error2():
  error = request.args.get('error')
  return "Ocurrió el siguiente error \n\n {}".format(error)


@app.route('/check')
def check():
  coords = request.args.get('coords')
  level = request.args.get('level')
  ingee = request.args.get('ingee')
  start = request.args.get('start')
  end = request.args.get('end')
  
  user = os.environ['HUB_USER']
  password = os.environ['HUB_PASS']
  api = get_api(user, password)
  
  ch = Checker(coords, start, end, level, ingee, api)

  html = ch.create_html()

  return html

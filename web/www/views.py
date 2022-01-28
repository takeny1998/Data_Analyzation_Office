from flask import Blueprint, jsonify, render_template, request
from database.db_handler import DBHandler
import datetime as dt
import json

views = Blueprint("views", __name__)

@views.route('/')
def index():
     return render_template('index.html')


@views.route('/get_crawling_data', methods=['POST'])
def get_crawling_data():
     db_handler = DBHandler()
     now = dt.datetime.now()
     times = int(now.hour / 3)

     data = request.get_json()
     today = data['date']
     type = data['type']

     crawling_data = db_handler.get_crawling_data(today, times, type)
     db_handler.close()
     return json.dumps(crawling_data)


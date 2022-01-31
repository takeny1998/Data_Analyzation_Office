from flask import Blueprint, jsonify, render_template, request
from database.db_handler import DBHandler
import datetime as dt
import json

views = Blueprint("views", __name__)

@views.route('/')
def index():
     return render_template('index.html')

@views.route('/get_started')
def get_started():
     return render_template('get_started.html')


@views.route('/get_crawling_data', methods=['POST'])
def get_crawling_data():
     data = request.get_json()
     selected_day = data['date']
     type = data['type']

     db_handler = DBHandler()
     now = dt.datetime.now()
     today = now.strftime('%Y-%m-%d')

     if today == selected_day:
          times = int(now.hour / 3)
     else:
          times = 7

     while True:
          try:
               crawling_data = db_handler.get_crawling_data(
                    selected_day, times, type)
               break
          except TypeError:
               times -= 1
               continue

     tagcloud_data = trans_tagcloud_data(crawling_data, 200)
     barchart_data = trans_barchart_data(crawling_data, 15)
     db_handler.close()

     return json.dumps({'tag': tagcloud_data, 'bar':barchart_data})


def trans_tagcloud_data(input, top_num):
     result = []
     
     for key, value in input.items():
          result.append({
               'x': key,
               'value': value
          })

     result = sorted(result, key=(lambda x: x['value']), reverse=True)
     return result[:top_num]


def trans_barchart_data(input, top_num):
     result = []

     for key, value in input.items():
          result.append([key, value])

     result = sorted(result, key=(lambda x: x[1]), reverse=True)
     return result[:top_num]
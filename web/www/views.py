from flask import Blueprint, render_template
from database import db_handler
from database.db_handler import DBHandler
views = Blueprint("views", __name__)

@views.route('/')
def index():
     db_handler = DBHandler()
     crawling_data = db_handler.get_crawling_data('2022-01-27', '6')
     print(type(crawling_data))
     db_handler.close()
     return render_template('index.html', value=crawling_data)
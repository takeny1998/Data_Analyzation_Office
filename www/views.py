from flask import Blueprint, render_template
from crawler import culture_crawler
views = Blueprint("views", __name__)

@views.route('/')
def index():
     return render_template('index.html')
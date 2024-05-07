from flask import Flask,render_template,request,redirect
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
def create_app():
    client = MongoClient(os.getenv("MONGODB_URI"))
    #取得我的database
    db = client['micro_blog']
    #取得我的collection
    collection = db['entries']
    app = Flask(__name__)


    @app.route('/',methods=["GET","POST"])
    def home():
        if request.method == "POST":
            entry_form = request.form.get("content")
            formatted_date = datetime.today().strftime("%Y-%m-%d")
            collection.insert_one(
            {'entry_form':entry_form,
            'formatted_date':formatted_date}
            )
            return redirect('/')
        else:
            data_all = collection.find({})
            entry_list = list()
            for data in data_all:
                entry_list.append(dict(
                    blog=data['entry_form'],
                    date=data['formatted_date']
                                    ))
            return render_template("home.html",entries=entry_list)
    return app
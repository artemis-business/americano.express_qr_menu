import os
from flask import Flask, jsonify, send_file
from flask_cors import CORS
import pymongo
import certifi

app = Flask(__name__)
CORS(app)

# ⚠️ MONGODB LİNKİNİ BURAYA YAPIŞTIR
MONGODB_URL =  "mongodb+srv://expresamericano084_db_user:wux07S6yL2zC8QSb@cluster0.963nuit.mongodb.net/"
client = pymongo.MongoClient(MONGODB_URL, tlsCAFile=certifi.where())
db = client["kafe_db"]
menu_koleksiyonu = db["menu"]
kategori_koleksiyonu = db["kategoriler"]

# Sistemin index.html'i kesin bulması için dosya yolu garantisi
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
HTML_YOLU = os.path.join(THIS_FOLDER, 'index.html')

@app.route('/')
def home():
    return send_file(HTML_YOLU)

@app.route('/api/menu', methods=['GET'])
def get_menu():
    try:
        kategoriler = list(kategori_koleksiyonu.find({}, {"_id": 0})) 
        urunler = list(menu_koleksiyonu.find().sort("_id", -1))
        for urun in urunler:
            urun['_id'] = str(urun['_id'])
        return jsonify({"status": "success", "kategoriler": kategoriler, "urunler": urunler})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

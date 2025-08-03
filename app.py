from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Koneksi ke MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mahasiswapolman']
collection = db['cempat']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data')
def data():
    usia = request.args.get('usia')
    nama = request.args.get('nama')
    jk = request.args.get('jk')

    query = {}
    if usia:
        query['usia_mhs'] = int(usia)
    if nama:
        query['nama_mhs'] = {'$regex': f'^{nama}', '$options': 'i'}
    if jk:
        query['jk_mhs'] = jk

    cempat = list(collection.find(query))
    return render_template("data.html", cempat=cempat)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        data = {
            'nim_mhs': request.form['nim'],
            'nama_mhs': request.form['nama'],
            'usia_mhs': int(request.form['usia']),
            'jk_mhs': request.form['jk'],
            'kota_mhs': request.form['kota'],
            'nomor_mhs': request.form['nomor']
        }
        collection.insert_one(data)
        return redirect(url_for('data'))
    return render_template('tambah.html')

if __name__ == '__main__':
    app.run(debug=True)

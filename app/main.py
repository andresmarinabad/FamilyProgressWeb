from datetime import date, datetime
from flask import Flask
from flask import render_template
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

app = Flask(__name__)

cred = credentials.Certificate('firebase.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://babies-progress.firebaseio.com'
})


class Bebe:
    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)

        current_year = date.today().year
        parts = self.date_fin.split('/')
        cumple = f'{parts[0]}/{parts[1]}/{current_year}'

        cumple_date = datetime.strptime(cumple, '%d/%m/%Y')
        today = datetime.today()

        if today >= cumple_date:
            self.date_fin = f'{parts[0]}/{parts[1]}/{current_year+1}'
            cumple_date = datetime.strptime(self.date_fin, '%d/%m/%Y')
        else:
            self.date_fin = f'{parts[0]}/{parts[1]}/{current_year}'

        dif_dates = (cumple_date - today).days
        self.progress = int(((365 - dif_dates)/365) * 100)

        if self.progress < 25:
            self.color = 'red'
        elif self.progress < 50:
            self.color = ''


def get_bebes():
    ref_bebes = db.reference('bebes')
    bebes = []
    for bebe in ref_bebes.get():
        info_bebe = db.reference(f'bebes/{bebe}')
        bebe = Bebe(info_bebe.get())
        bebes.append(bebe)

    bebes.sort(key=lambda x: x.orden)
    return bebes


@app.route("/")
def index():
    page_title = 'Family Progress'
    return render_template('index.html',
                           title=page_title,
                           bebes=get_bebes())


import re
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

class GoogleSheetForm(FlaskForm):
    sheet_link = StringField('Google Sheets Link', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def display_data():
    form = GoogleSheetForm()
    data = []

    if form.validate_on_submit():
        sheet_link = form.sheet_link.data
        sheet_id = extract_sheet_id(sheet_link)

        if sheet_id:
            SHEET_NAME = 'AAPL'
            url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
            df = pd.read_csv(url)

            df_sorted = df.sort_values(by='points')
            # df_sorted = df_sorted.reset_index(drop=True)

            data = list(df_sorted[['name', 'points']].itertuples(index=False, name=None))
            # data = list(df_sorted[['name', 'points']].to_records(index=False))

    return render_template('index.html', form=form, data=data)

def extract_sheet_id(sheet_link):
    pattern = r"/d/([a-zA-Z0-9-_]+)"

    match = re.search(pattern, sheet_link)

    if match:
        return match.group(1)  #id
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)

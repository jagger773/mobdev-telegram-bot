from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request

import pandas as pd

from src.data_manager import data_constants
from src.data_manager import date_builder
app  = Flask(__name__)

@app.route('/')
@app.route('/docs')
def api_document():
    return render_template('api_doc.html')

@app.route('/parse')
def parse_all():
    how = request.args.get('how')
    filename = data_constants.DATA_FOLDER + date_builder.get_current_date_for_xlsx()+".xlsx"
    data = pd.read_excel(filename)
    if not how:
        return "<h1>No arguments are provided</h1>"
    if how=="all":
        data.to_excel('all.xlsx')
        return send_from_directory('.', 'all.xlsx', as_attachment=True)
    data = data[data['Магазин'].str.startswith(how)]
    if data.empty:
        return "<h1>The given argument was not valid</h1>"
    data.to_excel(how+'.xlsx')
    return send_from_directory('.', how+'.xlsx', as_attachment=True)

if __name__=="__main__":
    app.run(port=5000)
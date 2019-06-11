from flask import render_template, redirect, url_for

from flask import request, jsonify
from flask_csv import send_csv
from project.main import bp


@bp.route("/")
def index():
    return redirect(url_for('task.list'))


@bp.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        return jsonify({"result": request.get_array(field_name='file')})
        return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data>
    <p><input type=file name=file><input type=submit value=Upload>
   </form>
    '''

@bp.route("/export", methods=['GET'])
def export_records():
    return excel.make_response_from_array([[1,2], [3, 4]], "csv",
                                          file_name="export_data")


@bp.route("/test")
def test():
    return send_csv([{"id": 42, "foo": "bar"}, {"id": 91, "foo": "baz"}],
         "test.csv", ["id", "foo"], cache_timeout=0)

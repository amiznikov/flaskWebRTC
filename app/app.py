# !/usr/bin/env python
# -*- coding: utf-8 -*-
# from __future__ import unicode_literal

from random import randrange as rnd
from flask import Flask,render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    app.gQueue.put('Same entery to "http://127.0.0.1:5000/index"')
    return render_template('index.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        stream_url = request.form['stream_url']
        stream_type = request.form['stream_type']
        stream_url, stream_type = str(stream_url), str(stream_type)
        print(stream_url, stream_type)
        # list_dict = { str(rnd(1000, 10000)) : stream_url}
        if "rtsp://" in stream_url:
            stream_id = str(rnd(1000, 10000))
            while stream_id in app.active_list.keys():
                stream_id = str(rnd(1000, 10000))
            else:
                app.active_list[stream_id] = stream_url
            # app.active_list.append(list_dict)
        print(app.active_list)
        return redirect(url_for('main.list'))
    else:
        return render_template('add.html', options=['rtsp'])


@app.route('/list')
def list():
    return render_template('list.html', list=app.active_list)

@app.route('/stream/<string:stream_id>')
def stream(stream_id):
    print("stream_id is " + stream_id)
    return render_template('stream.html')


@app.route('/get_stream_url', methods=['POST'])
def get_stream_url():
    stream_link = request.get_json().get('stream_link')
    stream_id = stream_link[stream_link.rfind('/')+1:]
    stream_url = app.active_list.get(stream_id)
    print (stream_id, stream_url)
    return jsonify({'result': stream_url})

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400

if __name__ == "__main__":
    app.run()

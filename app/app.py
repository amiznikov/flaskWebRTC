# !/usr/bin/env python
# -*- coding: utf-8 -*-
# from __future__ import unicode_literal

from random import randrange as rnd
from flask import Flask,render_template, request, redirect, url_for, jsonify, abort
from config import Flask_Config

app = Flask(__name__)
app.config.from_object(Flask_Config())


active_list = {}


def generate_id(stream_url):
    stream_id = str(rnd(1000, 10000))
    while stream_id in active_list:
        stream_id = str(rnd(1000, 10000))
    else:
        active_list[stream_id] = stream_url


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        stream_url = request.form['stream_url']
        stream_url = str(stream_url)
        if "rtsp://" in stream_url:
            generate_id()
        return redirect(url_for('list'))
    else:
        return render_template('add.html')


@app.route('/list')
def list():
    return render_template('list.html', list=active_list)


@app.route('/nourl')
def nostream():
    return render_template('nourl.html')


@app.route('/stream/<stream_id>')
def stream(stream_id):
    if stream_id in active_list:
        return render_template('stream.html')
    else:
        return abort(404)


@app.route('/get_stream_url', methods=['POST'])
def get_stream_url():
    stream_link = request.get_json().get('stream_link')
    stream_id = stream_link[stream_link.rfind('/')+1:]
    stream_url = active_list.get(stream_id)
    return jsonify(result=stream_url)

@app.errorhandler(Exception)
def http_error_handler(error):
    return render_template('nourl.html')

if __name__ == "__main__":
    generate_id('rtsp://b1.dnsdojo.com:1935/live/sys3.stream')
    generate_id('rtsp://184.72.239.149/vod/mp4:BigBuckBunny_115k.mov')
    app.run()

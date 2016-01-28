# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 01:32:43 2015

@author: kurner

Best to NOT try running this from inside Spyder.
Go to Terminal and use Ctrl-C to kill server when done.

sudo lsof -i :5000 
kill -9 pid

if you have to.
"""

from flask import Flask, request, render_template
import sqlite3 as sql
import os
import time
import datetime

target_path = '/Users/kurner/Documents/classroom_labs'
db_name = os.path.join(target_path, 'npym.db')

app = Flask(__name__)

@app.route("/")
def index():
    user_agent = request.headers.get('User-Agent')
    localtime = time.ctime(time.mktime(time.localtime()))
    gmt_time = time.ctime(time.mktime(time.gmtime()))
    return render_template('index.html', agent = user_agent,
                           local = localtime,
                           gmt = gmt_time)

@app.route("/slate/npym")
def npym_slate():
    user_agent = request.headers.get('User-Agent')
    localtime = time.ctime(time.mktime(time.localtime()))
    gmt_time = time.ctime(time.mktime(time.gmtime()))

    conn = sql.connect(db_name)
    c = conn.cursor()
    c.execute("""SELECT sl.group_name, sl.role_name, sl.friend_name, 
    ma.mtg_name, sl.start_date, sl.stop_date 
    FROM slates AS sl, member_attender AS ma
    WHERE sl.friend_id = ma.friend_id
    AND ({} BETWEEN sl.start_date AND sl.stop_date)
    AND sl.mtg_code = 'npym' 
    ORDER BY sl.group_name""".format(datetime.date.today().toordinal()))
    recs = list(c.fetchall())    
    conn.close()

    def converter(unixepoch):
        return datetime.date.fromordinal(unixepoch).isoformat()
        
    return render_template('npym_slate.html', recs = recs, agent = user_agent,
                           local = localtime,
                           gmt = gmt_time, converter = converter)

    
@app.route('/slate/<mtg_code>')
def meeting_slate(mtg_code):

    user_agent = request.headers.get('User-Agent')
    localtime = time.ctime(time.mktime(time.localtime()))
    gmt_time = time.ctime(time.mktime(time.gmtime()))

    conn = sql.connect(db_name)
    c = conn.cursor()
    c.execute("""SELECT * FROM slates AS sl
    WHERE ({} BETWEEN sl.start_date AND sl.stop_date)
    AND sl.mtg_code = '{}' 
    ORDER BY sl.group_name""".format(datetime.date.today().toordinal(), 
                                     mtg_code))

    recs = list(c.fetchall())    
    conn.close()

    def converter(unixepoch):
        return datetime.date.fromordinal(unixepoch).isoformat()
        
    return render_template('slate.html', recs = recs, agent = user_agent,
                           local = localtime,
                           gmt = gmt_time, converter = converter)

@app.route('/friends/<mtg_code>')
def friends(mtg_code):
    user_agent = request.headers.get('User-Agent')
    localtime = time.ctime(time.mktime(time.localtime()))
    gmt_time = time.ctime(time.mktime(time.gmtime()))
    conn = sql.connect(db_name)
    c = conn.cursor()
    
    c.execute("""SELECT * FROM member_attender ma 
    WHERE ma.mtg_code = '{}' 
    ORDER BY ma.friend_name""".format(mtg_code))
  
    today = datetime.date.today().toordinal()
    recs = [rec for rec in c.fetchall() 
        if ((rec[5] == None) or (not today > rec[5]))]
    conn.close()
    return render_template('friends.html', recs = recs, agent = user_agent,
                           local = localtime,
                           gmt = gmt_time)    
    
@app.route('/meetings/')
def meetings():
    user_agent = request.headers.get('User-Agent')
    localtime = time.ctime(time.mktime(time.localtime()))
    gmt_time = time.ctime(time.mktime(time.gmtime()))
    
    conn = sql.connect(db_name)
    c = conn.cursor()
    c.execute("""SELECT mtg_quarter, mtg_type, mtg_name, mtg_code FROM Meetings 
    ORDER BY mtg_quarter, mtg_type, mtg_name""")
    recs = list(c.fetchall())    
    conn.close()
    return render_template('meetings.html', recs = recs, agent = user_agent,
                           local = localtime,
                           gmt = gmt_time)
        
if __name__ == "__main__":
    app.run(debug=True)

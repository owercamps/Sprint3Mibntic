from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql

app=Flask(__name__)
app.secret_key='admin123'

@app.route('/')
@app.route('/index')
def index():
    con=sql.connect('db_web.db')
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute('select * from users')
    data=cur.fetchall()
    return render_template('index.html',datas=data)


@app.route('/add_user',methods=['GET','POST'])
def add_user():
    if request.method=='POST':
        uname=request.form['uname']
        contact=request.form['contact']
        con=sql.connect('db_web.db')
        cur=con.cursor()
        cur.execute('insert into users(UNAME,CONTACT) values (?,?)',(uname,contact))
        con.commit()
        flash('Usuario Guardado','success')
        return redirect(url_for('index'))
    return render_template('add_user.html')


@app.route('/edit_user/<string:uid>',methods=['GET','POST'])
def edit_user(uid):
    if request.method=='POST':
        uname=request.form['uname']
        contact=request.form['contact']
        con=sql.connect('db_web.db')
        cur=con.cursor()
        cur.execute('update users set UNAME=?, CONTACT=? where UID=?',(uname,contact,uid))
        con.commit()
        flash('Usuario Actualizado','success')
        return redirect(url_for('index'))
    
    con=sql.connect('db_web.db')
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute('select * from users where UID=?',(uid))
    data=cur.fetchone()
    return render_template('edit_user.html',datas=data)



@app.route('/delete_user/<string:uid>',methods=['GET'])
def delete_user(uid):
    con=sql.connect('db_web.db')
    cur=con.cursor()
    cur.execute('delete from users where UID=?',(uid))
    con.commit()
    flash('Usuario Eliminado','warning')
    return redirect(url_for('index'))





if __name__=='__main__':
    app.run(debug=True)
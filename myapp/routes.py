from flask import render_template, request, session, redirect, url_for, flash
from sqlalchemy.ext.horizontal_shard import set_shard_id

from myapp import app, db, CONSULTANTS
from myapp.models import Feedbacks, Workers


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'number' in session:
            return render_template('thanks.html')
        return render_template('index.html', consultants=CONSULTANTS)
    else:
        consult_name = request.form.get('consult_name')
        date = request.form.get('date')
        comment = request.form.get('comment')
        rating = request.form.get('rating')
        phone_number = request.form.get('phone')
        print(consult_name, date, comment, rating, phone_number)
        new_feed = Feedbacks(consult_name=consult_name, date_feed=date, comment=comment,
                             rating=rating, phone_number=phone_number)
        db.session.add(new_feed)
        db.session.commit()
        session['number'] = phone_number
        return render_template('thanks.html')


@app.route('/logout/', methods=['GET'])
def logout():
    if 'number' in session:
        session.pop('number', None)
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/admin_login/', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('admin_login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '123pass456!':
            session['admin'] = 'admin'
            return redirect(url_for('admin_panel'))

        else:
            flash('Ошибка ввода логина и пароля', 'errors')
            return render_template('admin_login.html')


@app.route('/admin_panel/', methods=['GET', 'POST'])
def admin_panel():
    if 'admin' in session:
        if request.method == 'GET':
            feedbacks = db.session.query(Feedbacks).all()
            workers = db.session.query(Workers).all()
            return render_template('admin_panel.html', feedbacks=feedbacks, workers=workers)
    else:
        return redirect(url_for('admin'))


@app.route('/admin_panel/delete/', methods=['POST'])
def del_comment():
    comment_id = request.form.get('but-del')
    comment_to_del = db.session.query(Feedbacks).filter(Feedbacks.id == comment_id).one_or_none()
    if comment_to_del:
        db.session.delete(comment_to_del)
        db.session.commit()
    return redirect(url_for('admin_panel'))


@app.route('/admin_panel/delete-worker/', methods=['POST'])
def del_worker():
    pass


@app.route('/admin_panel/add_worker/', methods=['POST'])
def add_worker():
    pass


@app.route('/admin_logout/')
def admin_logout():
    if 'admin' in session:
        session.pop('admin', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

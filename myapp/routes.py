from flask import render_template, request, session, redirect, url_for, flash
from datetime import date as dt

from myapp import app, db
from myapp.models import Feedbacks, Workers


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    date_today = dt.today()
    if 'sended_post' in session:
        return render_template('thanks.html')

    if request.method == 'GET':
        return render_template('index.html', consultants=app.config['CONSULTANTS'], date_today=date_today)
    else:
        consult_name = request.form.get('consult_name')
        date = request.form.get('date')
        comment = request.form.get('comment')
        rate = request.form.get('rate')
        phone_number = request.form.get('phone')

        if not check_date(date):
            flash('Вы ввели некорректную дату, год должен быть текущим, дата отзыва меньше или равна текущей', 'errors')
            return render_template('index.html', consultants=app.config['CONSULTANTS'], date_today=date_today)

        new_feed = Feedbacks(consult_name=consult_name, date_feed=date, comment=comment,
                             rate=rate, phone_number=phone_number)
        db.session.add(new_feed)
        db.session.commit()
        session['sended_post'] = True
        session.permanent = app.config['session_permanent']
        app.permanent_session_lifetime = app.config['session_time']
        return render_template('thanks.html')


@app.route('/admin_login/', methods=['GET', 'POST'])
def admin_login():
    if 'name' in session:
        if request.method == 'GET':
            if session['name'] == 'admin':
                return redirect(url_for('admin_panel'))
            return render_template('admin_login.html')
        else:
            username = request.form.get('username')
            password = request.form.get('password')

            if username == app.config['login_adm'] and password == app.config['pass_adm']:
                session['name'] = 'admin'
                session.permanent = app.config['session_permanent']
                app.permanent_session_lifetime = app.config['session_time']
                return redirect(url_for('admin_panel'))

            else:
                flash('Ошибка ввода логина и пароля', 'errors')
                return render_template('admin_login.html')
    else:
        session['name'] = 'defoult'
        return render_template('admin_login.html')


@app.route('/admin_panel/', methods=['GET'])
def admin_panel():
    if 'name' in session and session['name'] == 'admin':
        feedbacks = db.session.query(Feedbacks).all()
        workers = db.session.query(Workers).all()
        return render_template('admin_panel.html', feedbacks=feedbacks, workers=workers, app=app)
    else:
        session['name'] = 'defoult'
    return redirect(url_for('admin_login'))


@app.route('/admin_logout/')
def admin_logout():
    if 'name' in session:
        session.clear()
        session['name'] = 'defoult'
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


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
    worker_id = request.form.get('but-del-worker')
    worker_to_del = db.session.query(Workers).filter(Workers.id == worker_id).one_or_none()
    if worker_to_del:
        db.session.delete(worker_to_del)
        db.session.commit()
    app.config['CONSULTANTS'].pop(app.config['CONSULTANTS'].index(worker_to_del.full_name))
    return redirect(url_for('admin_panel'))


@app.route('/admin_panel/add_worker/', methods=['POST'])
def add_worker():
    full_name = request.form.get('full_name')
    worker_post = request.form.get('worker_post')
    contacts = request.form.get('contacts')
    new_worker = Workers(full_name=full_name, worker_post=worker_post, contacts=contacts)
    db.session.add(new_worker)
    db.session.commit()
    app.config['CONSULTANTS'].append(full_name)
    return redirect(url_for('admin_panel'))


@app.route('/admin_panel/change_pass/', methods=['POST'])
def change_pass():
    if 'name' in session and session['name'] == 'admin':
        lst_psw = request.form.get('last_password')
        new_psw = request.form.get('new_password')
        new_psw_rpt = request.form.get('new_password_repeat')
        if lst_psw == app.config['pass_adm']:
            if new_psw == new_psw_rpt:
                app.config['pass_adm'] = new_psw
                flash('Пароль изменен', 'success')
            else:
                flash('Пароли не совпадают', 'errors')
        else:
            flash('Старый пароль введен неверно', 'errors')
    return redirect(url_for('admin_panel'))


@app.route('/update_rating/', methods=['GET'])
def update_rating():
    if session['name'] == 'admin':
        all_workers = db.session.query(Workers).all()
        for worker in all_workers:
            all_worker_feeds = db.session.query(Feedbacks).filter(Feedbacks.consult_name == worker.full_name).all()
            if len(all_worker_feeds) != 0:
                worker.rating = round(sum([el.rate for el in all_worker_feeds]) / len(all_worker_feeds), 2)
            else:
                worker.rating = 0
            db.session.commit()
    return redirect(url_for('admin_panel'))


@app.route('/change_send_set/', methods=['GET'])
def change_send_set():
    if session['name'] == 'admin':
        if app.config['SEND_FLAG']:
            app.config['SEND_FLAG'] = False
        else:
            app.config['SEND_FLAG'] = True
    return redirect(url_for('admin_panel'))


def check_date(date):
    date_today = list(map(int, str(dt.today()).split('-')))
    date = list(map(int, date.split('-')))
    if date_today[0] == date[0] and date_today[1] >= date[1] and date_today[2] >= date[2]:
        return True
    return False


def check_number(number):
    red_number = []
    for el in number:
        if el.isdigit():
            pass

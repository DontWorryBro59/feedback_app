from flask import render_template, request, session, redirect, url_for, flash
from myapp import app, CONSULTANTS


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
        phone_number = request.form.get('number')
        print(consult_name, date, comment, rating, phone_number)
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

@app.route('/admin_panel/')
def admin_panel():
    if 'admin' in session:
        return render_template('admin_panel.html')
    else:
        return redirect(url_for('index'))

@app.route('/admin_logout/')
def admin_logout():
    if 'admin' in session:
        session.pop('admin', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


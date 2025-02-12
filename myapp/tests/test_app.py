from flask import request, session
from myapp import app, db
from myapp.models import Admins, Workers, Feedbacks


def test_start_app_config():
    """
    This function can check default app configuration
    :return:
    """
    assert app.config['pass_adm_def'] == 'admin'
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///./feedback.db'
    assert app.config['session_permanent'] == True
    assert app.config['SEND_FLAG'] == False

    with app.app_context():
        admins = db.session.query(Admins).all()
        consults = db.session.query(Workers).all()
        admin = admins[0]
    assert len(admins) == 1
    assert admin.username == 'admin'
    assert admin.check_password(app.config['pass_adm_def'])
    assert len(consults) == len(app.config['CONSULTANTS'])
    assert [consult.full_name for consult in consults] == app.config['CONSULTANTS']


def test_routes():
    """
    This function can check all routes in app
    :return:
    """
    with app.test_client() as test_client:
        assert test_client.get('/').status_code == 200
        assert test_client.get('/index/').status_code == 200
        assert test_client.get('/admin_login/').status_code == 200
        assert test_client.get('/admin_panel/').status_code == 302
        assert test_client.get('/admin_logout/').status_code == 302


def test_add_and_del_feedback():
    """
    This function can check add and del client's feedback
    :return:
    """
    with app.test_client() as test_client:
        #Имитируем добавление в БД клиентом отзыв о работе сотрудника
        test_post = Feedbacks(consult_name='test_name',
                             date_feed='2025-01-01',
                             comment='test_comment',
                             rate=0,
                             phone_number='+79999999999')
        #Удаляем пост клиента из панели администратора
        with app.app_context():
            db.session.add(test_post)
            db.session.commit()
            feed = db.session.query(Feedbacks).filter(Feedbacks.consult_name == 'test_name').first()
            assert feed == test_post
            test_client.post('/admin_panel/delete/', data={'but-del':feed.id})
            feed = db.session.query(Feedbacks).filter(Feedbacks.id == feed.id).first()
            assert feed == None


def test_add_and_del_workers():
    """
    This function can check add and del new workers in admin panel
    :return:
    """
    with app.test_client() as test_client:
        #Тест создания
        test_client.post('/admin_panel/add_worker/', data={'full_name': 'full_name_test',
                                                           'worker_post':'test_user',
                                                           'contacts':'test_contacts'})
        get_id = db.session.query(Workers).filter(Workers.full_name == 'full_name_test').first().id
        assert len(db.session.query(Workers).filter(Workers.full_name == 'full_name_test').all()) == 1

        #Тест удаления созданного работника
        test_client.post('/admin_panel/delete-worker/', data={'but-del-worker':get_id})
        check_user = db.session.query(Workers).filter(Workers.full_name == 'full_name_test').first()
        assert check_user == None

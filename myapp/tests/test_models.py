from myapp.models import Feedbacks, Admins, Workers


def test_admins_model():
    test_admin = Admins()
    test_admin.username = 'admin'
    test_admin.set_password('this_pass_true')

    assert test_admin.username == 'admin'
    assert test_admin.password_hash != 'this_pass_true'
    assert test_admin.check_password('this_pass_true') == True


def test_feedbacks_model():
    test_feedback = Feedbacks(
        consult_name="Иванов Иван Иванович",
        date_feed="2025-01-01",
        comment='test comment',
        rate=5,
        phone_number='+79999999999'
    )
    assert test_feedback.consult_name == "Иванов Иван Иванович"
    assert test_feedback.date_feed == '2025-01-01'
    assert test_feedback.comment == 'test comment'
    assert test_feedback.rate == 5
    assert test_feedback.phone_number == '+79999999999'
    # send по дефолту станет False при записи экземпляра класса в БД
    assert test_feedback.send == None


def test_workers_model():
    test_worker = Workers(
        full_name='Иванов Иван Иванович',
        worker_post='консультант',
        contacts='+79999999999',
    )
    assert test_worker.full_name == 'Иванов Иван Иванович'
    assert test_worker.worker_post == 'консультант'
    assert test_worker.contacts == '+79999999999'
    # rating по дефолту станет False при записи экземпляра класса в БД
    assert test_worker.rating == None
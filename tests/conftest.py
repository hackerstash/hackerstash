import pytest
from sqlalchemy import event
from hackerstash.db import db as _db
from hackerstash.server import app as _app, create_app


@pytest.fixture(scope='session')
def app(request):
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hackerstash:hackerstash@db:5432/hackerstash_test'
    return create_app()


@pytest.fixture(scope='session')
def db(app, request):
    with app.app_context():
        _db.drop_all()
        _db.create_all()


@pytest.fixture(scope='function', autouse=True)
def session(app, db, request):
    with app.app_context():
        conn = _db.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = _db.create_scoped_session(options=options)
        sess.begin_nested()

        @event.listens_for(sess(), 'after_transaction_end')
        def restart_savepoint(next_sess, trans):
            if trans.nested and not trans._parent.nested:
                next_sess.expire_all()
                sess.begin_nested()

        _db.session = sess
        yield sess

        sess.remove()
        txn.rollback()
        conn.close()
    return app


@pytest.fixture
def client(app, db, request, session):
    return app.test_client()

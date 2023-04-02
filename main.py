from website import create_app, DATABASEURI
from sqlalchemy import *
from flask import g

app = create_app()

engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    try:
        g.conn.close()
    except Exception as e:
        pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port = 8111)

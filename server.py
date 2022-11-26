from src.resources.TaskResource import TaskResource
from src.resources.TasksListResource import TasksListResource
# from src.tester import Tester

# tester = Tester()

# tester.run()
# tester.run_random()
# tester.run_batch(size=100)


from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from src.db.database import db


def create_app(db_connection='sqlite:///tarefas.db'):
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_connection
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    api = Api(app)
    api.add_resource(TasksListResource, '/tarefas')
    api.add_resource(TaskResource, '/tarefa/<string:id>')
    return app


app = create_app()


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


app.debug = True
if __name__ == '__main__':
    app.run(host="localhost", port=5000)

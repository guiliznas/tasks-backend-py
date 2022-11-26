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
from src.db.models import db

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


api.add_resource(TasksListResource, '/tarefas')
api.add_resource(TaskResource, '/tarefa/<string:id>')

app.debug = True
if __name__ == '__main__':
    app.run(host="localhost", port=5000)

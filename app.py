from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, fields, Resource


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Myrage;Auto23@localhost:3306/AWS'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)


class Task(db.Model):
    __tablename__ = "Tasks"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return "{" + f"id={self.id!r}, name={self.name!r}" + "}"


task_model = api.model('task', {
    'id': fields.Integer(readonly=True),
    'name': fields.String('task name')
})


@api.route('/tasks')
class Tasks(Resource):
    @api.doc('task list')
    @api.marshal_list_with(task_model)
    def get(self):
        return Task.query.all()

    @api.doc('add task')
    @api.expect(task_model)
    @api.marshal_with(task_model)
    def post(self):
        task = Task(**api.payload)
        db.session.add(task)
        db.session.commit()
        return task


@api.route('/tasks/<int:id>')
@api.doc(params={'id': 'task id'})
class Tasks_id(Resource):
    @api.doc('get task by id')
    @api.marshal_with(task_model)
    def get(self, id):
        return Task.query.get_or_404(id)

    @api.doc('delete task')
    @api.marshal_with(task_model)
    def delete(self, id):
        task = Task.get_or_404(id)
        db.session.delete(task)
        return "task deleted"

    @api.doc("update task")
    @api.expect(task_model)
    @api.marshal_with(task_model)
    def put(self,id):
        task_json = api.payload
        task = Task.query.get_or_404(id)
        task.name = task_json['name']
        db.session.commit()
        return task


@app.route('/init_db')
def init_and_populate():
    db.drop_all()
    db.create_all()
    return "database restored to original"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

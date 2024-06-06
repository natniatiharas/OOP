from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SECRET KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:etongzzz@localhost:5432/sqlalchemy'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return{
        'message': 'Welcome to building RESTful APIs with Flask and SQLAlchemy'
    }, 200
    
if __name__ == '__main__':
    app.run()

class User(db.Mode1):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(28), nullable=False, unique=True)
    public_id = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    todos = db.relationship('Todo', backref='owner', lazy='dynamic')
    
    def __repr__(self):
        return f'User <{self.email}>'
    
class Todo(db.Mode1):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(20), nullable=False)
    is_completed = db.Column(db.String, nullable=False)
    public_id = db.Column(db.String, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'Todo <{self.name}>'

import uuid
import requests

@app.route('/users/', methods=['POST'])
def create_user():
    data = requests.get.json()
    if not 'name' in data or not 'email' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Name or email not given'
        }), 400
    if len(data['name']) < 4 or len(data['email']) < 6:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Name and email must be contain minimum of 4 letters'
        }), 400
    u = User(
        name = data['name'],
        email=data['email'],
        is_admin=data.get('is admin', False),
        public_id=str(uuid.uuid())
    )

    db.session.add(u)
    db.session.commit()
    return {
        'id': u.public_id, 'name': u.name,
        'email': u.email, 'is admin': u.is_admin
    }, 201
    
@app.route('/users/<id>/', methods=['PUT'])
def update_user(id):
    data = requests.get_json()
    if 'name' not in data:
        return{
            'error': 'Bad Request',
            'message': 'Name field needs to be present'
        }, 400
    user = User.query.filter_by(public_id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return{
        'success': 'Data deleted successfully'
        }
        
@app.route('/todos/')
def get_todos():
    return jsonify([
        {
            'id': todo.public_id, 'name': todo.name,
            'owner': {
                'name': todo.owner.name,
                'email': todo.owner.email,
                'public_id': todo.owner.public_id
            }
        } for todo in Todo.query.all()
    ])
    
    
@app.route('/todos/<id>')
def get_todo(id):
    todo = Todo.query.filter_by(public_id=id).firs_or_404()
    return jsonify([
        {
            'id': todo.public_id, 'name': todo.name,
            'owner': {
                'name': todo.owner.name,
                'email': todo.owner.email,
                'public_id': todo.owner.public_id
            }
        } for todo in Todo.query.all()
    ])
    
@app.route('/todos/<id>')
def get_todo(id):
    todo = Todo.query.filter_by(public_id=id).first_or_404()
    return jsonify({
        'id': todo.public_id, 'name': todo.name,
        'owner': {
            'name': todo.owner.name,
            'email': todo.owner.email,
            'public_id': todo.owner.public_id
        }
    })
    
@app.route('/todos/', methods=['POST'])
def create_todo():
    data = requests.get_json()
    if not 'name' in data or not 'email' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Name of todo or email of creator not given'
        }), 400
    if len(data['name']) < 4:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Name of todo or email of creator not given'
        }), 400
    if len(data['name']) < 4:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Name of todo contain minimum of 4 letters'
        }), 400
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return{
            'error': 'Bad request',
            'message': 'Invalid email, no user with that email'
        }
    is_completed = data.get('is completed', False)
    todo = Todo(
        name=data['name'], user_id=user.id,
        is_completed=is_completed, public_id=str(uuid.uuid4())
    )
    db.session.add(todo)
    db.session.commit()
    return {
        'id': todo.public_id, 'name': todo.name, 'completed': todo.is_completed,
        'owner': {
            'name': todo.owner.name,
            'email': todo.owner.email,
            'is admin': todo.owner.is_admin
        }
    }, 201
    
@app.route('/todos/<id>/', methods=['PUT'])
def update_todo(id):
    data = requests.get_json()
    print(data)
    print('is completed' in data)
    if not 'name' in data or not 'is completed' in data:
        return{
            'error': 'Bad Request',
            'message': 'Name or completed fields need to be present'
        }, 400
    todo = Todo.query.filter_by(public_id=id).first_or_404()
    todo.name = data.get('name', todo.name)
    if 'is completed' in data:
        todo.is_completed=data['is completed']
    db.session.commit()
    return {
        'id': todo.public_id, 'name': todo.name,
        'is completed': todo.is_completed,
        'owner': {
            'name': todo.owner.name, 'email': todo.owner.email,
            'is admin': todo.owner.is_admin
        }
    }, 201
    
@app.route('/todos/<id>/', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.filter_by(public_id=id).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    return {
        'success': 'Data deleted successfully'
    }
    

@app.route('/todos/<id>/complete', methods=['PUT'])
def complete_todo(id):
    todo = Todo.query.filter_by(public_id=id).first_or_404()
    todo.is_completed = True
    db.session.commit()
    return jsonify({
        'message': 'Todo marked as completed',
        'todo_id': id
    })

@app.route('/todos/<id>/uncomplete', methods=['PUT'])
def uncomplete_todo(id):
    todo = Todo.query.filter_by(public_id=id).first_or_404()
    todo.is_completed = False
    db.session.commit()
    return jsonify({
        'message': 'Todo marked as uncompleted',
        'todo_id': id
    })

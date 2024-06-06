from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:etongzzz@localhost:5432/perpustakaan'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

class books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    publish_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    copies_available = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f'<Book {self.title}>'

class penulis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f'<Author {self.name}>'

class kategori(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class return_book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    return_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<ReturnBook {self.id}>'

class transaction_book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    transaction_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.Date)

    def __repr__(self):
        return f'<TransactionBook {self.id}>'

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    transactions = db.relationship('TransactionBook', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
@auth.verify_password
def verify_password(username, password):
    user = users.query.filter_by(username=username).first()
    if user and user.password == password:
        return user
    
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Unauthorized'}), 401
    user = users.query.filter_by(username=auth.username).first()
    if not user or not user.check_password(auth.password):
        return jsonify({'message': 'Unauthorized'}), 401
    token = user.generate_auth_token()
    return jsonify({'token': token.decode('UTF-8')})

@app.route('/logout')
@auth.login_required
def logout():
    return jsonify({'message': 'Logged out successfully'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data:
        return jsonify({'message': 'Missing username or password'}), 400
    if users.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    new_user = users(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/admin')
@auth.login_required
def admin():
    user = users.query.filter_by(username=auth.username()).first()
    if not user.is_admin:
        return jsonify({'message': 'Unauthorized, admin access required'}), 403

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.engine.execute("commit")
        db.metadata.create_all(db.engine)
    app.run(debug=True)

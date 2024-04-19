from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    CORS(app,resources={r"/*": {"origins": "*"}})
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://users_ttoz_user:h2o9r7DgqKuthBQlPh27TCWUSND812UQ@dpg-coh6juvsc6pc73ahpvq0-a.oregon-postgres.render.com:5432/users_ttoz'
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    return app

app=create_app()
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/', methods=['GET'])
def index():
    return {"message":"It's working"}


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user= User.query.filter_by(username=data['username']).first()
    if user:
        return {'message':'Username is already taken !'}
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return {'message': 'New user created!'}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return {'message': 'Login failed!'}
    login_user(user)
    return {'message': 'Logged in successfully!'}


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

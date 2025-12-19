from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user-notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique=True)
    email = db.Column(db.String(100), nullable = False, unique=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    notes = db.relationship('Note', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'email' : self.email,
            'created_at' : self.created_at.isoformat() if self.created_at else None,
            'notes' : [note.to_dict() for note in self.notes]
        }

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'user_id' : self.user_id,
            'username' : self.user.username,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"Error": "No user found."}), 404

@app.route('/users/<int:user_id>/notes', methods=['GET'])
def get_user_notes(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify([note.to_dict() for note in user.notes]), 200
    else:
        return jsonify({"Error" : "User not found."}), 404

@app.route('/users/<int:user_id>/notes', methods=['POST'])
def create_note(user_id):
    user = User.query.get(user_id)
    data = request.get_json()
    if not user:
        jsonify({"Error" : "No user found."}), 404

    new_note = Note(
        title = data['title'],
        content = data['content'],
        user_id = user.id
    )
    db.session.add(new_note)
    db.session.commit()

    return jsonify(new_note.to_dict()), 200

@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note_with_user(note_id):
    note = Note.query.get(note_id)

    if not note:
        return jsonify({"Error" : "No note found."}), 404

    return jsonify(note.to_dict()), 200

@app.route('/users/<int:user_id', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'Message': 'User does not exist.'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"Message" : "User deleted"}), 200



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_data.db'
db = SQLAlchemy(app)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    message = db.Column(db.String(255))

@app.route('/')
def index():
    chat_data = Chat.query.all()
    return render_template('index.html', chat_data=chat_data)

@app.route('/add_chat', methods=['GET', 'POST'])
def add_chat():
    if request.method == 'POST':
        user_input = request.form['user_input']
        new_chat = Chat(user='User', message=user_input)
        db.session.add(new_chat)
        db.session.commit()

    # Retrieve chat data after adding a new chat
    chat_data = Chat.query.all()

    return render_template('index.html', chat_data=chat_data)

@app.route('/delete_chat/<int:chat_id>', methods=['POST'])
def delete_chat(chat_id):
    chat_to_delete = Chat.query.get_or_404(chat_id)
    db.session.delete(chat_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/get_chat_data', methods=['GET'])
def get_chat_data():
    chat_data = Chat.query.all()
    data = [{'user': chat.user, 'message': chat.message} for chat in chat_data]
    return jsonify(data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
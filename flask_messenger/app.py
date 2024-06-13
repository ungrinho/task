from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from models import ChatMessage

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/friends')
def friends():
    return render_template('friends.html')

@app.route('/chats')
def chats():
    return render_template('chats.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        message = request.form['message']
        new_message = ChatMessage(sender='You', message=message)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('chat'))
    
    messages = ChatMessage.query.all()
    return render_template('chat.html', messages=messages)

def add_initial_messages():
    if not ChatMessage.query.first():
        initial_message = ChatMessage(sender='Friend', message='Hello! How can I help you today?')
        db.session.add(initial_message)
        db.session.commit()

if __name__ == '__main__':
    db.create_all()  
    add_initial_messages()  
    app.run(debug=True)

from flask import Flask, jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_data.db'

def get_chat_data():
    with app.app_context():
        response = app.test_client().get('/get_chat_data')
        if response.status_code == 200:
            return response.json
        else:
            print(f"Error retrieving chat data. Status code: {response.status_code}")
            return []

if __name__ == '__main__':
    chat_data = get_chat_data()
    if chat_data is not None:
        print("Chat History:")
        for chat in chat_data:
            print(f"{chat['user']}: {chat['message']}")
    else:
        print("Chat data is None. Please check for errors.")
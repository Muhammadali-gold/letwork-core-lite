from collections import defaultdict

from flask import Flask, request

app = Flask(__name__)

messages = defaultdict(list)

id_seq = 0

@app.route('/message', methods=['GET', 'POST'])
def message():
    basic_auth = request.authorization
    if not basic_auth:
        print('no basic auth')
        return 'no basic auth', 401

    global id_seq
    if request.method == 'POST':
        data = request.json
        if not data:
            print('no json')
            return 'no json', 400
        username, password = basic_auth.username, basic_auth.password
        print(username, password)
        if isinstance(data, dict):
            data['id'] = id_seq
            id_seq += 1
            messages[username].append(data)
        if isinstance(data, list):
            for d in data:
                d['id'] = id_seq
                id_seq += 1
                messages[username].append(d)

        return 'ok', 200
    if request.method == 'GET':
        return str(messages.get(basic_auth.username, {})), 200



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()


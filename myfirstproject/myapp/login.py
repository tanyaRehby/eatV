from flask import Flask, request
from api.views import LoginView

app = Flask(__name__)
@app.route('/LogIn', methods=['GET', 'POST'])
def login():
    LoginView.post()
    if request.method == 'POST':
        user_id = request.form['ID']
        password = request.form['psw']
        return f'ID: {user_id}, Password: {password}'
    return '''
    <html>
    <body>
    <font size="6">
    <link rel="stylesheet" type="text/css" href="SignAndLogin.css">
    <form method="post" action="/LogIn">
    <div class="container">
    <br></br><br></br>
    <font face="verdana" color="black"><h2>login:</h2></font>
    <h5>
        <font face="verdana" color="black"><label><b>ID</b></label></font>
    <br>
    <input type="text" placeholder="Enter your ID" name="ID" required>
        <br></br>
        <font face="verdana" color="black"><label><b>Password</b></label></font>
    <br>
        <input type="password" placeholder="Enter 5 digits's Password" name="psw" required>
    <br></br>
        <button type="submit">ok</button>
    </h5>
        </div>
    </form>
    </font>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)

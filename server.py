from flask import Flask

app = Flask(__name__)
app.secret_key = 'some_secret'

if __name__ == '__main__':
    from views import *
    app.run(debug=True)




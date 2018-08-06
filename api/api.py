from flask import Flask, render_template

api = Flask(__name__)

@api.route('/')
def hello_whale():
    return 'hello world again!'

if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0')

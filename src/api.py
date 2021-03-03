from flask import Flask, request

# def create_app():

app = Flask(__name__)

# api/book?id={attr_value} Example: /book?id=3735293
@app.route('/api/book')
def test():
    args = request.args
    return args['id']




@app.route('/')
def hello_world():
    return 'Hello, Roxanne!'

if __name__ == "__main__":
    app.run(debug=True)
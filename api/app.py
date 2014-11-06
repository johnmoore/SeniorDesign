#!flask/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

sensors = ['test1', 'test2']

@app.route('/sensors/list/', methods=['GET'])
def list_sensors():
    return jsonify({'sensors': sensors})

if __name__ == '__main__':
    app.run(debug=True)
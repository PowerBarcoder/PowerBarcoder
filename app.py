import time

import yaml
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import subprocess
from flask import Flask, Response, stream_with_context, render_template, request, jsonify
import yml_parser

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')
app.debug = True  # set debug flag to True


@socketio.on('run-procedure')
def run_procedure(data):

    socketio.emit('procedure-result', '<br>')
    socketio.emit('procedure-result', 'Generating config file...<br>')
    # Access form data
    form_data = data
    yml_parser.parsingFormDataToYml(form_data)
    yml_parser.parsingYmlToShell()

    socketio.emit('procedure-result', 'Data procedure started<br>')

    # 這個ok，就是沒換行不好看
    cmd = 'cd /PowerBarcoder/main && bash powerBarcode.sh 2>&1'
    # cmd_output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    # socketio.emit('procedure-result', cmd_output)
    # 這個好，相當完美
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
    for line in iter(p.stdout.readline, b''):
        # Process each line of output
        socketio.emit('procedure-result', line.decode('utf-8'))

    socketio.emit('procedure-result', 'done<br>')
    socketio.emit('procedure-result',
                  'Find your results in <a href="C:\\Users\\kwz50" target="_blank">C:\\Users\\kwz50</a>')


@app.route('/')
def home():
    # with open('/PowerBarcoder/data/test.txt', 'w') as f:
    #     f.write('test')
    return render_template('index.html')


@app.route('/start-data-procedure', methods=['POST'])
def start_data_procedure():
    #     # Call the run_procedure() function by emitting a socket event
    #     # socketio.emit('run-procedure', {'param1': 'value1', 'param2': 'value2'})
    return "Data procedure started."


@app.route('/result')
def home2():
    return render_template('result.html')


@app.route('/submit-form', methods=['POST'])
def submit_form():
    paramA = request.form.get('paramA')
    paramB = request.form.get('paramB')
    paramC = request.form.getlist('paramC')
    paramD = request.form.getlist('paramD')
    print(paramC)
    # Process form data here

    return jsonify({'status': str(paramC)})



if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.config['CORS_HEADERS'] = 'Content-Type'
    socketio.run(app, debug=True, host='0.0.0.0', allow_unsafe_werkzeug=True)



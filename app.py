import subprocess
import time
from datetime import datetime

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
import flask_socketio as ws

import yml_parser

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')
app.debug = True  # set debug flag to True


def ws_emit_procedure_result(msg, room_name):
    ws.emit('procedure-result', "[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "]" + msg, room=room_name)


@socketio.on('run-procedure')
def run_procedure(data):

    # Get current datetime
    formatted_datetime = datetime.now().strftime("%Y%m%d%H%M")

    ws.join_room(formatted_datetime)

    # socketio.emit('procedure-result', '<br>')
    ws.emit('procedure-result', '\r\n', room=formatted_datetime)
    ws_emit_procedure_result('Generating config file...\r\n',formatted_datetime)

    # [For Debug]
    # n=0
    # while True:
    #     socketio.emit('procedure-result', str(n)+'\r\n')
    #     n+=1
    #     time.sleep(1)

    # Access form data
    form_data = data
    yml_parser.parsingFormDataToYml(form_data)
    yml_parser.parsingYmlToShell(formatted_datetime)

    ws_emit_procedure_result('Data procedure started\r\n',formatted_datetime)

    cmd = 'cd /PowerBarcoder/main && bash powerBarcode.sh ' +formatted_datetime+ ' 2>&1'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)

    # throttle detection, we don't need virtual scrolling anymore
    throttle_seconds = int(time.time())
    temp_line = ""

    for line in iter(p.stdout.readline, b''):
        # Process each line of output
        if int(time.time()) - throttle_seconds > 1:
            temp_line += "[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "]" + line.decode('utf-8', 'ignore')
            socketio.emit('procedure-result', temp_line, room=formatted_datetime)
            temp_line = ""
            throttle_seconds = int(time.time())
        else:
            temp_line += "[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "]" + line.decode('utf-8', 'ignore')
    socketio.emit('procedure-result', temp_line, room=formatted_datetime)

    # [For Debug]
    # for line in iter(p.stdout.readline, b''):
    #     # Process each line of output
    #     socketio.emit('procedure-result', "["+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"]"+line.decode('utf-8'))

    ws_emit_procedure_result('done\r\n',formatted_datetime)
    ws_emit_procedure_result('Find your results in data/result/ folder\r\n',formatted_datetime)


@app.route('/')
def home():
    # passing default value to html (some parameters are not used in demo,
    # and are hard-coded in parsingYmlToShell() method)
    # Path
    default_myCutadaptPath = "/venv/cutadapt-venv/bin/"
    default_myFastpPath = "/usr/local/bin/"
    default_localBlastToolDir = "/usr/local/bin/"
    default_ampliconInfo = "/PowerBarcoder/data/amplicon_data/"
    default_resultDataPath = "/PowerBarcoder/data/result/"
    default_missList = "/PowerBarcoder/data/missingList.txt"
    default_R1FastqGz = "RUN_pool_R1.fastq.gz"
    default_R2FastqGz = "RUN_pool_R2.fastq.gz"
    default_summaryJsonFileName = "summary.json"
    default_summaryHtmlFileName = "summary.html"
    default_dada2LearnErrorFile = "/PowerBarcoder/data/dada2LearnErrorFile/"
    default_dada2BarcodeFile = "multiplex_cpDNAbarcode_clean.txt"

    # Locus (only the one for demo)
    default_nameOfLoci = "rbcLN"
    default_errorRateCutadaptor = 0.125
    default_minimumLengthCutadaptor = 70
    default_primerF = "GAGACTAAAGCAGGTGTTGGATTCA"
    default_primerFName = "fVGF"
    default_primerR = "TCAAGTCCACCRCGAAGRCATTC"
    default_primerRName = "rECL"
    # default_amplicon_r1 = "rbcLN_amplicon_r1.fq"
    # default_amplicon_r2 = "rbcLN_amplicon_r2.fq"
    default_barcodesFile1 = "barcodes_rbcL_start_0.fasta"
    default_barcodesFile2 = "barcodes_rbcLN_start2_0.fasta"
    default_sseqidFileName = "fermalies_rbcL.fasta"
    default_minimumLengthCutadaptorInLoop = 150
    default_customizedCoreNumber = 30

    return render_template('index.html',
                           default_myCutadaptPath=default_myCutadaptPath,
                           default_myFastpPath=default_myFastpPath,
                           default_localBlastToolDir=default_localBlastToolDir,
                           default_ampliconInfo=default_ampliconInfo,
                           default_resultDataPath=default_resultDataPath,
                           default_missList=default_missList,
                           default_R1FastqGz=default_R1FastqGz,
                           default_R2FastqGz=default_R2FastqGz,
                           default_summaryJsonFileName=default_summaryJsonFileName,
                           default_summaryHtmlFileName=default_summaryHtmlFileName,
                           default_dada2LearnErrorFile=default_dada2LearnErrorFile,
                           default_dada2BarcodeFile=default_dada2BarcodeFile,
                           default_nameOfLoci=default_nameOfLoci,
                           default_errorRateCutadaptor=default_errorRateCutadaptor,
                           default_minimumLengthCutadaptor=default_minimumLengthCutadaptor,
                           default_primerF=default_primerF,
                           default_primerFName=default_primerFName,
                           default_primerR=default_primerR,
                           default_primerRName=default_primerRName,
                           # default_amplicon_r1=default_amplicon_r1,
                           # default_amplicon_r2=default_amplicon_r2,
                           default_barcodesFile1=default_barcodesFile1,
                           default_barcodesFile2=default_barcodesFile2,
                           default_sseqidFileName=default_sseqidFileName,
                           default_minimumLengthCutadaptorInLoop=default_minimumLengthCutadaptorInLoop,
                           default_customizedCoreNumber=default_customizedCoreNumber
                           )


@app.route('/start-data-procedure', methods=['POST'])
def start_data_procedure():
    #     # Call the run_procedure() function by emitting a socket event
    #     # socketio.emit('run-procedure', {'param1': 'value1', 'param2': 'value2'})
    return "Data procedure started."


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.config['CORS_HEADERS'] = 'Content-Type'
    socketio.run(app, debug=True, host='0.0.0.0', allow_unsafe_werkzeug=True)

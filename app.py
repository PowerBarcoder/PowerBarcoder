import subprocess
import time

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO

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

    cmd = 'cd /PowerBarcoder/main && bash powerBarcode.sh 2>&1'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)

    # throttle detection, we don't need virtual scrolling anymore
    line_number = 0
    throttle_seconds = int(time.time())
    temp_line = ""

    for line in iter(p.stdout.readline, b''):
        # Process each line of output
        if line_number > 5 and int(time.time()) - throttle_seconds > 2:
            temp_line += line.decode('utf-8')
            socketio.emit('procedure-result', temp_line)
            temp_line = ""
            line_number = 0
            throttle_seconds = int(time.time())
        else:
            temp_line += line.decode('utf-8')
            line_number += 1

    socketio.emit('procedure-result', 'done<br>')
    socketio.emit('procedure-result',
                  'Find your results in data/result/ folder<br>')


@app.route('/')
def home():
    # passing default value to html (some parameters are not used in demo,
    # and are hard-coded in parsingYmlToShell() method)
    # Path
    default_myCutadaptPath = "/venv/cutadapt-venv/bin/"
    default_myFastpPath = "deprecated"
    default_localBlastToolDir = "/usr/local/bin/"
    default_ampliconInfo = "/PowerBarcoder/data/amplicon_data/"
    default_resultDataPath = "/PowerBarcoder/data/result/"
    default_missList = "/PowerBarcoder/data/missingList.txt"
    default_R1FastqGz = "/PowerBarcoder/data/amplicon_data/trim_RUN1.5_R1.fq.gz"
    default_R2FastqGz = "/PowerBarcoder/data/amplicon_data/trim_RUN1.5_R2.fq.gz"
    default_summaryJsonFileName = "221229RUN1_5.json"
    default_summaryHtmlFileName = "221229RUN1_5.html"
    default_dada2LearnErrorFile = "/PowerBarcoder/data/dada2LearnErrorFile/"
    default_dada2BarcodeFile = "multiplex_cpDNAbarcode_clean.txt"

    # Locus (only the one for demo)
    default_nameOfLoci = "rbcLN"
    default_errorRateCutadaptor = 0.125
    default_minimumLengthCutadaptor = 70
    default_primerF = "GAGACTAAAGCAGGTGTTGGATTCA"
    default_primerR = "TCAAGTCCACCRCGAAGRCATTC"
    default_amplicon_r1 = "rbcLN_amplicon_r1.fq"
    default_amplicon_r2 = "rbcLN_amplicon_r2.fq"
    default_barcodesFile1 = "barcodes_rbcL_start_0.fasta"
    default_barcodesFile2 = "barcodes_rbcLN_start2_0.fasta"
    default_sseqidFileName = "fermalies_rbcL.fasta"
    default_minimumLengthCutadaptorInLoop = 150
    default_customizedThreadNumber = 30

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
                           default_primerR=default_primerR,
                           default_amplicon_r1=default_amplicon_r1,
                           default_amplicon_r2=default_amplicon_r2,
                           default_barcodesFile1=default_barcodesFile1,
                           default_barcodesFile2=default_barcodesFile2,
                           default_sseqidFileName=default_sseqidFileName,
                           default_minimumLengthCutadaptorInLoop=default_minimumLengthCutadaptorInLoop,
                           default_customizedThreadNumber=default_customizedThreadNumber
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

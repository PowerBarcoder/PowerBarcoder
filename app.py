import subprocess
import time
from datetime import datetime

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
import flask_socketio as ws
import uuid
import yml_parser

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')
app.debug = True  # set debug flag to True
batch_name_set = set()


def ws_emit_procedure_result(msg, room_name):
    ws.emit('procedure-result', "[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "]" + msg, room=room_name)


@socketio.on('run-procedure')
def run_procedure(data):
    # Get current datetime
    formatted_datetime = datetime.now().strftime("%Y%m%d%H%M")

    # Join room, so that we can emit to specific room
    if formatted_datetime not in batch_name_set:
        batch_name_set.add(formatted_datetime)
        ws.join_room(formatted_datetime)
    else:
        temp_uuid = uuid.uuid4()
        ws.join_room(formatted_datetime + str(temp_uuid))
        ws_emit_procedure_result('Server is busy, please try again later\r\n', formatted_datetime + str(temp_uuid))
        ws.close_room(formatted_datetime + str(temp_uuid))
        return

    # socketio.emit('procedure-result', '<br>')
    ws.emit('procedure-result', '\r\n', room=formatted_datetime)
    ws_emit_procedure_result('Generating config file...\r\n', formatted_datetime)

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

    ws_emit_procedure_result('Data procedure started\r\n', formatted_datetime)

    cmd = 'cd /PowerBarcoder/main && bash powerBarcode.sh ' + formatted_datetime + ' 2>&1'
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

    ws_emit_procedure_result('done\r\n', formatted_datetime)
    ws_emit_procedure_result('Find your results in data/result/ folder\r\n', formatted_datetime)

    # Remove batch name from set
    batch_name_set.remove(formatted_datetime)
    ws.leave_room(formatted_datetime)


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
    devMode = 1
    ampliconMinimumLength = 1
    minimumOverlapBasePair = 4

    # Locus (rbcL demo)
    rbcL_nameOfLoci = "rbcLN"
    rbcL_errorRateCutadaptor = 0.125
    rbcL_minimumLengthCutadaptor = 70
    rbcL_primerF = "GAGACTAAAGCAGGTGTTGGATTCA"
    rbcL_primerFName = "fVGF"
    rbcL_primerR = "TCAAGTCCACCRCGAAGRCATTC"
    rbcL_primerRName = "rECL"
    rbcL_barcodesFile1 = "barcodes_rbcL_start_0.fasta"
    rbcL_barcodesFile2 = "barcodes_rbcLN_start2_0.fasta"
    rbcL_sseqidFileName = "fermalies_rbcL.fasta"
    rbcL_minimumLengthCutadaptorInLoop = 150
    rbcL_customizedCoreNumber = 30
    rbcL_blastReadChoosingMode = 1
    rbcL_blastParsingMode = 2

    # Locus (trnLF demo)
    trnLF_nameOfLoci = "trnLF"
    trnLF_errorRateCutadaptor = 0.125
    trnLF_minimumLengthCutadaptor = 70
    trnLF_primerF = "TGAGGGTTCGANTCCCTCTA"
    trnLF_primerFName = "L5675"
    trnLF_primerR = "GGATTTTCAGTCCYCTGCTCT"
    trnLF_primerRName = "F4121"
    trnLF_barcodesFile1 = "barcodes_trnL_3exonSTART_0.fasta"
    trnLF_barcodesFile2 = "barcodes_trnF_0.fasta"
    trnLF_sseqidFileName = "ftol_sanger_alignment_trnLLF_full_f.fasta"
    trnLF_minimumLengthCutadaptorInLoop = 150
    trnLF_customizedCoreNumber = 30
    trnLF_blastReadChoosingMode = 1  # 0: r1 r2 cat後blast, 1: r1 r2分開blast
    trnLF_blastParsingMode = 2

    return render_template('index.html',
                           # Path
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
                           devMode=devMode,
                           ampliconMinimumLength=ampliconMinimumLength,
                           minimumOverlapBasePair=minimumOverlapBasePair,
                           # Locus (rbcL demo)
                           rbcL_nameOfLoci=rbcL_nameOfLoci,
                           rbcL_errorRateCutadaptor=rbcL_errorRateCutadaptor,
                           rbcL_minimumLengthCutadaptor=rbcL_minimumLengthCutadaptor,
                           rbcL_primerF=rbcL_primerF,
                           rbcL_primerFName=rbcL_primerFName,
                           rbcL_primerR=rbcL_primerR,
                           rbcL_primerRName=rbcL_primerRName,
                           rbcL_barcodesFile1=rbcL_barcodesFile1,
                           rbcL_barcodesFile2=rbcL_barcodesFile2,
                           rbcL_sseqidFileName=rbcL_sseqidFileName,
                           rbcL_minimumLengthCutadaptorInLoop=rbcL_minimumLengthCutadaptorInLoop,
                           rbcL_customizedCoreNumber=rbcL_customizedCoreNumber,
                           rbcL_blastReadChoosingMode=rbcL_blastReadChoosingMode,
                           rbcL_blastParsingMode=rbcL_blastParsingMode,
                           # Locus (trnLF demo)
                           trnLF_nameOfLoci=trnLF_nameOfLoci,
                           trnLF_errorRateCutadaptor=trnLF_errorRateCutadaptor,
                           trnLF_minimumLengthCutadaptor=trnLF_minimumLengthCutadaptor,
                           trnLF_primerF=trnLF_primerF,
                           trnLF_primerFName=trnLF_primerFName,
                           trnLF_primerR=trnLF_primerR,
                           trnLF_primerRName=trnLF_primerRName,
                           trnLF_barcodesFile1=trnLF_barcodesFile1,
                           trnLF_barcodesFile2=trnLF_barcodesFile2,
                           trnLF_sseqidFileName=trnLF_sseqidFileName,
                           trnLF_minimumLengthCutadaptorInLoop=trnLF_minimumLengthCutadaptorInLoop,
                           trnLF_customizedCoreNumber=trnLF_customizedCoreNumber,
                           trnLF_blastReadChoosingMode=trnLF_blastReadChoosingMode,
                           trnLF_blastParsingMode=trnLF_blastParsingMode,
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

    # # Specify the path to the ssl folder
    # ssl_folder = 'ssl'
    # # Use the SSL certificate and key files from the ssl folder
    # ssl_context = (f'{ssl_folder}/smallfarmer_shop.crt', f'{ssl_folder}/smallfarmer.key')
    # # Run the app with socketio and HTTPS enabled
    # socketio.run(app, debug=True, host='0.0.0.0', port=5000, ssl_context=ssl_context, allow_unsafe_werkzeug=True)

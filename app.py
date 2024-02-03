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
    yml_parser.parsing_form_data_to_yml(form_data)
    yml_parser.parsing_yml_to_shell(formatted_datetime)

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
    # and are hard-coded in parsing_yml_to_shell() method)
    # Path
    default_mycutadapt_path = "/venv/cutadapt-venv/bin/"
    default_myfastp_path = "/usr/local/bin/"
    default_localblast_tool_dir = "/usr/local/bin/"
    default_amplicon_info = "/PowerBarcoder/data/amplicon_data/"
    default_result_data_path = "/PowerBarcoder/data/result/"
    default_miss_list = "/PowerBarcoder/data/missingList.txt"
    default_r1_fastq_gz = "RUN_pool_R1.fastq.gz"
    default_r2_fastq_gz = "RUN_pool_R2.fastq.gz"
    default_summary_json_file_name = "summary.json"
    default_summary_html_file_name = "summary.html"
    default_dada2_learn_error_file = "/PowerBarcoder/data/dada2LearnErrorFile/"
    default_dada2_barcode_file = "multiplex_cpDNAbarcode_clean.txt"
    dev_mode = 1
    amplicon_minimum_length = 1
    minimum_overlap_base_pair = 12  # default: 12, least: 4

    # Locus (rbcL demo)
    rbcl_name_of_loci = "rbcLN"
    rbcl_error_rate_cutadaptor = 0.125
    rbcl_minimum_length_cutadaptor = 70
    rbcl_primer_f = "GAGACTAAAGCAGGTGTTGGATTCA"
    rbcl_primer_f_name = "fVGF"
    rbcl_primer_r = "TCAAGTCCACCRCGAAGRCATTC"
    rbcl_primer_r_name = "rECL"
    rbcl_barcodes_file1 = "barcodes_rbcL_start_0.fasta"
    rbcl_barcodes_file2 = "barcodes_rbcLN_start2_0.fasta"
    rbcl_sseqid_file_name = "fermalies_rbcL.fasta"
    rbcl_minimum_length_cutadaptor_in_loop = 150
    rbcl_customized_core_number = 30
    rbcl_blast_read_choosing_mode = 1
    rbcl_blast_parsing_mode = 2

    # Locus (trnLF demo)
    trnlf_name_of_loci = "trnLF"
    trnlf_error_rate_cutadaptor = 0.125
    trnlf_minimum_length_cutadaptor = 70
    trnlf_primer_f = "TGAGGGTTCGANTCCCTCTA"
    trnlf_primer_f_name = "L5675"
    trnlf_primer_r = "GGATTTTCAGTCCYCTGCTCT"
    trnlf_primer_r_name = "F4121"
    trnlf_barcodes_file1 = "barcodes_trnL_3exonSTART_0.fasta"
    trnlf_barcodes_file2 = "barcodes_trnF_0.fasta"
    trnlf_sseqid_file_name = "ftol_sanger_alignment_trnLLF_full_f.fasta"
    trnlf_minimum_length_cutadaptor_in_loop = 150
    trnlf_customized_core_number = 30
    trnlf_blast_read_choosing_mode = 1  # 0: r1 r2 cat後blast, 1: r1 r2分開blast
    trnlf_blast_parsing_mode = 2

    return render_template('index.html',
                           # Path
                           default_mycutadapt_path=default_mycutadapt_path,
                           default_myfastp_path=default_myfastp_path,
                           default_localblast_tool_dir=default_localblast_tool_dir,
                           default_amplicon_info=default_amplicon_info,
                           default_result_data_path=default_result_data_path,
                           default_miss_list=default_miss_list,
                           default_r1_fastq_gz=default_r1_fastq_gz,
                           default_r2_fastq_gz=default_r2_fastq_gz,
                           default_summary_json_file_name=default_summary_json_file_name,
                           default_summary_html_file_name=default_summary_html_file_name,
                           default_dada2_learn_error_file=default_dada2_learn_error_file,
                           default_dada2_barcode_file=default_dada2_barcode_file,
                           dev_mode=dev_mode,
                           amplicon_minimum_length=amplicon_minimum_length,
                           minimum_overlap_base_pair=minimum_overlap_base_pair,
                           # Locus (rbcL demo)
                           rbcl_name_of_loci=rbcl_name_of_loci,
                           rbcl_error_rate_cutadaptor=rbcl_error_rate_cutadaptor,
                           rbcl_minimum_length_cutadaptor=rbcl_minimum_length_cutadaptor,
                           rbcl_primer_f=rbcl_primer_f,
                           rbcl_primer_f_name=rbcl_primer_f_name,
                           rbcl_primer_r=rbcl_primer_r,
                           rbcl_primer_r_name=rbcl_primer_r_name,
                           rbcl_barcodes_file1=rbcl_barcodes_file1,
                           rbcl_barcodes_file2=rbcl_barcodes_file2,
                           rbcl_sseqid_file_name=rbcl_sseqid_file_name,
                           rbcl_minimum_length_cutadaptor_in_loop=rbcl_minimum_length_cutadaptor_in_loop,
                           rbcl_customized_core_number=rbcl_customized_core_number,
                           rbcl_blast_read_choosing_mode=rbcl_blast_read_choosing_mode,
                           rbcl_blast_parsing_mode=rbcl_blast_parsing_mode,
                           # Locus (trnLF demo)
                           trnlf_name_of_loci=trnlf_name_of_loci,
                           trnlf_error_rate_cutadaptor=trnlf_error_rate_cutadaptor,
                           trnlf_minimum_length_cutadaptor=trnlf_minimum_length_cutadaptor,
                           trnlf_primer_f=trnlf_primer_f,
                           trnlf_primer_f_name=trnlf_primer_f_name,
                           trnlf_primer_r=trnlf_primer_r,
                           trnlf_primer_r_name=trnlf_primer_r_name,
                           trnlf_barcodes_file1=trnlf_barcodes_file1,
                           trnlf_barcodes_file2=trnlf_barcodes_file2,
                           trnlf_sseqid_file_name=trnlf_sseqid_file_name,
                           trnlf_minimum_length_cutadaptor_in_loop=trnlf_minimum_length_cutadaptor_in_loop,
                           trnlf_customized_core_number=trnlf_customized_core_number,
                           trnlf_blast_read_choosing_mode=trnlf_blast_read_choosing_mode,
                           trnlf_blast_parsing_mode=trnlf_blast_parsing_mode,
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

import os
import subprocess
import time
import uuid
import zipfile
from datetime import datetime
import re

import flask_socketio as ws
from flask import Flask, render_template, send_file
from flask_cors import CORS
from flask_socketio import SocketIO

import yml_parser

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')
app.debug = True  # set debug flag to True
batch_name_set = set()


def ws_emit_procedure_result(msg, room_name):
    """
    @brief Emit procedure result to a specific WebSocket room.
    @param msg: The message to emit.
    @param room_name: The name of the WebSocket room.
    """
    ws.emit('procedure-result', "[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "]" + msg, room=room_name)


def remove_ansi_escape_sequences(text):
    """
    @brief Remove ANSI escape sequences from the given text (used by tqdm). 
    @param text: The text containing ANSI escape sequences.
    @return: The text with ANSI escape sequences removed.
    """
    ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


@socketio.on('run-procedure')
def run_procedure(data):
    """
    @brief Run PowerBarcoder procedure.
    @param data: The data containing form inputs.
    @exception Exception: If an error occurs during the process.
    """
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
    ws.emit('procedure-result', f'Socket room name: {formatted_datetime}\r\n', room=formatted_datetime)
    ws_emit_procedure_result('Generating config file...\r\n', formatted_datetime)

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
        decoded_line = line.decode('utf-8', 'ignore')
        # Remove extra spaces from tqdm output
        decoded_line = decoded_line.replace('                                                             ', '')
        cleaned_line = remove_ansi_escape_sequences(decoded_line)
        # Always add timestamp
        timestamped_line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]{cleaned_line}"

        # If line contains tqdm output (progress bar), emit immediately
        if '%|' in cleaned_line:
            if temp_line:  # Emit accumulated non-progress lines first
                socketio.emit('procedure-result', temp_line, room=formatted_datetime)
                temp_line = ""
            socketio.emit('procedure-result', timestamped_line, room=formatted_datetime)
            throttle_seconds = int(time.time())
        else:
            # Accumulate non-progress lines with throttling
            if int(time.time()) - throttle_seconds > 1:
                temp_line += timestamped_line
                socketio.emit('procedure-result', temp_line, room=formatted_datetime)
                temp_line = ""
                throttle_seconds = int(time.time())
            else:
                temp_line += timestamped_line

    # Emit any remaining lines
    if temp_line:
        socketio.emit('procedure-result', temp_line, room=formatted_datetime)

    ws_emit_procedure_result('done\r\n', formatted_datetime)
    ws_emit_procedure_result('Find your results in data/result/ folder\r\n', formatted_datetime)

    # Remove batch name from set
    batch_name_set.remove(formatted_datetime)
    ws.leave_room(formatted_datetime)


@app.route('/')
def home():
    """
    @brief Render the home page with default values for the form. Some parameters are not used in demo, and are hard-coded in parsing_yml_to_shell() method
    @return: The rendered home page template.
    """
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
    default_denoise_mode = 0
    dev_mode = 1
    amplicon_minimum_length = 1

    # Locus (rbcL demo)
    rbcl_name_of_loci = "rbcLN"
    rbcl_error_rate_cutadapt = 0.125
    rbcl_minimum_length_cutadapt = 70
    rbcl_primer_f = "GAGACTAAAGCAGGTGTTGGATTCA"
    rbcl_primer_f_name = "fVGF"
    rbcl_primer_r = "TCAAGTCCACCRCGAAGRCATTC"
    rbcl_primer_r_name = "rECL"
    rbcl_barcodes_file1 = "barcodes_rbcL_start_0.fasta"
    rbcl_barcodes_file2 = "barcodes_rbcLN_start2_0.fasta"
    rbcl_sseqid_file_name = "fermalies_rbcL.fasta"
    rbcl_minimum_length_cutadapt_in_loop = 150
    rbcl_customized_core_number = 30
    rbcl_blast_read_choosing_mode = 1
    rbcl_blast_parsing_mode = 2
    rbcl_minimum_overlap_base_pair = 12
    rbcl_maximum_mismatch_base_pair = 0

    # Locus (trnLF demo)
    trnlf_name_of_loci = "trnLF"
    trnlf_error_rate_cutadapt = 0.125
    trnlf_minimum_length_cutadapt = 70
    trnlf_primer_f = "TGAGGGTTCGANTCCCTCTA"
    trnlf_primer_f_name = "L5675"
    trnlf_primer_r = "GGATTTTCAGTCCYCTGCTCT"
    trnlf_primer_r_name = "F4121"
    trnlf_barcodes_file1 = "barcodes_trnL_3exonSTART_0.fasta"
    trnlf_barcodes_file2 = "barcodes_trnF_0.fasta"
    trnlf_sseqid_file_name = "ftol_sanger_alignment_trnLLF_full_f.fasta"
    trnlf_minimum_length_cutadapt_in_loop = 150
    trnlf_customized_core_number = 30
    trnlf_blast_read_choosing_mode = 1  # 0: r1 r2 cat後blast, 1: r1 r2分開blast
    trnlf_blast_parsing_mode = 2
    trnlf_minimum_overlap_base_pair = 12
    trnlf_maximum_mismatch_base_pair = 0  # 為了一致使用預設的，都取 0

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
                           default_denoise_mode=default_denoise_mode,
                           dev_mode=dev_mode,
                           amplicon_minimum_length=amplicon_minimum_length,
                           # Locus (rbcL demo)
                           rbcl_name_of_loci=rbcl_name_of_loci,
                           rbcl_error_rate_cutadapt=rbcl_error_rate_cutadapt,
                           rbcl_minimum_length_cutadapt=rbcl_minimum_length_cutadapt,
                           rbcl_primer_f=rbcl_primer_f,
                           rbcl_primer_f_name=rbcl_primer_f_name,
                           rbcl_primer_r=rbcl_primer_r,
                           rbcl_primer_r_name=rbcl_primer_r_name,
                           rbcl_barcodes_file1=rbcl_barcodes_file1,
                           rbcl_barcodes_file2=rbcl_barcodes_file2,
                           rbcl_sseqid_file_name=rbcl_sseqid_file_name,
                           rbcl_minimum_length_cutadapt_in_loop=rbcl_minimum_length_cutadapt_in_loop,
                           rbcl_customized_core_number=rbcl_customized_core_number,
                           rbcl_blast_read_choosing_mode=rbcl_blast_read_choosing_mode,
                           rbcl_blast_parsing_mode=rbcl_blast_parsing_mode,
                           rbcl_minimum_overlap_base_pair=rbcl_minimum_overlap_base_pair,
                           rbcl_maximum_mismatch_base_pair=rbcl_maximum_mismatch_base_pair,
                           # Locus (trnLF demo)
                           trnlf_name_of_loci=trnlf_name_of_loci,
                           trnlf_error_rate_cutadapt=trnlf_error_rate_cutadapt,
                           trnlf_minimum_length_cutadapt=trnlf_minimum_length_cutadapt,
                           trnlf_primer_f=trnlf_primer_f,
                           trnlf_primer_f_name=trnlf_primer_f_name,
                           trnlf_primer_r=trnlf_primer_r,
                           trnlf_primer_r_name=trnlf_primer_r_name,
                           trnlf_barcodes_file1=trnlf_barcodes_file1,
                           trnlf_barcodes_file2=trnlf_barcodes_file2,
                           trnlf_sseqid_file_name=trnlf_sseqid_file_name,
                           trnlf_minimum_length_cutadapt_in_loop=trnlf_minimum_length_cutadapt_in_loop,
                           trnlf_customized_core_number=trnlf_customized_core_number,
                           trnlf_blast_read_choosing_mode=trnlf_blast_read_choosing_mode,
                           trnlf_blast_parsing_mode=trnlf_blast_parsing_mode,
                           trnlf_minimum_overlap_base_pair=trnlf_minimum_overlap_base_pair,
                           trnlf_maximum_mismatch_base_pair=trnlf_maximum_mismatch_base_pair
                           )


@app.route('/download/<room_name>', methods=['GET'])
def download_result(room_name):
    """
    @brief Download result from a specific room by loci.

    This function retrieves results stored in predefined folders and 
    compresses them into a ZIP file for download.

    ### trnLF result:
    - `/PowerBarcoder/data/result/{room}/trnLF_result/qcResult/validator/best`
    - `/PowerBarcoder/data/result/{room}/trnLF_result/qcResult/validator/all`
    - `/PowerBarcoder/data/result/{room}/trnLF_result/qcResult/qcReport.csv`

    ### rbcL result:
    - `/PowerBarcoder/data/result/{room}/rbcL_result/qcResult/validator/best`
    - `/PowerBarcoder/data/result/{room}/rbcL_result/qcResult/validator/all`
    - `/PowerBarcoder/data/result/{room}/rbcL_result/qcResult/qcReport.csv`

    More loci can be added in the future.

    @param room_name The name of the room.
    @return The ZIP file containing the result folders.
    @exception Exception If an error occurs during the process.
    """
    # List all result folders in room_name folder
    room_name_folder = f'/PowerBarcoder/data/result/{room_name}'
    result_folders = os.listdir(room_name_folder)
    # Get only the folders, not files
    result_folders = [f for f in result_folders if os.path.isdir(os.path.join(room_name_folder, f))]

    # Create a zip file
    zip_file_name = f'{room_name}_best_seq.zip'
    zip_file_path = os.path.join(room_name_folder, zip_file_name)

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for folder in result_folders:
            # Include 'best' folder contents
            best_seq_folder = os.path.join(room_name_folder, folder, 'qcResult', 'validator', 'best')
            for root, dirs, files in os.walk(best_seq_folder):
                for file in files:
                    src_file = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file, best_seq_folder)
                    zipf.write(src_file, os.path.join(folder, 'best', rel_path))

            # Include 'all' folder contents
            all_seq_folder = os.path.join(room_name_folder, folder, 'qcResult', 'validator', 'all')
            for root, dirs, files in os.walk(all_seq_folder):
                for file in files:
                    src_file = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file, all_seq_folder)
                    zipf.write(src_file, os.path.join(folder, 'all', rel_path))

            # Include 'qcReport.csv' file
            qc_report_file = os.path.join(room_name_folder, folder, 'qcResult', 'qcReport.csv')
            if os.path.exists(qc_report_file):
                zipf.write(qc_report_file, os.path.join(folder, 'qcReport.csv'))

    # Download the zip file
    return send_file(zip_file_path, as_attachment=True)


# health check
@app.route('/health')
def health():
    """
    @brief Health check endpoint.
    @return: 'OK' if the server is running.
    """
    return 'OK'


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.config['CORS_HEADERS'] = 'Content-Type'
    socketio.run(app, debug=True, host='0.0.0.0', allow_unsafe_werkzeug=True)

Vue.component('form-group', {
    props: ['label', 'tooltip', 'value', 'placeholder', 'class'],
    template: `
        <div :class="['form-group', class]">
            <label :for="label">{{ label }}</label>
            <input type="text" class="form-control" :id="label" :placeholder="placeholder" v-model="inputValue">
            <span :id="'tooltip' + label" class="fa fa-info-circle" data-bs-toggle="tooltip" :title="tooltip"></span>
        </div>
    `,
    data() {
        return {
            inputValue: this.value
        };
    },
    watch: {
        inputValue(newValue) {
            this.$emit('input', newValue);
        }
    }
});

Vue.component('modal', {
    props: ['title', 'darkMode', 'isDownloadEnabled'],
    template: `
        <div class="modal" id="myModal">
            <div class="modal-dialog modal-fullscreen">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{ title }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body" id="modalBodyDiv" style="padding-bottom: 0rem">
                        <div class="text-center mb-3"></div>
                        <div id="consoleDiv">
                            <pre style="margin-bottom: 0rem" id="console">
                                <div class="d-flex justify-content-center" id="loadPreviousDiv">
                                    <button class="btn btn-success" id="loadPreviousButton" style="display: none;" @click="loadPrevious">Load Previous</button>
                                </div>
                            </pre>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <div class="container">
                            <div class="row">
                                <div class="col-sm">
                                    <span>&nbsp</span>
                                    <div class="form-check form-switch">
                                        <input class="form-check-input" type="checkbox" role="switch" id="darkModeToggle" v-model="darkMode">
                                        <label class="form-check-label" for="darkModeToggle">Dark Mode</label>
                                    </div>
                                </div>
                                <div class="col-sm d-md-flex justify-content-md-end">
                                    <button class="btn btn-warning" id="downloadButton" :disabled="!isDownloadEnabled" @click="downloadResult">Download Result</button>
                                    &nbsp;
                                    <button class="btn btn-secondary" id="clearButton" @click="clearLog">Clear Log</button>
                                    &nbsp;
                                    <button class="btn btn-primary" id="saveButton" @click="saveLog">Save Execution Log</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    methods: {
        loadPrevious() {
            // Implement load previous functionality
        },
        clearLog() {
            $("#console").children().not("#loadPreviousDiv").remove();
        },
        saveLog() {
            let removedLogContent = removedData.join('\n') + '\n';
            let codeElement = document.getElementById('console');
            let codeElementCopy = codeElement.cloneNode(true);
            let divToRemove = codeElementCopy.querySelector("#loadPreviousDiv");
            if (divToRemove) {
                codeElementCopy.removeChild(divToRemove);
            }
            let innerText = (removedLogContent + codeElementCopy.innerText)
                .replaceAll("                ", "")
                .replace("                    [", "[")
                .replaceAll("<", "&lt;")
                .replaceAll(">", "&gt;");
            let downloadLink = document.createElement('a');
            downloadLink.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(innerText);
            downloadLink.download = 'log.txt';
            downloadLink.style.display = 'none';
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        },
        downloadResult() {
            let roomName = sessionStorage.getItem('roomName');
            window.open(HOST_URL + 'download/' + roomName, '_blank');
        }
    }
});

new Vue({
    el: '#app',
    data: {
        formData: {
            ampliconInfo: '',
            R1FastqGz: '',
            R2FastqGz: '',
            dada2LearnErrorFile: '',
            dada2BarcodeFile: '',
            dev_mode: '',
            denoise_mode: '',
            amplicon_minimum_length: '',
            nameOfLoci: [''],
            errorRateCutadapt: [''],
            minimumLengthCutadapt: [''],
            primerFName: [''],
            primerF: [''],
            primerRName: [''],
            primerR: [''],
            barcodesFile1: [''],
            barcodesFile2: [''],
            sseqidFileName: [''],
            minimumLengthCutadaptInLoop: [''],
            customizedCoreNumber: [''],
            blastReadChoosingMode: [''],
            blastParsingMode: ['']
        },
        isSubmitting: false,
        submitButtonText: 'Submit',
        darkMode: false,
        isDownloadEnabled: false
    },
    methods: {
        handleFormSubmission() {
            this.isSubmitting = true;
            this.submitButtonText = 'Please wait...';

            const formData = this.formData;

            $("#myModal").modal("show");
            $("#showModalButton").removeClass("d-none");
            socket.emit('run-procedure', formData);

            let seconds = 70;
            let countdownInterval = setInterval(() => {
                seconds--;
                if (seconds > 0) {
                    this.submitButtonText = `Please wait... ${seconds}s`;
                } else {
                    this.isSubmitting = false;
                    this.submitButtonText = 'Submit';
                    clearInterval(countdownInterval);
                }
            }, 1000);
        },
        openAdvanceMode() {
            const advanceModeElements = document.querySelectorAll('.advanceMode');
            advanceModeElements.forEach(element => {
                element.classList.toggle('hideAdvanceMode');
                element.classList.toggle('showAdvanceMode');
            });
        },
        autoCompleteWithDefaultPath() {
            this.formData.ampliconInfo = CONFIG.default_amplicon_info;
            this.formData.R1FastqGz = CONFIG.default_r1_fastq_gz;
            this.formData.R2FastqGz = CONFIG.default_r2_fastq_gz;
            this.formData.dada2LearnErrorFile = CONFIG.default_dada2_learn_error_file;
            this.formData.dada2BarcodeFile = CONFIG.default_dada2_barcode_file;
            this.formData.dev_mode = CONFIG.dev_mode;
            this.formData.amplicon_minimum_length = CONFIG.amplicon_minimum_length;
        },
        autoCompleteWithRBCLLoci() {
            this.formData.nameOfLoci[0] = CONFIG.rbcl_name_of_loci;
            this.formData.primerF[0] = CONFIG.rbcl_primer_f;
            this.formData.primerR[0] = CONFIG.rbcl_primer_r;
            this.formData.barcodesFile1[0] = CONFIG.rbcl_barcodes_file1;
            this.formData.barcodesFile2[0] = CONFIG.rbcl_barcodes_file2;
            this.formData.sseqidFileName[0] = CONFIG.rbcl_sseqid_file_name;
            this.formData.errorRateCutadapt[0] = CONFIG.rbcl_error_rate_cutadapt;
            this.formData.minimumLengthCutadapt[0] = CONFIG.rbcl_minimum_length_cutadapt;
            this.formData.minimumLengthCutadaptInLoop[0] = CONFIG.rbcl_minimum_length_cutadapt_in_loop;
            this.formData.customizedCoreNumber[0] = CONFIG.rbcl_customized_core_number;
            this.formData.minimum_overlap_base_pair[0] = CONFIG.rbcl_minimum_overlap_base_pair;
            this.formData.maximum_mismatch_base_pair[0] = CONFIG.rbcl_maximum_mismatch_base_pair;
            this.formData.blastReadChoosingMode[0] = CONFIG.rbcl_blast_read_choosing_mode;
            this.formData.blastParsingMode[0] = CONFIG.rbcl_blast_parsing_mode;
        },
        autoCompleteWithTRNLFLoci() {
            this.formData.nameOfLoci[0] = CONFIG.trnlf_name_of_loci;
            this.formData.primerF[0] = CONFIG.trnlf_primer_f;
            this.formData.primerR[0] = CONFIG.trnlf_primer_r;
            this.formData.barcodesFile1[0] = CONFIG.trnlf_barcodes_file1;
            this.formData.barcodesFile2[0] = CONFIG.trnlf_barcodes_file2;
            this.formData.sseqidFileName[0] = CONFIG.trnlf_sseqid_file_name;
            this.formData.errorRateCutadapt[0] = CONFIG.trnlf_error_rate_cutadapt;
            this.formData.minimumLengthCutadapt[0] = CONFIG.trnlf_minimum_length_cutadapt;
            this.formData.minimumLengthCutadaptInLoop[0] = CONFIG.trnlf_minimum_length_cutadapt_in_loop;
            this.formData.customizedCoreNumber[0] = CONFIG.trnlf_customized_core_number;
            this.formData.minimum_overlap_base_pair[0] = CONFIG.trnlf_minimum_overlap_base_pair;
            this.formData.maximum_mismatch_base_pair[0] = CONFIG.trnlf_maximum_mismatch_base_pair;
            this.formData.blastReadChoosingMode[0] = CONFIG.trnlf_blast_read_choosing_mode;
            this.formData.blastParsingMode[0] = CONFIG.trnlf_blast_parsing_mode;
        },
        addNewLocus() {
            this.formData.nameOfLoci.push('');
            this.formData.primerF.push('');
            this.formData.primerR.push('');
            this.formData.barcodesFile1.push('');
            this.formData.barcodesFile2.push('');
            this.formData.sseqidFileName.push('');
            this.formData.errorRateCutadapt.push('');
            this.formData.minimumLengthCutadapt.push('');
            this.formData.minimumLengthCutadaptInLoop.push('');
            this.formData.customizedCoreNumber.push('');
            this.formData.minimum_overlap_base_pair.push('');
            this.formData.maximum_mismatch_base_pair.push('');
            this.formData.blastReadChoosingMode.push('');
            this.formData.blastParsingMode.push('');
        },
        showModal() {
            $("#myModal").modal("show");
        },
        loadPrevious() {
            // Implement load previous functionality
        },
        clearLog() {
            $("#console").children().not("#loadPreviousDiv").remove();
        },
        saveLog() {
            let removedLogContent = removedData.join('\n') + '\n';
            let codeElement = document.getElementById('console');
            let codeElementCopy = codeElement.cloneNode(true);
            let divToRemove = codeElementCopy.querySelector("#loadPreviousDiv");
            if (divToRemove) {
                codeElementCopy.removeChild(divToRemove);
            }
            let innerText = (removedLogContent + codeElementCopy.innerText)
                .replaceAll("                ", "")
                .replace("                    [", "[")
                .replaceAll("<", "&lt;")
                .replaceAll(">", "&gt;");
            let downloadLink = document.createElement('a');
            downloadLink.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(innerText);
            downloadLink.download = 'log.txt';
            downloadLink.style.display = 'none';
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        },
        downloadResult() {
            let roomName = sessionStorage.getItem('roomName');
            window.open(HOST_URL + 'download/' + roomName, '_blank');
        }
    },
    mounted() {
        let socket = io.connect(HOST_URL, {
            withCredentials: true,
        });

        socket.on('procedure-result', (data) => {
            let newDiv = $("<code>");
            newDiv.text(data);
            $("#console").append(newDiv);
            newDiv.addClass("shellsession");

            if (this.darkMode) {
                hljs.highlightAll();
            }

            let lines = $("#console").find("code").length;
            if (lines > 50) {
                let firstLine = $("#console").find("code:first");
                let removedLine = firstLine.text().trim();
                removedData.push(removedLine);
                firstLine.remove();
                $("#loadPreviousButton").show();
            }

            if (data.includes("Socket room name:")) {
                let roomName = data.split(":")[1].trim();
                sessionStorage.setItem('roomName', roomName);
            }

            if (data.includes("Find your results in")) {
                this.isDownloadEnabled = true;
            }
        });
    }
});

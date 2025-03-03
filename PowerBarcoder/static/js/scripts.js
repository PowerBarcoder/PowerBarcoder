document.addEventListener('DOMContentLoaded', function () {
    // Function to auto-complete form fields with default values
    function autoCompleteWithDefaultPath() {
        document.getElementById('ampliconInfo').value = '{{default_amplicon_info}}';
        document.getElementById('R1FastqGz').value = '{{default_r1_fastq_gz}}';
        document.getElementById('R2FastqGz').value = '{{default_r2_fastq_gz}}';
        document.getElementById('dada2LearnErrorFile').value = '{{default_dada2_learn_error_file}}';
        document.getElementById('dada2BarcodeFile').value = '{{default_dada2_barcode_file}}';
        addRawFolderPath();
    }

    function autoCompleteWithRBCLLoci() {
        document.getElementById('nameOfLoci').value = '{{rbcl_name_of_loci}}';
        document.getElementById('errorRateCutadaptor').value = '{{rbcl_error_rate_cutadaptor}}';
        document.getElementById('minimumLengthCutadaptor').value = '{{rbcl_minimum_length_cutadaptor}}';
        document.getElementById('primerFName').value = '{{rbcl_primer_f_name}}';
        document.getElementById('primerF').value = '{{rbcl_primer_f}}';
        document.getElementById('primerRName').value = '{{rbcl_primer_r_name}}';
        document.getElementById('primerR').value = '{{rbcl_primer_r}}';
        document.getElementById('barcodesFile1').value = '{{rbcl_barcodes_file1}}';
        document.getElementById('barcodesFile2').value = '{{rbcl_barcodes_file2}}';
        document.getElementById('sseqidFileName').value = '{{rbcl_sseqid_file_name}}';
        document.getElementById('minimumLengthCutadaptorInLoop').value = '{{rbcl_minimum_length_cutadaptor_in_loop}}';
        document.getElementById('customizedCoreNumber').value = '{{rbcl_customized_core_number}}';
        document.getElementById('blastReadChoosingMode').value = '{{rbcl_blast_read_choosing_mode}}';
        document.getElementById('blastParsingMode').value = '{{rbcl_blast_parsing_mode}}';
        addRawFolderPath();
    }

    function autoCompleteWithTRNLFLoci() {
        document.getElementById('nameOfLoci').value = '{{trnlf_name_of_loci}}';
        document.getElementById('errorRateCutadaptor').value = '{{trnlf_error_rate_cutadaptor}}';
        document.getElementById('minimumLengthCutadaptor').value = '{{trnlf_minimum_length_cutadaptor}}';
        document.getElementById('primerFName').value = '{{trnlf_primer_f_name}}';
        document.getElementById('primerF').value = '{{trnlf_primer_f}}';
        document.getElementById('primerRName').value = '{{trnlf_primer_r_name}}';
        document.getElementById('primerR').value = '{{trnlf_primer_r}}';
        document.getElementById('barcodesFile1').value = '{{trnlf_barcodes_file1}}';
        document.getElementById('barcodesFile2').value = '{{trnlf_barcodes_file2}}';
        document.getElementById('sseqidFileName').value = '{{trnlf_sseqid_file_name}}';
        document.getElementById('minimumLengthCutadaptorInLoop').value = '{{trnlf_minimum_length_cutadaptor_in_loop}}';
        document.getElementById('customizedCoreNumber').value = '{{trnlf_customized_core_number}}';
        document.getElementById('blastReadChoosingMode').value = '{{trnlf_blast_read_choosing_mode}}';
        document.getElementById('blastParsingMode').value = '{{trnlf_blast_parsing_mode}}';
        addRawFolderPath();
    }

    function openAdvanceMode() {
        let advanceMode = document.getElementsByClassName("advanceMode");
        for (let i = 0; i < advanceMode.length; i++) {
            if (advanceMode[i].classList.contains("showAdvanceMode")) {
                advanceMode[i].classList.remove("showAdvanceMode");
                advanceMode[i].classList.add("hideAdvanceMode");
            } else {
                advanceMode[i].classList.add("showAdvanceMode");
                advanceMode[i].classList.remove("hideAdvanceMode");
            }
        }
    }

    function addRawFolderPath() {
        let rawFolderPathOriginDiv = document.getElementById("ampliconInfo");
        let rawFolderPathDestinationDivCollection = document.getElementsByClassName("rawFolderPath");
        for (let rawFolderPathDestinationDiv of rawFolderPathDestinationDivCollection) {
            rawFolderPathDestinationDiv.value = rawFolderPathOriginDiv.value;
        }
    }

    // Function to handle form submission and socket connection
    function handleFormSubmission(event) {
        event.preventDefault();

        const formData = {
            'ampliconInfo': $('#ampliconInfo').val(),
            'R1FastqGz': $('#R1FastqGz').val(),
            'R2FastqGz': $('#R2FastqGz').val(),
            'dada2LearnErrorFile': $('#dada2LearnErrorFile').val(),
            'dada2BarcodeFile': $('#dada2BarcodeFile').val(),
            'dev_mode': $('#dev_mode').val(),
            'amplicon_minimum_length': $('#amplicon_minimum_length').val(),
            'minimum_overlap_base_pair': $('#minimum_overlap_base_pair').val(),
            'nameOfLoci': $('.nameOfLoci').map(function () {
                return $(this).val();
            }).get(),
            'errorRateCutadaptor': $('.errorRateCutadaptor').map(function () {
                return $(this).val();
            }).get(),
            'minimumLengthCutadaptor': $('.minimumLengthCutadaptor').map(function () {
                return $(this).val();
            }).get(),
            'primerFName': $('.primerFName').map(function () {
                return $(this).val();
            }).get(),
            'primerF': $('.primerF').map(function () {
                return $(this).val();
            }).get(),
            'primerRName': $('.primerRName').map(function () {
                return $(this).val();
            }).get(),
            'primerR': $('.primerR').map(function () {
                return $(this).val();
            }).get(),
            'barcodesFile1': $('.barcodesFile1').map(function () {
                return $(this).val();
            }).get(),
            'barcodesFile2': $('.barcodesFile2').map(function () {
                return $(this).val();
            }).get(),
            'sseqidFileName': $('.sseqidFileName').map(function () {
                return $(this).val();
            }).get(),
            'minimumLengthCutadaptorInLoop': $('.minimumLengthCutadaptorInLoop').map(function () {
                return $(this).val();
            }).get(),
            'customizedCoreNumber': $('.customizedCoreNumber').map(function () {
                return $(this).val();
            }).get(),
            'blastReadChoosingMode': $('.blastReadChoosingMode').map(function () {
                return $(this).val();
            }).get(),
            'blastParsingMode': $('.blastParsingMode').map(function () {
                return $(this).val();
            }).get(),
        };

        $("#myModal").modal("show");
        $("#showModalButton").removeClass("d-none");
        socket.emit('run-procedure', formData);

        $('#submitButton').prop('disabled', true);
        $('#submitButton').val('Please wait...');

        let seconds = 70;
        let countdownInterval = setInterval(function () {
            seconds--;
            if (seconds > 0) {
                $('#submitButton').val('Please wait... ' + seconds + 's');
            } else {
                $('#submitButton').prop('disabled', false).val('Submit');
                clearInterval(countdownInterval);
            }
        }, 1000);
    }

    // Function to handle socket connection and console updates
    function handleSocketConnection() {
        let removedData = [];
        let max_lines = 50;

        document.getElementById('saveButton').addEventListener('click', function () {
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
        });

        document.getElementById('clearButton').addEventListener('click', function () {
            $("#console").children().not("#loadPreviousDiv").remove();
            removedData = [];
        });

        let socket = io.connect('{{ request.host_url }}', {
            withCredentials: true,
        });

        socket.on('procedure-result', function (data) {
            let newDiv = $("<code>");
            newDiv.text(data);
            $("#console").append(newDiv);
            newDiv.addClass("shellsession");

            if ($('#darkModeToggle').is(":checked")) {
                hljs.highlightAll();
            }

            let lines = $("#console").find("code").length;
            if (lines > max_lines) {
                let firstLine = $("#console").find("code:first");
                let removedLine = firstLine.text().trim();
                removedData.push(removedLine);
                firstLine.remove();
                $("#loadPreviousButton").show();
            }
        });

        $("#loadPreviousButton").click(function () {
            if (removedData.length > 0) {
                let previousData = removedData.pop();
                let newDiv = $("<code>");
                newDiv.text(previousData + "\n");
                newDiv.insertBefore($("#console code:first"));
                newDiv.addClass("shellsession");
                max_lines += 1;
            }
            if (removedData.length === 0) {
                $("#loadPreviousButton").hide();
            }
        });

        $('#darkModeToggle').on("change", function (event) {
            if ($(this).is(":checked")) {
                $('code').each(function () {
                    hljs.highlightElement(this);
                });
            } else {
                $('.hljs').removeClass('hljs');
                $('.hljs').removeClass('language-shell');
            }
        });
    }

    // Event listeners
    document.getElementById('autoCompletePath').addEventListener('click', autoCompleteWithDefaultPath);
    document.getElementById('autoCompleteWithRBCL').addEventListener('click', autoCompleteWithRBCLLoci);
    document.getElementById('autoCompleteWithTRNLF').addEventListener('click', autoCompleteWithTRNLFLoci);
    document.getElementById('addLocusButton').addEventListener('click', addRawFolderPath);
    document.querySelector('form').addEventListener('submit', handleFormSubmission);

    handleSocketConnection();
});

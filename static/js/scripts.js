// Define global function placeholders that will be used by inline HTML onclick handlers
window.autoCompleteWithDefaultPath = function () {
};
window.autoCompleteWithRBCLLoci = function () {
};
window.autoCompleteWithTRNLFLoci = function () {
};
window.openAdvanceMode = function () {
};
window.addRawFolderPath = function () {
};
window.addNewLocus = function () {
};
// Add new function placeholders for dynamic locus form population
window.populateLocusWithRBCL = function (locusIndex) {
};
window.populateLocusWithTRNLF = function (locusIndex) {
};

document.addEventListener('DOMContentLoaded', function () {
    // Track the number of locus forms
    let locusContainerCount = 0;

    // Initialize socket at the top level so it's accessible to all functions
    let socket = io.connect(HOST_URL, {
        withCredentials: true,
    });

    // Implement the functions and assign them to the global scope
    window.autoCompleteWithDefaultPath = function () {
        document.getElementById('ampliconInfo').value = CONFIG.default_amplicon_info;
        document.getElementById('R1FastqGz').value = CONFIG.default_r1_fastq_gz;
        document.getElementById('R2FastqGz').value = CONFIG.default_r2_fastq_gz;
        document.getElementById('dada2LearnErrorFile').value = CONFIG.default_dada2_learn_error_file;
        document.getElementById('dada2BarcodeFile').value = CONFIG.default_dada2_barcode_file;
        window.addRawFolderPath();
    };

    window.autoCompleteWithRBCLLoci = function () {
        document.getElementById('nameOfLoci').value = CONFIG.rbcl_name_of_loci;
        document.getElementById('errorRateCutadapt').value = CONFIG.rbcl_error_rate_cutadapt;
        document.getElementById('minimumLengthCutadapt').value = CONFIG.rbcl_minimum_length_cutadapt;
        document.getElementById('primerFName').value = CONFIG.rbcl_primer_f_name;
        document.getElementById('primerF').value = CONFIG.rbcl_primer_f;
        document.getElementById('primerRName').value = CONFIG.rbcl_primer_r_name;
        document.getElementById('primerR').value = CONFIG.rbcl_primer_r;
        document.getElementById('barcodesFile1').value = CONFIG.rbcl_barcodes_file1;
        document.getElementById('barcodesFile2').value = CONFIG.rbcl_barcodes_file2;
        document.getElementById('sseqidFileName').value = CONFIG.rbcl_sseqid_file_name;
        document.getElementById('minimumLengthCutadaptInLoop').value = CONFIG.rbcl_minimum_length_cutadapt_in_loop;
        document.getElementById('customizedCoreNumber').value = CONFIG.rbcl_customized_core_number;
        document.getElementById('blastReadChoosingMode').value = CONFIG.rbcl_blast_read_choosing_mode;
        document.getElementById('blastParsingMode').value = CONFIG.rbcl_blast_parsing_mode;
        document.getElementById('minimum_overlap_base_pair').value = CONFIG.rbcl_minimum_overlap_base_pair;
        document.getElementById('maximum_mismatch_base_pair').value = CONFIG.rbcl_maximum_mismatch_base_pair;
        window.addRawFolderPath();
    };

    window.autoCompleteWithTRNLFLoci = function () {
        document.getElementById('nameOfLoci').value = CONFIG.trnlf_name_of_loci;
        document.getElementById('errorRateCutadapt').value = CONFIG.trnlf_error_rate_cutadapt;
        document.getElementById('minimumLengthCutadapt').value = CONFIG.trnlf_minimum_length_cutadapt;
        document.getElementById('primerFName').value = CONFIG.trnlf_primer_f_name;
        document.getElementById('primerF').value = CONFIG.trnlf_primer_f;
        document.getElementById('primerRName').value = CONFIG.trnlf_primer_r_name;
        document.getElementById('primerR').value = CONFIG.trnlf_primer_r;
        document.getElementById('barcodesFile1').value = CONFIG.trnlf_barcodes_file1;
        document.getElementById('barcodesFile2').value = CONFIG.trnlf_barcodes_file2;
        document.getElementById('sseqidFileName').value = CONFIG.trnlf_sseqid_file_name;
        document.getElementById('minimumLengthCutadaptInLoop').value = CONFIG.trnlf_minimum_length_cutadapt_in_loop;
        document.getElementById('customizedCoreNumber').value = CONFIG.trnlf_customized_core_number;
        document.getElementById('blastReadChoosingMode').value = CONFIG.trnlf_blast_read_choosing_mode;
        document.getElementById('blastParsingMode').value = CONFIG.trnlf_blast_parsing_mode;
        document.getElementById('minimum_overlap_base_pair').value = CONFIG.trnlf_minimum_overlap_base_pair;
        document.getElementById('maximum_mismatch_base_pair').value = CONFIG.trnlf_maximum_mismatch_base_pair;
        window.addRawFolderPath();
    };

    window.openAdvanceMode = function () {
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
    };

    window.addRawFolderPath = function () {
        let rawFolderPathOriginDiv = document.getElementById("ampliconInfo");
        let rawFolderPathDestinationDivCollection = document.getElementsByClassName("rawFolderPath");
        for (let rawFolderPathDestinationDiv of rawFolderPathDestinationDivCollection) {
            rawFolderPathDestinationDiv.value = rawFolderPathOriginDiv.value;
        }
    };

    window.populateLocusWithRBCL = function (locusIndex) {
        document.getElementById(`nameOfLoci${locusIndex}`).value = CONFIG.rbcl_name_of_loci;
        document.getElementById(`errorRateCutadapt${locusIndex}`).value = CONFIG.rbcl_error_rate_cutadapt;
        document.getElementById(`minimumLengthCutadapt${locusIndex}`).value = CONFIG.rbcl_minimum_length_cutadapt;
        document.getElementById(`primerFName${locusIndex}`).value = CONFIG.rbcl_primer_f_name;
        document.getElementById(`primerF${locusIndex}`).value = CONFIG.rbcl_primer_f;
        document.getElementById(`primerRName${locusIndex}`).value = CONFIG.rbcl_primer_r_name;
        document.getElementById(`primerR${locusIndex}`).value = CONFIG.rbcl_primer_r;
        document.getElementById(`barcodesFile1${locusIndex}`).value = CONFIG.rbcl_barcodes_file1;
        document.getElementById(`barcodesFile2${locusIndex}`).value = CONFIG.rbcl_barcodes_file2;
        document.getElementById(`sseqidFileName${locusIndex}`).value = CONFIG.rbcl_sseqid_file_name;
        document.getElementById(`minimumLengthCutadaptInLoop${locusIndex}`).value = CONFIG.rbcl_minimum_length_cutadapt_in_loop;
        document.getElementById(`customizedCoreNumber${locusIndex}`).value = CONFIG.rbcl_customized_core_number;
        document.getElementById(`blastReadChoosingMode${locusIndex}`).value = CONFIG.rbcl_blast_read_choosing_mode;
        document.getElementById(`blastParsingMode${locusIndex}`).value = CONFIG.rbcl_blast_parsing_mode;
        document.getElementById(`minimum_overlap_base_pair${locusIndex}`).value = CONFIG.rbcl_minimum_overlap_base_pair;
        document.getElementById(`maximum_mismatch_base_pair${locusIndex}`).value = CONFIG.rbcl_maximum_mismatch_base_pair;
        window.addRawFolderPath();
    };

    window.populateLocusWithTRNLF = function (locusIndex) {
        document.getElementById(`nameOfLoci${locusIndex}`).value = CONFIG.trnlf_name_of_loci;
        document.getElementById(`errorRateCutadapt${locusIndex}`).value = CONFIG.trnlf_error_rate_cutadapt;
        document.getElementById(`minimumLengthCutadapt${locusIndex}`).value = CONFIG.trnlf_minimum_length_cutadapt;
        document.getElementById(`primerFName${locusIndex}`).value = CONFIG.trnlf_primer_f_name;
        document.getElementById(`primerF${locusIndex}`).value = CONFIG.trnlf_primer_f;
        document.getElementById(`primerRName${locusIndex}`).value = CONFIG.trnlf_primer_r_name;
        document.getElementById(`primerR${locusIndex}`).value = CONFIG.trnlf_primer_r;
        document.getElementById(`barcodesFile1${locusIndex}`).value = CONFIG.trnlf_barcodes_file1;
        document.getElementById(`barcodesFile2${locusIndex}`).value = CONFIG.trnlf_barcodes_file2;
        document.getElementById(`sseqidFileName${locusIndex}`).value = CONFIG.trnlf_sseqid_file_name;
        document.getElementById(`minimumLengthCutadaptInLoop${locusIndex}`).value = CONFIG.trnlf_minimum_length_cutadapt_in_loop;
        document.getElementById(`customizedCoreNumber${locusIndex}`).value = CONFIG.trnlf_customized_core_number;
        document.getElementById(`blastReadChoosingMode${locusIndex}`).value = CONFIG.trnlf_blast_read_choosing_mode;
        document.getElementById(`blastParsingMode${locusIndex}`).value = CONFIG.trnlf_blast_parsing_mode;
        document.getElementById(`minimum_overlap_base_pair${locusIndex}`).value = CONFIG.trnlf_minimum_overlap_base_pair;
        document.getElementById(`maximum_mismatch_base_pair${locusIndex}`).value = CONFIG.trnlf_maximum_mismatch_base_pair;
        window.addRawFolderPath();
    };

    window.addNewLocus = function () {
        locusContainerCount++;
        let idString = 'locusContainer' + locusContainerCount.toString();
        // Get the container element where the new DOM will be appended
        const container = document.getElementById(idString);

        if (!container) {
            console.error("Container not found: " + idString);
            return;
        }

        // Show the horizontal rule
        const hr = document.getElementById('locusHr' + locusContainerCount);
        if (hr) {
            hr.classList.remove('d-none');
        }

        // Create a new div element
        const newDiv = document.createElement('div');

        // Create the content for the new div element with CONFIG values
        const content = `
<div class="border border-gray p-3 bg-light">
            <div class="d-flex align-items-center">
                <h4 class="m-0">Locus ${locusContainerCount + 1}</h4>
                <button id="locusFormContainerToggleBtn${locusContainerCount.toString()}" class="btn btn-primary dropdown-toggle ms-auto" type="button"
                        data-bs-toggle="collapse" href="#locusFormContainer${locusContainerCount.toString()}" aria-expanded="false" aria-controls="pathFormContainer">
                    Hide the Locus Form
                </button>
            </div>
            <div id="locusFormContainer${locusContainerCount.toString()}" class="mt-3 show">
                <div class="form-group">
                    <label for="nameOfLoci${locusContainerCount}">Name of Loci:</label>
                    <div class="row">
                        <div class="col-12">
                            <input type="text" class="form-control nameOfLoci" id="nameOfLoci${locusContainerCount}" required="required" name="nameOfLoci" placeholder="${CONFIG.rbcl_name_of_loci}">
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label for="primerF${locusContainerCount}">
                        <span id="tooltip7${locusContainerCount}">Primer F: <i class="fa fa-question-circle"></i></span>
                        <span class="text-secondary information">
                            <i>
                                Primer F sequence for this locus
                            </i>
                        </span>
                    </label>
                    <div class="row">
                        <div class="col">
                            <input type="text" class="form-control primerFName" required="required"
                                   placeholder="${CONFIG.rbcl_primer_f_name}" id="primerFName${locusContainerCount}" name="primerFName">
                        </div>
                        <div class="col">
                            <input type="text" class="form-control primerF" id="primerF${locusContainerCount}"
                                   name="primerF" required="required"
                                   placeholder="${CONFIG.rbcl_primer_f}">
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label for="primerR${locusContainerCount}">
                        <span id="tooltip8${locusContainerCount}">Primer R: <i class="fa fa-question-circle"></i></span>
                        <span class="text-secondary information">
                            <i>
                                Primer R sequence for this locus
                            </i>
                        </span>
                    </label>
                    <div class="row">
                        <div class="col">
                            <input type="text" class="form-control primerRName" required="required"
                                   placeholder="${CONFIG.rbcl_primer_r_name}" id="primerRName${locusContainerCount}" name="primerRName">
                        </div>
                        <div class="col">
                            <input type="text" class="form-control primerR" id="primerR${locusContainerCount}"
                                   name="primerR" required="required"
                                   placeholder="${CONFIG.rbcl_primer_r}">
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label for="barcodesFile1${locusContainerCount}">Barcodes File 1:</label>
                    <div class="row">
                        <div class="col">
                            <input type="text" class="form-control rawFolderPath" required="required"
                                   placeholder="" disabled="disabled">
                        </div>
                        <div class="col">
                            <input type="text" class="form-control barcodesFile1" id="barcodesFile1${locusContainerCount}" required="required"
                                   name="barcodesFile1" placeholder="${CONFIG.rbcl_barcodes_file1}">
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label for="barcodesFile2${locusContainerCount}">Barcodes File 2:</label>
                    <div class="row">
                         <div class="col">
                            <input type="text" class="form-control rawFolderPath" required="required"
                                   placeholder="" disabled="disabled">
                        </div>
                        <div class="col">
                            <input type="text" class="form-control barcodesFile2"
                                   id="barcodesFile2${locusContainerCount}" required="required"
                                   name="barcodesFile2" placeholder="${CONFIG.rbcl_barcodes_file2}">
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label for="sseqidFileName${locusContainerCount}">Sseqid File:</label>
                    <div class="row">
                        <div class="col">
                            <input type="text" class="form-control rawFolderPath" required="required"
                                   placeholder="" disabled="disabled">
                        </div>
                        <div class="col">
                            <input type="text" class="form-control sseqidFileName"
                                   id="sseqidFileName${locusContainerCount}" required="required"
                                   name="sseqidFileName" placeholder="${CONFIG.rbcl_sseqid_file_name}">
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label for="errorRateCutadapt${locusContainerCount}">Cutadapt Error Rate:</label>
                    <div class="row">
                        <div class="col-12">
                            <input type="text" class="form-control errorRateCutadapt" id="errorRateCutadapt${locusContainerCount}" required="required"
                                   name="errorRateCutadapt" placeholder="${CONFIG.rbcl_error_rate_cutadapt}">
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label for="minimumLengthCutadapt${locusContainerCount}">Cutadapt Minimum Length:</label>
                    <div class="row">
                        <div class="col-12">
                            <input type="text" class="form-control minimumLengthCutadapt" id="minimumLengthCutadapt${locusContainerCount}" required="required"
                                   name="minimumLengthCutadapt" placeholder="${CONFIG.rbcl_minimum_length_cutadapt}">
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label for="minimumLengthCutadaptInLoop${locusContainerCount}">Cutadapt Minimum Length In Loop:</label>
                    <div class="row">
                        <div class="col-12">
                            <input type="text" class="form-control minimumLengthCutadaptInLoop"
                                   id="minimumLengthCutadaptInLoop${locusContainerCount}" required="required"
                                   name="minimumLengthCutadaptInLoop" placeholder="${CONFIG.rbcl_minimum_length_cutadapt_in_loop}">
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label for="customizedCoreNumber${locusContainerCount}">Cutadapt Customized Core Number:</label>
                    <div class="row">
                        <div class="col-12">
                            <input type="text" class="form-control customizedCoreNumber"
                                   id="customizedCoreNumber${locusContainerCount}" required="required"
                                   name="customizedCoreNumber" placeholder="${CONFIG.rbcl_customized_core_number}">
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label for="minimum_overlap_base_pair${locusContainerCount}"> DADA2 Minimum Overlap Base Pair:</label>
                    <div class="row">
                        <div class="col-12">
                            <input type="text" class="form-control minimum_overlap_base_pair"
                                   id="minimum_overlap_base_pair${locusContainerCount}"
                                   name="minimum_overlap_base_pair" required="required"
                                   placeholder="${CONFIG.rbcl_minimum_overlap_base_pair}">
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label for="minimum_overlap_base_pair${locusContainerCount}"> DADA2 Maximum Mismatch Base Pair:</label>
                    <div class="row">
                        <div class="col-12">
                            <input type="text" class="form-control maximum_mismatch_base_pair"
                                   id="maximum_mismatch_base_pair${locusContainerCount}"
                                   name="maximum_mismatch_base_pair" required="required"
                                   placeholder="${CONFIG.rbcl_maximum_mismatch_base_pair}">
                        </div>
                    </div>
                </div>
                <div class="form-group advanceMode hideAdvanceMode">
                    <label for="blastReadChoosingMode${locusContainerCount}">
                        <span id="tooltip95${locusContainerCount}">Blast Read Choosing Mode: <i class="fa fa-question-circle"></i></span>
                        <span class="text-secondary information">
                            <i>
                                Blast Read Choosing Mode, details can be found in PowerBarcoder manual.
                            </i>
                        </span>
                    </label>
                    <div class="row">
                        <div class="col-12">
                            <input type="text" class="form-control blastReadChoosingMode" id="blastReadChoosingMode${locusContainerCount}"
                                   name="blastReadChoosingMode"
                                   required="required" value="${CONFIG.rbcl_blast_read_choosing_mode}"
                                   placeholder="${CONFIG.rbcl_blast_read_choosing_mode}">
                        </div>
                    </div>
                </div>
                <div class="form-group advanceMode hideAdvanceMode">
                    <label for="blastParsingMode${locusContainerCount}">
                        <span id="tooltip94${locusContainerCount}">Blast Parsing Mode: <i class="fa fa-question-circle"></i></span>
                        <span class="text-secondary information">
                            <i>
                                Blast Parsing Mode, details can be found in PowerBarcoder manual.
                            </i>
                        </span>
                    </label>
                    <div class="row">
                        <div class="col-12">
                            <input type="text" class="form-control blastParsingMode" id="blastParsingMode${locusContainerCount}"
                                   name="blastParsingMode"
                                   required="required" value="${CONFIG.rbcl_blast_parsing_mode}"
                                   placeholder="${CONFIG.rbcl_blast_parsing_mode}">
                        </div>
                    </div>
                </div>
                <br>
                <div class="d-flex align-items-center">
                    <button id="autoCompleteWithRBCL${locusContainerCount}" class="btn btn-warning" type="button"
                            onclick="populateLocusWithRBCL(${locusContainerCount})">
                        Demo rbcL
                    </button>
                    &nbsp;
                    <button id="autoCompleteWithTRNLF${locusContainerCount}" class="btn btn-warning" type="button"
                            onclick="populateLocusWithTRNLF(${locusContainerCount})">
                        Demo trnLF
                    </button>
                </div>
            </div>
        </div>
`;

        // Set the innerHTML of the new div element to the content
        newDiv.innerHTML = content;

        // Append the new div element to the container element
        container.appendChild(newDiv);

        // disable the add button if the number of locus container is 4
        if (locusContainerCount === 4) {
            document.getElementById('addLocusButton').disabled = true;
        }

        window.addRawFolderPath();
    };

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
            'errorRateCutadapt': $('.errorRateCutadapt').map(function () {
                return $(this).val();
            }).get(),
            'minimumLengthCutadapt': $('.minimumLengthCutadapt').map(function () {
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
            'minimumLengthCutadaptInLoop': $('.minimumLengthCutadaptInLoop').map(function () {
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

        // Socket connection has been moved to the top level
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

            // set room name in session storage
            if (data.includes("Socket room name:")) {
                let roomName = data.split(":")[1].trim();
                sessionStorage.setItem('roomName', roomName);
            }

            // add download button when the result is ready
            if (data.includes("Find your results in")) {
                // Download Result
                document.getElementById('downloadButton').disabled = false;
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

        // Download result button
        document.getElementById('downloadButton').addEventListener('click', function () {
            // get room name from session storage
            let roomName = sessionStorage.getItem('roomName');
            // call api to download the result by room name (path parameter) in new page
            window.open(HOST_URL + 'download/' + roomName, '_blank');
        });
    }

    // Event listeners
    document.getElementById('autoCompletePath').addEventListener('click', window.autoCompleteWithDefaultPath);
    document.getElementById('autoCompleteWithRBCL').addEventListener('click', window.autoCompleteWithRBCLLoci);
    document.getElementById('autoCompleteWithTRNLF').addEventListener('click', window.autoCompleteWithTRNLFLoci);
    document.getElementById('addLocusButton').addEventListener('click', window.addNewLocus);
    document.querySelector('form').addEventListener('submit', handleFormSubmission);

    handleSocketConnection();
});

document.addEventListener('DOMContentLoaded', function () {
    // Track the number of locus forms
    let locusContainerCount = 0;

    // Initialize socket at the top level so it's accessible to all functions
    let socket = io.connect(HOST_URL, {
        withCredentials: true,
    });

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

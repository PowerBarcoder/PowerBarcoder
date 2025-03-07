// Import the form fields configuration
import locusFields from './locus-fields.js';
import pathFields from './path-fields.js';
import formGroupTemplate from '../js/templates/form-group.js';
import modalTemplate from '../js/templates/modal.js';
import pathFormTemplate from '../js/templates/path-form.js';
import locusFormTemplate from '../js/templates/locus-form.js';

Vue.component('form-group', {
    props: ['label', 'tooltip', 'value', 'placeholder', 'customClass', 'dual', 'secondaryPlaceholder', 'secondaryValue', 'secondaryId', 'inputId', 'inputClass', 'inputName', 'tooltipId', 'secondaryDisabled', 'infoText', 'ampliconInfoValue'],
    template: formGroupTemplate,
    data() {
        return {
            inputValue: this.value,
            secondaryInputValue: this.secondaryDisabled && this.ampliconInfoValue ? this.ampliconInfoValue : this.secondaryValue
        };
    },
    computed: {
        actualInputId() {
            return this.inputId || this.label.replace(/\s+/g, '');
        },
        actualInputName() {
            return this.inputName || this.actualInputId;
        },
        actualInputClass() {
            return this.inputClass || this.actualInputId;
        },
        actualTooltipId() {
            return this.tooltipId || 'tooltip' + this.label.replace(/\s+/g, '');
        },
        actualSecondaryId() {
            return this.secondaryId || this.actualInputId + 'Name';
        },
        secondaryClass() {
            return this.secondaryDisabled ? 'rawFolderPath' : this.actualSecondaryId;
        }
    },
    watch: {
        inputValue(newValue) {
            this.$emit('input', newValue);
        },
        secondaryInputValue(newValue) {
            this.$emit('secondary-input', newValue);
        },
        ampliconInfoValue: {
            immediate: true,
            handler(newValue) {
                // Update secondaryInputValue when ampliconInfoValue changes and field is disabled
                if (this.secondaryDisabled && newValue) {
                    this.secondaryInputValue = newValue;
                    this.$emit('secondary-input', newValue);
                }
            }
        }
    }
});

Vue.component('modal', {
    props: ['title', 'darkMode', 'isDownloadEnabled'],
    template: modalTemplate,
    methods: {
        loadPrevious() {
            if (window.removedData && window.removedData.length > 0) {
                let previousData = window.removedData.pop();
                let newDiv = $("<code>");
                newDiv.text(previousData + "\n");
                newDiv.insertBefore($("#console code:first"));
                newDiv.addClass("shellsession");
                
                if (this.darkMode) {
                    hljs.highlightElement(newDiv[0]);
                }
                
                if (window.removedData.length === 0) {
                    $("#loadPreviousButton").hide();
                }
            }
        },
        clearLog() {
            $("#console").children().not("#loadPreviousDiv").remove();
            window.removedData = [];
        },
        saveLog() {
            let removedLogContent = window.removedData.join('\n') + '\n';
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


// 新增 path-form 組件，透過 v-for 產生所有路徑欄位
Vue.component('path-form', {
    props: ['formData', 'pathFields'],
    computed: {
        CONFIG() {
            return CONFIG;
        }
    },
    template: pathFormTemplate
});


// Create a new component for locus forms with per-locus buttons
Vue.component('locus-form', {
    props: ['index', 'formData'],
    computed: {
        CONFIG() {
            return CONFIG;
        }
    },
    template: locusFormTemplate,
    data() {
        return {
            locusFields: locusFields,
        };
    },
    methods: {
        getPlaceholder(placeholderKey) {
            return CONFIG[`rbcl_${placeholderKey}`] || '';
        },
        fillWithRBCL() {
            this.$parent.autoCompleteWithLoci('rbcl', this.index);
        },
        fillWithTRNLF() {
            this.$parent.autoCompleteWithLoci('trnlf', this.index);
        }
    },
});

// Add a helper function to convert camelCase to snake_case
function toSnakeCase(str) {
    return str.replace(/([A-Z])/g, "_$1").toLowerCase();
}

new Vue({
    el: '#app',
    data: {
        formData: {
            ampliconInfo: '',
            R1FastqGz: '',
            R1FastqGzHelper: '',  // New secondary field for R1FastqGz
            R2FastqGz: '',
            R2FastqGzHelper: '',  // New secondary field for R2FastqGz
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
            // Add missing secondary array for barcodesFile1
            barcodesFile1Helper: [''],
            barcodesFile2: [''],
            // Add missing secondary array for barcodesFile2
            barcodesFile2Helper: [''],
            sseqidFileName: [''],
            // Add missing secondary array for sseqidFileName
            sseqidFileHelper: [''],
            minimumLengthCutadaptInLoop: [''],
            customizedCoreNumber: [''],
            blastReadChoosingMode: [''],
            blastParsingMode: [''],
            minimum_overlap_base_pair: [''],
            maximum_mismatch_base_pair: ['']
        },
        pathFields: pathFields, // 加入新建立的 pathFields 陣列
        isSubmitting: false,
        submitButtonText: 'Submit',
        darkMode: false,
        isDownloadEnabled: false,
        lociCount: 1,
        socket: null,
        pathFormVisible: true,
        locusFormVisible: true,
        locusFields: locusFields, // Add locusFields to the main Vue instance
        removedData: [],
        maxLines: 10,
    },
    methods: {
        handleFormSubmission() {
            // First check if the form is valid (all required fields are filled)
            const allInputsValid = this.validateAllInputs();
            
            if (!allInputsValid) {
                alert("Please fill in all required fields before submitting.");
                return;
            }
            
            this.isSubmitting = true;
            this.submitButtonText = 'Please wait...';

            const formData = this.formData;

            // // 添加 console.log 輸出完整表單數據
            // console.log('Form data being submitted:', JSON.stringify(formData, null, 2));

            $("#myModal").modal("show");
            $("#showModalButton").removeClass("d-none");
            this.socket.emit('run-procedure', formData);

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
        
        validateAllInputs() {
            // Basic path validation
            if (!this.formData.ampliconInfo || !this.formData.R1FastqGz || !this.formData.R2FastqGz || 
                !this.formData.dada2LearnErrorFile || !this.formData.dada2BarcodeFile) {
                return false;
            }
            
            // Validate all loci fields
            for (let i = 0; i < this.lociCount; i++) {
                for (const field of this.locusFields) {
                    if (!this.formData[field.name][i]) {
                        return false;
                    }
                }
            }
            
            return true;
        },
        
        openAdvanceMode() {
            const advanceModeElements = document.querySelectorAll('.advanceMode');
            advanceModeElements.forEach(element => {
                element.classList.toggle('hideAdvanceMode');
                element.classList.toggle('showAdvanceMode');
            });
        },
        autoCompleteWithDefaultPath() {
            // Use direct DOM approach to update fields
            this.directUpdatePathFields();
            
            // Also update Vue data model for consistency
            this.formData.ampliconInfo = CONFIG.default_amplicon_info;
            this.formData.R1FastqGz = CONFIG.default_r1_fastq_gz;
            this.formData.R2FastqGz = CONFIG.default_r2_fastq_gz;
            this.formData.dada2LearnErrorFile = CONFIG.default_dada2_learn_error_file;
            this.formData.dada2BarcodeFile = CONFIG.default_dada2_barcode_file;
            this.formData.dev_mode = CONFIG.dev_mode;
            this.formData.denoise_mode = CONFIG.default_denoise_mode;  // Added this line
            this.formData.amplicon_minimum_length = CONFIG.amplicon_minimum_length;
        },
        
        // Direct DOM manipulation for path fields
        directUpdatePathFields() {
            const fieldMapping = {
                // Map actual element IDs to CONFIG keys
                'ampliconInfo': 'default_amplicon_info',
                'R1FastqGz': 'default_r1_fastq_gz',
                'R2FastqGz': 'default_r2_fastq_gz',
                'dada2LearnErrorFile': 'default_dada2_learn_error_file',
                'dada2BarcodeFile': 'default_dada2_barcode_file',
                'dev_mode': 'dev_mode',
                'denoise_mode': 'default_denoise_mode', 
                'amplicon_minimum_length': 'amplicon_minimum_length',
            };
            
            // Use setTimeout to ensure DOM is ready
            setTimeout(() => {
                for (const [fieldId, configKey] of Object.entries(fieldMapping)) {
                    try {
                        const value = CONFIG[configKey];
                        const input = document.getElementById(fieldId);
                        
                        if (input) {
                            // Set the value directly on the DOM element
                            input.value = value;
                            // Also trigger input event to make Vue aware of the change
                            const event = new Event('input', { bubbles: true });
                            input.dispatchEvent(event);
                        } else {
                            console.error(`Element with ID "${fieldId}" not found`);
                        }
                    } catch (e) {
                        console.error(`Error updating ${fieldId}:`, e);
                    }
                }
            }, 100);
        },
        
        // Unified method to handle any locus autocomplete
        autoCompleteWithLoci(prefix, index) {
            // Use direct DOM manipulation to update fields
            this.directUpdateFields(prefix, index);
            
            for (const field of this.locusFields) {
                // Use configKey if provided; otherwise, convert field.name to snake_case
                const primaryKey = field.configKey || `${prefix}_${toSnakeCase(field.name)}`;
                this.formData[field.name][index] = CONFIG[primaryKey];
                if (field.secondary) {
                    // Skip updating secondary fields for barcodesFile1Helper, barcodesFile2Helper, sseqidFileHelper
                    if (!["barcodesFile1Helper", "barcodesFile2Helper", "sseqidFileHelper"].includes(field.secondary.name)) {
                        const secKey = field.secondary.configKey || `${prefix}_${toSnakeCase(field.secondary.name)}`;
                        this.formData[field.secondary.name][index] = CONFIG[secKey];
                    }
                }
            }
            
            // Force Vue to update
            this.$forceUpdate();
        },
        
        // Updated directUpdateFields to target specific locus by index
        directUpdateFields(prefix, index) {
            const locusNum = index + 1;
            
            // Use setTimeout to ensure DOM is ready
            setTimeout(() => {
                for (const field of this.locusFields) {
                    try {
                        const fieldId = field.name + (locusNum > 1 ? locusNum : '');
                        const primaryKey = field.configKey || `${prefix}_${toSnakeCase(field.name)}`;
                        const value = CONFIG[primaryKey];
                        const input = document.getElementById(fieldId);
                        
                        if (input) {
                            input.value = value;
                            const event = new Event('input', { bubbles: true });
                            input.dispatchEvent(event);
                        } else {
                            console.error(`Element with ID "${fieldId}" not found`);
                        }
                    } catch (e) {
                        console.error(`Error updating ${field.name}:`, e);
                    }
                    if (field.secondary && !["barcodesFile1Helper", "barcodesFile2Helper", "sseqidFileHelper"].includes(field.secondary.name)) {
                        try {
                            const secFieldId = field.secondary.name + (locusNum > 1 ? locusNum : '');
                            const secKey = field.secondary.configKey || `${prefix}_${toSnakeCase(field.secondary.name)}`;
                            const secValue = CONFIG[secKey];
                            const secInput = document.getElementById(secFieldId);
                            
                            if (secInput) {
                                secInput.value = secValue;
                                const event = new Event('input', { bubbles: true });
                                secInput.dispatchEvent(event);
                            } else {
                                console.error(`Element with ID "${secFieldId}" not found`);
                            }
                        } catch (e) {
                            console.error(`Error updating ${field.secondary.name}:`, e);
                        }
                    }
                }
            }, 100);
        },
        
        // Legacy methods for backward compatibility
        autoCompleteWithRBCLLoci() {
            this.autoCompleteWithLoci('rbcl', 0);
        },
        
        autoCompleteWithTRNLFLoci() {
            this.autoCompleteWithLoci('trnlf', 0);
        },
        
        addNewLocus() {
            // Add a new locus to the data arrays
            for (const field of this.locusFields) {
                this.formData[field.name].push('');
                if (field.secondary) {
                    this.formData[field.secondary.name].push('');
                }
            }
            
            // Increment the loci count
            this.lociCount++;
        },
        showModal() {
            $("#myModal").modal("show");
        },
        loadPrevious() {
            if (this.removedData && this.removedData.length > 0) {
                let previousData = this.removedData.pop();
                let newDiv = $("<code>");
                newDiv.text(previousData + "\n");
                newDiv.insertBefore($("#console code:first"));
                newDiv.addClass("shellsession");
                
                if (this.darkMode) {
                    hljs.highlightElement(newDiv[0]);
                }
                
                if (this.removedData.length === 0) {
                    $("#loadPreviousButton").hide();
                }
            }
        },
        clearLog() {
            $("#console").children().not("#loadPreviousDiv").remove();
            this.removedData = [];
        },
        saveLog() {
            let removedLogContent = this.removedData.join('\n') + '\n';
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
        },
        togglePathForm() {
            this.pathFormVisible = !this.pathFormVisible;
            $('#pathFormContainer').collapse(this.pathFormVisible ? 'show' : 'hide');
            $('#pathFormContainerToggleBtn').text(this.pathFormVisible ? 'Hide the Path Form' : 'Show the Path Form');
        },
        toggleLocusForm() {
            this.locusFormVisible = !this.locusFormVisible;
            $('#locusFormContainer').collapse(this.locusFormVisible ? 'show' : 'hide');
            $('#locusFormContainerToggleBtn').text(this.locusFormVisible ? 'Hide the Locus Form' : 'Show the Locus Form');
        },
        toggleDarkMode() {
            if (this.darkMode) {
                $('code').each(function() {
                    hljs.highlightElement(this);
                });
            } else {
                $('.hljs').removeClass('hljs');
                $('.hljs').removeClass('language-shell');
            }
        }
    },
    watch: {
        // Add a watcher for ampliconInfo to update all helper fields
        'formData.ampliconInfo': function(newValue) {
            // Update all secondary helper fields that are disabled
            for (const field of this.pathFields) {
                if (field.secondary && field.secondary.disabled) {
                    this.formData[field.secondary.name] = newValue;
                }
            }
            
            // Also update loci fields with disabled secondary fields
            for (let i = 0; i < this.lociCount; i++) {
                for (const field of this.locusFields) {
                    if (field.secondary && field.secondary.disabled) {
                        this.formData[field.secondary.name][i] = newValue;
                    }
                }
            }
        }
    },
    mounted() {
        // Initialize socket connection
        this.socket = io.connect(HOST_URL, {
            withCredentials: true,
        });

        this.socket.on('procedure-result', (data) => {
            let newDiv = $("<code>");
            newDiv.text(data);
            $("#console").append(newDiv);
            newDiv.addClass("shellsession");

            if (this.darkMode) {
                hljs.highlightAll();
            }

            let lines = $("#console").find("code").length;
            if (lines > this.maxLines) {
                let firstLine = $("#console").find("code:first");
                let removedLine = firstLine.text().trim();
                this.removedData.push(removedLine);
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

        // Set up collapse toggle button listeners
        $('#pathFormContainerToggleBtn').on('click', () => {
            setTimeout(() => {
                this.pathFormVisible = $('#pathFormContainer').hasClass('show');
                $('#pathFormContainerToggleBtn').text(this.pathFormVisible ? 'Hide the Path Form' : 'Show the Path Form');
            }, 350);
        });

        $('#locusFormContainerToggleBtn').on('click', () => {
            setTimeout(() => {
                this.locusFormVisible = $('#locusFormContainer').hasClass('show');
                $('#locusFormContainerToggleBtn').text(this.locusFormVisible ? 'Hide the Locus Form' : 'Show the Locus Form');
            }, 350);
        });

        // Watch dark mode changes
        this.$watch('darkMode', this.toggleDarkMode);

        // Set initial state for collapsible sections
        setTimeout(() => {
            $('#pathFormContainer').collapse('show');
            $('#locusFormContainer').collapse('show');
        }, 100);
        
        // Add explicit event listener for trnLF button
        const autoTRNLFBtn = document.getElementById('autoCompleteWithTRNLF');
        if (autoTRNLFBtn) {
            autoTRNLFBtn.addEventListener('click', this.autoCompleteWithTRNLFLoci.bind(this));
        } else {
            console.warn("Element 'autoCompleteWithTRNLF' not found in mounted.");
        }
        
        // Add explicit event listener for rbcL button
        const autoRBCLBtn = document.getElementById('autoCompleteWithRBCL');
        if (autoRBCLBtn) {
            autoRBCLBtn.addEventListener('click', this.autoCompleteWithRBCLLoci.bind(this));
        } else {
            console.warn("Element 'autoCompleteWithRBCL' not found in mounted.");
        }
        
        // Add explicit event listener for Demo Path button
        const autoDemoPathBtn = document.getElementById('autoCompletePath');
        if (autoDemoPathBtn) {
            autoDemoPathBtn.addEventListener('click', () => {
                this.autoCompleteWithDefaultPath();
            });
        } else {
            console.warn("Element 'autoCompletePath' not found in mounted.");
        }
    }
});

const pathFields = [
    {
        name: 'ampliconInfo',
        label: 'Raw Files Folder Path:',
        placeholderKey: 'default_amplicon_info',
        infoText: "The path of the raw data file within, including 'R1 fastq.gz', 'R2 fastq.gz', 'Dada2 Barcode file', 'Barcodes File 1', 'Barcodes File 2', and 'Sseqid File'."
    },
    {
        name: 'R1FastqGz',
        label: 'R1 fastq.gz file path:',
        placeholderKey: 'default_r1_fastq_gz',
        secondary: {
            name: 'R1FastqGzHelper',
            disabled: true,
            placeholderKey: 'default_amplicon_info',
        },
        infoText: "Raw data (.gz) path for R1 within the mounted folder ../amplicon_data/ ."
    },
    {
        name: 'R2FastqGz',
        label: 'R2 fastq.gz file path:',
        placeholderKey: 'default_r2_fastq_gz',
        secondary: {
            name: 'R2FastqGzHelper',
            disabled: true,
            placeholderKey: 'default_amplicon_info',
        },
        infoText: "Raw data (.gz) path for R2 within the mounted folder ../amplicon_data/ ."
    },
    {
        name: 'dada2LearnErrorFile',
        label: 'Dada2 Learn Error Files Folder Path:',
        placeholderKey: 'default_dada2_learn_error_file',
        infoText: "File path within the mounted folder for DADA2 learning error; put the fastq files under this path."
    },
    {
        name: 'dada2BarcodeFile',
        label: 'Dada2 Barcode File:',
        placeholderKey: 'default_dada2_barcode_file',
        infoText: "File name within the mounted folder '../amplicon_data/' for DADA2 learning error."
    },
    {
        name: 'dev_mode',
        label: 'Develop Mode:',
        placeholderKey: 'dev_mode',
        customClass: 'advanceMode hideAdvanceMode',
        infoText: `If you want to use the develop mode, please set it to "1", otherwise, set it to "0
        # 0: off (keep all the intermediate files),
        # 1: on  (cleanup all the intermediate files)
        `
    },
    {
        name: 'denoise_mode',
        label: 'Denoise Mode:',
        placeholderKey: 'default_denoise_mode',
        customClass: 'advanceMode hideAdvanceMode',
        infoText: "Denoise mode; default is 0, no error learning is 1, 2nd error learning is 2."
    },
    {
        name: 'amplicon_minimum_length',
        label: 'Amplicon Minimum Length:',
        placeholderKey: 'amplicon_minimum_length',
        customClass: 'advanceMode hideAdvanceMode',
        infoText: "The minimum length of amplicon; default is 1."
    }
];

export default pathFields;

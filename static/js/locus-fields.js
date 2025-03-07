const locusFields = [
    {
        name: 'nameOfLoci',
        label: 'Name of Loci',
        placeholderKey: 'name_of_loci',
        infoText: 'Locus name for your data',
    },
    {
        name: 'primerF',
        label: 'Primer F',
        placeholderKey: 'primer_f',
        secondary: {
            name: 'primerFName',
            placeholderKey: 'rbcl_primer_f_name',
        },
        infoText: 'Primer F sequence for this locus',
    },
    {
        name: 'primerR',
        label: 'Primer R',
        placeholderKey: 'primer_r',
        secondary: {
            name: 'primerRName',
            placeholderKey: 'rbcl_primer_r_name',
        },
        infoText: 'Primer R sequence for this locus',
    },
    {
        name: 'barcodesFile1',
        label: 'Barcodes File 1',
        placeholderKey: 'barcodes_file1',
        secondary: {
            name: 'barcodesFile1Helper',
            disabled: true,
            placeholderKey: 'default_amplicon_info',
        },
        infoText: 'Barcodes file within the mounted folder \'../amplicon_data/\' for R1 fastq, should be prepared by yourself',
    },
    {
        name: 'barcodesFile2',
        label: 'Barcodes File 2',
        placeholderKey: 'barcodes_file2',
        secondary: {
            name: 'barcodesFile2Helper',
            disabled: true,
            placeholderKey: 'default_amplicon_info',
        },
        infoText: 'Barcodes file within the mounted folder \'../amplicon_data/\' for R2 fastq, should be prepared by yourself',
    },
    {
        name: 'sseqidFileName',
        label: 'Sseqid File',
        placeholderKey: 'sseqid_file_name',
        secondary: {
            name: 'sseqidFileHelper',
            disabled: true,
            placeholderKey: 'default_amplicon_info',
        },
        infoText: 'Library file within the mounted folder \'../amplicon_data/\' for local BLAST, should be prepared by yourself. We suggest user to use close related species as the library.',
    },
    {
        name: 'errorRateCutadapt',
        label: 'Cutadapt Error Rate',
        placeholderKey: 'error_rate_cutadapt',
        inputClass: 'errorRateCutadaptor',
        infoText: 'Trimming sensitivity for cutadapt, details can be found in cutadapt manual',
    },
    {
        name: 'minimumLengthCutadapt',
        label: 'Cutadapt Minimum Length',
        placeholderKey: 'minimum_length_cutadapt',
        inputClass: 'minimumLengthCutadaptor',
        infoText: 'Trimming length threshold for cutadapt, details can be found in cutadapt manual',
    },
    {
        name: 'minimumLengthCutadaptInLoop',
        label: 'Cutadapt Minimum Length In Loop',
        placeholderKey: 'minimum_length_cutadapt_in_loop',
        inputClass: 'minimumLengthCutadaptorInLoop',
        infoText: 'I\'m thinking about to remove this parameter, but I\'m not sure yet.',
    },
    {
        name: 'customizedCoreNumber',
        label: 'Cutadapt Customized Core Number',
        placeholderKey: 'customized_core_number',
        infoText: 'PowerBarcoder supports multi-threading, set proper core number to speed up the analysis.',
    },
    {
        name: 'minimum_overlap_base_pair',
        label: 'DADA2 Minimum Overlap Base Pair',
        placeholderKey: 'minimum_overlap_base_pair',
        infoText: 'The minimum overlap base pair, default is 12',
    },
    {
        name: 'maximum_mismatch_base_pair',
        label: 'DADA2 Maximum Mismatch Base Pair',
        placeholderKey: 'maximum_mismatch_base_pair',
        infoText: 'Maximum number of mismatches allowed in the overlapping region, default is 0',
    },
    {
        name: 'blastReadChoosingMode',
        label: 'Blast Read Choosing Mode',
        placeholderKey: 'blast_read_choosing_mode',
        customClass: 'advanceMode hideAdvanceMode',
        infoText: 'Blast Read Choosing Mode, details can be found in PowerBarcoder manual.',
    },
    {
        name: 'blastParsingMode',
        label: 'Blast Parsing Mode',
        placeholderKey: 'blast_parsing_mode',
        customClass: 'advanceMode hideAdvanceMode',
        infoText: `Blast Parsing Mode, details can be found in PowerBarcoder manual.
                    blast_parsing_mode == "0":
                        - identity: 用3排序，取最高者出來，但不低於85
                        - qstart-qend: 用abs(7-8)取最大，但不低於序列長度的一半
                    blast_parsing_mode == "1":
                        - qstart-qend: 用abs(7-8)取最大，但不低於序列長度(qseqid_length)的一半
                        - identity: 用3排序，取最高者出來，但不低於85
                    blast_parsing_mode == "2":
                        - qstart-qend & identity 並行，用abs(7-8)*identity取最大，但不低於序列長度的一半，且identity要大於85
                    blast_parsing_mode == "3":
                        - e-value, 越小越好，但不高於0.01，1/10000代表每10000次align才可能出現一次更好的結果`
    },
];

export default locusFields;

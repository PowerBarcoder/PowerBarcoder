CREATE_QC_REPORT_TABLE = '''
    CREATE TABLE IF NOT EXISTS qcReport (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode TEXT,
        sample_name TEXT,
        cutadapt_demultiplex_r1 INTEGER,
        cutadapt_demultiplex_r2 INTEGER,
        cutadapt_trim_r1 INTEGER,
        cutadapt_trim_r2 INTEGER,
        dada2_filter_r1 INTEGER,
        dada2_filter_r2 INTEGER,
        highest_abundance_asv_header TEXT,
        highest_abundance_asv_sequence TEXT,
        highest_abundance_asv_length INTEGER,
        ambiguous_sites_number INTEGER,
        lowercase_sites_number INTEGER,
        blast_subject_id TEXT,
        blast_identity TEXT,
        blast_qstart_qend TEXT,
        identical_to_dada2_merge TEXT,
        dada2_denoise_r1_asv_count INTEGER,
        dada2_denoise_r1_best_asv_proportion REAL,
        dada2_denoise_r1_best_asv_number INTEGER,
        dada2_denoise_r1_hash_value TEXT,
        dada2_denoise_r2_asv_count INTEGER,
        dada2_denoise_r2_best_asv_proportion REAL,
        dada2_denoise_r2_best_asv_number INTEGER,
        dada2_denoise_r2_hash_value TEXT,
        dada2_merge_asv_count INTEGER,
        dada2_merge_best_asv_proportion REAL,
        dada2_merge_best_asv_number INTEGER,
        dada2_merge_hash_value TEXT,
        dada2_10n_concat_asv_count INTEGER,
        dada2_10n_concat_best_asv_proportion REAL,
        dada2_10n_concat_best_asv_number INTEGER,
        dada2_10n_concat_hash_value TEXT
    )
'''

INSERT_QC_REPORT_DATA = '''
    INSERT INTO qcReport (
        barcode, sample_name, cutadapt_demultiplex_r1, cutadapt_demultiplex_r2, cutadapt_trim_r1, cutadapt_trim_r2,
        dada2_filter_r1, dada2_filter_r2, highest_abundance_asv_header, highest_abundance_asv_sequence,
        highest_abundance_asv_length, ambiguous_sites_number, lowercase_sites_number, blast_subject_id,
        blast_identity, blast_qstart_qend, identical_to_dada2_merge, dada2_denoise_r1_asv_count,
        dada2_denoise_r1_best_asv_proportion, dada2_denoise_r1_best_asv_number, dada2_denoise_r1_hash_value,
        dada2_denoise_r2_asv_count, dada2_denoise_r2_best_asv_proportion, dada2_denoise_r2_best_asv_number,
        dada2_denoise_r2_hash_value, dada2_merge_asv_count, dada2_merge_best_asv_proportion,
        dada2_merge_best_asv_number, dada2_merge_hash_value, dada2_10n_concat_asv_count,
        dada2_10n_concat_best_asv_proportion, dada2_10n_concat_best_asv_number, dada2_10n_concat_hash_value
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''

CREATE_OVERALL_QC_REPORT_TABLE = '''
    CREATE TABLE IF NOT EXISTS overallQcReport (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        step TEXT,
        avg_q REAL,
        err_q REAL,
        num_seqs INTEGER,
        sum_len INTEGER,
        min_len INTEGER,
        max_len INTEGER
    )
'''

INSERT_OVERALL_QC_REPORT_DATA = '''
    INSERT INTO overallQcReport (step, avg_q, err_q, num_seqs, sum_len, min_len, max_len)
    VALUES (?, ?, ?, ?, ?, ?, ?)
'''

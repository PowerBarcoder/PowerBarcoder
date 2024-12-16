# GUI請先生出yml，再來用這支程式轉成shell script
import os
import yaml


# convert the formData to YAML
def parsing_form_data_to_yml(data):
    yaml_data = yaml.dump(data)
    with open('main/config.yml', 'w') as f:
        f.write("---\n")
        f.write(yaml_data)


# convert the YAML to shell script, with some fixed field
def parsing_yml_to_shell(batch_name: str):
    # Load YAML file
    with open('main/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    # Generate shell script (有#的代表使用者可以改)
    # path
    script = '#!/bin/bash\n'
    script += "datetime='" + batch_name + "/'\n"
    script += f"workingDirectory='/PowerBarcoder/main/'\n"
    script += f"myCutadaptPath='/venv/cutadapt-venv/bin/'\n"
    script += f"myFastpPath='/usr/local/bin/'\n"
    script += f"localBlastToolDir='/usr/local/bin/'\n"
    script += f"ampliconInfo='{str(config['ampliconInfo']).strip()}'\n"  # ampliconInfo
    script += f"resultDataPath='/PowerBarcoder/data/result/'$datetime\n"
    script += f"missList='/PowerBarcoder/data/missingList.txt'\n"
    script += f"R1FastqGz='{str(config['R1FastqGz']).strip()}'\n"  # R1FastqGz
    script += f"R2FastqGz='{str(config['R2FastqGz']).strip()}'\n"  # R2FastqGz
    script += f"summaryJsonFileName='summary.json'\n"
    script += f"summaryHtmlFileName='summary.html'\n"
    script += f"dada2LearnErrorFile='{str(config['dada2LearnErrorFile']).strip()}'\n"  # dada2LearnErrorFile
    script += f"dada2BarcodeFile='{str(config['dada2BarcodeFile']).strip()}'\n"  # dada2BarcodeFile
    script += f"amplicon_minimum_length='{str(config['amplicon_minimum_length']).strip()}'\n"  # amplicon_minimum_length (default: 1)
    # script += f"minimum_overlap_base_pair='{str(config['minimum_overlap_base_pair']).strip()}'\n"  # minimum_overlap_base_pair (default: 4)
    # Dev Only
    script += f"denoise_mode='{str(config['denoise_mode']).strip()}'\n"  # denoise_mode (default: 0, no_error_learning: 1, 2nd_error_learning: 2)
    script += f"dev_mode='{str(config['dev_mode']).strip()}'\n"
    # dev_mode (default: 0)
    # 0: off (keep all the intermediate files),
    # 1: on  (cleanup all the intermediate files)

    # loci
    for i in range(len(config['nameOfLoci'])):
        script += f"### loci:{str(config['nameOfLoci'][i]).strip()} ###\n"
        script += f"nameOfLoci+=('{str(config['nameOfLoci'][i]).strip()}')\n"  # nameOfLoci
        script += f"errorRateCutadapt+=('{str(config['errorRateCutadapt'][i]).strip()}')\n"  # errorRateCutadapt
        script += f"minimumLengthCutadapt+=('{str(config['minimumLengthCutadapt'][i]).strip()}')\n"  # minimumLengthCutadapt
        script += f"primerF+=('{str(config['primerF'][i]).strip()}')\n"  # primerF
        script += f"primerFName+=('{str(config['primerFName'][i]).strip()}')\n"  # primerFName
        script += f"primerR+=('{str(config['primerR'][i]).strip()}')\n"  # primerR
        script += f"primerRName+=('{str(config['primerRName'][i]).strip()}')\n"  # primerRName
        #     script += f"amplicon_r1+=('{config['amplicon_r1'][i]}')\n"  # amplicon_r1
        #     script += f"amplicon_r2+=('{config['amplicon_r2'][i]}')\n"  # amplicon_r2
        script += f"barcodesFile1+=('{str(config['barcodesFile1'][i]).strip()}')\n"  # barcodesFile1
        script += f"barcodesFile2+=('{str(config['barcodesFile2'][i]).strip()}')\n"  # barcodesFile2
        script += f"sseqidFileName+=('{str(config['sseqidFileName'][i]).strip()}')\n"  # sseqidFileName
        script += f"minimumLengthCutadaptInLoop+=('{str(config['minimumLengthCutadaptInLoop'][i]).strip()}')\n"  # minimumLengthCutadaptInLoop
        script += f"customizedCoreNumber+=('{str(config['customizedCoreNumber'][i]).strip()}')\n"  # customizedCoreNumber
        script += f"minimumOverlapBasePair+=('{str(config['minimum_overlap_base_pair'][i]).strip()}')\n"  # minimumOverlapBasePair
        script += f"maximumMismatchBasePair+=('{str(config['maximum_mismatch_base_pair'][i]).strip()}')\n"  # maximumMismatch
        # Dev Only
        script += f"blastReadChoosingMode[{i}]='{config['blastReadChoosingMode'][i] if config['blastReadChoosingMode'][i] == '0' else '1'}'\n"
        # blastReadChoosingMode (default: 1): 0: 10Ncat Blast, 1: split R1 R2 Blast
        script += f"blastParsingMode[{i}]='{config['blastParsingMode'][i] if config['blastParsingMode'][i] in ('0', '1', '2', '3') else '2'}'\n"
        # blastParsingMode (default: 2)
        # # blast_parsing_mode == "0":
        # 1.identity: 用3排序，取最高者出來，但不低於85
        # 2.qstart-qend: 用abs(7-8)取最大，但不低於序列長度的一半
        # # blast_parsing_mode == "1":
        # 1.qstart-qend: 用abs(7-8)取最大，但不低於序列長度(qseqid_length)的一半
        # 2.identity: 用3排序，取最高者出來，但不低於85
        # # blast_parsing_mode == "2":
        # 1.qstart-qend & identity 並行，用abs(7-8)*identity取最大，但不低於序列長度的一半，且identity要大於85
        # # blast_parsing_mode == "3":
        # 1. e-value, 越小越好，但不高於0.01，1/10000代表每10000次align才可能出現一次更好的結果

    script += 'echo \'[INFO] config imported!\'\n'

    # Write script to file
    os.makedirs('/PowerBarcoder/data/result/' + str(batch_name))
    with open("/PowerBarcoder/data/result/" + batch_name + "/config.sh", 'w') as f:
        f.write(script)

    print('Config file has been exported as a shell script.')

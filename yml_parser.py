# GUI請先生出yml，再來用這支程式轉成shell script
import os
import yaml
from datetime import datetime


# convert the formData to YAML
def parsingFormDataToYml(data):
    yaml_data = yaml.dump(data)
    with open('main/config.yml', 'w') as f:
        f.write("---\n")
        f.write(yaml_data)


# convert the YAML to shell script, with some fixed field
def parsingYmlToShell(batch_name:str):

    # Load YAML file
    with open('main/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    # Generate shell script (有#的代表使用者可以改)
    # path
    script = '#!/bin/bash\n'
    script += "datetime='" + batch_name + "/'\n"
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
    script += f"ampliconMinimumLength='1'\n"
    script += f"minimunOverlapBasePair='4'\n"

    # loci
    for i in range(len(config['nameOfLoci'])):
        script += f"nameOfLoci+=('{str(config['nameOfLoci'][i]).strip()}')\n"  # nameOfLoci

    for i in range(len(config['errorRateCutadaptor'])):
        script += f"errorRateCutadaptor+=('{str(config['errorRateCutadaptor'][i]).strip()}')\n"  # errorRateCutadaptor

    for i in range(len(config['minimumLengthCutadaptor'])):
        script += f"minimumLengthCutadaptor+=('{str(config['minimumLengthCutadaptor'][i]).strip()}')\n"  # minimumLengthCutadaptor

    for i in range(len(config['primerF'])):
        script += f"primerF+=('{str(config['primerF'][i]).strip()}')\n"  # primerF

    for i in range(len(config['primerFName'])):
        script += f"primerFName+=('{str(config['primerFName'][i]).strip()}')\n"  # primerFName

    for i in range(len(config['primerR'])):
        script += f"primerR+=('{str(config['primerR'][i]).strip()}')\n"  # primerR

    for i in range(len(config['primerRName'])):
        script += f"primerRName+=('{str(config['primerRName'][i]).strip()}')\n"  # primerRName

    # for i in range(len(config['amplicon_r1'])):
    #     script += f"amplicon_r1+=('{config['amplicon_r1'][i]}')\n"  # amplicon_r1
    #
    # for i in range(len(config['amplicon_r2'])):
    #     script += f"amplicon_r2+=('{config['amplicon_r2'][i]}')\n"  # amplicon_r2

    for i in range(len(config['barcodesFile1'])):
        script += f"barcodesFile1+=('{str(config['barcodesFile1'][i]).strip()}')\n"  # barcodesFile1

    for i in range(len(config['barcodesFile2'])):
        script += f"barcodesFile2+=('{str(config['barcodesFile2'][i]).strip()}')\n"  # barcodesFile2

    for i in range(len(config['sseqidFileName'])):
        script += f"sseqidFileName+=('{str(config['sseqidFileName'][i]).strip()}')\n"  # sseqidFileName

    for i in range(len(config['minimumLengthCutadaptorInLoop'])):
        script += f"minimumLengthCutadaptorInLoop+=('{str(config['minimumLengthCutadaptorInLoop'][i]).strip()}')\n"  # minimumLengthCutadaptorInLoop

    for i in range(len(config['customizedCoreNumber'])):
        script += f"customizedCoreNumber+=('{str(config['customizedCoreNumber'][i]).strip()}')\n"  # customizedCoreNumber

    for i in range(len(config['nameOfLoci'])):
        script += f"blastParsingMode+=('2')\n" # blastParsingMode (default: 2)

    script += f"workingDirectory='/PowerBarcoder/main/'\n"

    script += 'echo \'[INFO] config imported!\'\n'


    # Write script to file
    os.makedirs('/PowerBarcoder/data/result/'+str(batch_name))
    with open("/PowerBarcoder/data/result/"+batch_name+"/config.sh", 'w') as f:
        f.write(script)

    print('Config file has been exported as a shell script.')


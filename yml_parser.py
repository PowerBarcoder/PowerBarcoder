# GUI請先生出yml，再來用這支程式轉成shell script
import yaml
from datetime import datetime

# convert the formData to YAML
def parsingFormDataToYml(data):
    yaml_data = yaml.dump(data)
    with open('main/config.yml', 'w') as f:
        f.write("---\n")
        f.write(yaml_data)


# convert the YAML to shell script, with some fixed field
def parsingYmlToShell():
    # Get current datetime
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d%H%M")

    # Load YAML file
    with open('main/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    # Generate shell script (有#的代表使用者可以改)
    # path
    script = '#!/bin/bash\n'
    script += "datetime='"+formatted_datetime+"/'\n"
    script += f"myCutadaptPath='/venv/cutadapt-venv/bin/'\n"
    script += f"myFastpPath='/usr/local/bin/'\n"
    script += f"localBlastToolDir='/usr/local/bin/'\n"
    script += f"ampliconInfo='{config['ampliconInfo']}'\n" # ampliconInfo
    script += f"resultDataPath='/PowerBarcoder/data/result/$datetime'\n"
    script += f"missList='/PowerBarcoder/data/missingList.txt'\n"
    script += f"R1FastqGz='{config['R1FastqGz']}'\n"  # R1FastqGz
    script += f"R2FastqGz='{config['R2FastqGz']}'\n"  # R2FastqGz
    script += f"summaryJsonFileName='summary.json'\n"
    script += f"summaryHtmlFileName='summary.html'\n"
    script += f"dada2LearnErrorFile='{config['dada2LearnErrorFile']}'\n"  # dada2LearnErrorFile
    script += f"dada2BarcodeFile='{config['dada2BarcodeFile']}'\n"  # dada2BarcodeFile

    # loci
    for i in range(len(config['nameOfLoci'])):
        script += f"nameOfLoci+=('{config['nameOfLoci'][i]}')\n"  # nameOfLoci

    for i in range(len(config['errorRateCutadaptor'])):
        script += f"errorRateCutadaptor+=('{config['errorRateCutadaptor'][i]}')\n"  # errorRateCutadaptor

    for i in range(len(config['minimumLengthCutadaptor'])):
        script += f"minimumLengthCutadaptor+=('{config['minimumLengthCutadaptor'][i]}')\n"  # minimumLengthCutadaptor

    for i in range(len(config['primerF'])):
        script += f"primerF+=('{config['primerF'][i]}')\n"  # primerF

    for i in range(len(config['primerR'])):
        script += f"primerR+=('{config['primerR'][i]}')\n"  # primerR

    # for i in range(len(config['amplicon_r1'])):
    #     script += f"amplicon_r1+=('{config['amplicon_r1'][i]}')\n"  # amplicon_r1
    #
    # for i in range(len(config['amplicon_r2'])):
    #     script += f"amplicon_r2+=('{config['amplicon_r2'][i]}')\n"  # amplicon_r2

    for i in range(len(config['barcodesFile1'])):
        script += f"barcodesFile1+=('{config['barcodesFile1'][i]}')\n"  # barcodesFile1

    for i in range(len(config['barcodesFile2'])):
        script += f"barcodesFile2+=('{config['barcodesFile2'][i]}')\n"  # barcodesFile2

    for i in range(len(config['sseqidFileName'])):
        script += f"sseqidFileName+=('{config['sseqidFileName'][i]}')\n"  # sseqidFileName

    for i in range(len(config['minimumLengthCutadaptorInLoop'])):
        script += f"minimumLengthCutadaptorInLoop+=('{config['minimumLengthCutadaptorInLoop'][i]}')\n"  # minimumLengthCutadaptorInLoop

    for i in range(len(config['customizedCoreNumber'])):
        script += f"customizedCoreNumber+=('{config['customizedCoreNumber'][i]}')\n"  # customizedCoreNumber

    # script += f"nameOfLoci=('{','.join(config['nameOfLoci'])}')\n"# nameOfLoci
    # script += f"errorRateCutadaptor=('{','.join(str(x) for x in config['errorRateCutadaptor'])}')\n"# errorRateCutadaptor
    # script += f"minimumLengthCutadaptor=('{','.join(str(x) for x in config['minimumLengthCutadaptor'])}')\n"# minimumLengthCutadaptor
    # script += f"primerF=('{','.join(f'{x}' for x in config['primerF'])}')\n"# primerF
    # script += f"primerR=('{','.join(f'{x}' for x in config['primerR'])}')\n"# primerR
    # script += f"amplicon_r1=('{','.join(f'{x}' for x in config['amplicon_r1'])}')\n"# amplicon_r1
    # script += f"amplicon_r2=('{','.join(f'{x}' for x in config['amplicon_r2'])}')\n"# amplicon_r2
    # script += f"barcodesFile1=('{','.join(f'{x}' for x in config['barcodesFile1'])}')\n"# barcodesFile1
    # script += f"barcodesFile2=('{','.join(f'{x}' for x in config['barcodesFile2'])}')\n"# barcodesFile2
    # script += f"sseqidFileName=('{','.join(f'{x}' for x in config['sseqidFileName'])}')\n"# sseqidFileName
    # script += f"minimumLengthCutadaptorInLoop=('{','.join(str(x) for x in config['minimumLengthCutadaptorInLoop'])}')\n"# minimumLengthCutadaptorInLoop
    # script += f"customizedCoreNumber=('{','.join(str(x) for x in config['customizedCoreNumber'])}')\n"# customizedCoreNumber

    script += f"workingDirectory='/PowerBarcoder/main/'\n"

    script += 'echo \'[INFO] config imported!\'\n'

    # Write script to file
    with open('main/config.sh', 'w') as f:
        f.write(script)

    print('Config file has been exported as a shell script.')

# # Access values in YAML file
# myCutadaptPath = config['myCutadaptPath']
# myFastpPath = config['myFastpPath']
# localBlastToolDir = config['localBlastToolDir']
# ampliconInfo = config['ampliconInfo']
# resultDataPath = config['resultDataPath']
# missList = config['missList']
# R1FastqGz = config['R1FastqGz']
# R2FastqGz = config['R2FastqGz']
# summaryJsonFileName = config['summaryJsonFileName']
# summaryHtmlFileName = config['summaryHtmlFileName']
# dada2LearnErrorFile = config['dada2LearnErrorFile']
# dada2BarcodeFile = config['dada2BarcodeFile']
#
# # Access nested values in YAML file
# nameOfLoci = config['nameOfLoci']
# errorRateCutadaptor = config['errorRateCutadaptor']
# minimumLengthCutadaptor = config['minimumLengthCutadaptor']
# primerF = config['primerF']
# primerR = config['primerR']
# amplicon_r1 = config['amplicon_r1']
# amplicon_r2 = config['amplicon_r2']
# barcodesFile1 = config['barcodesFile1']
# barcodesFile2 = config['barcodesFile2']
# sseqidFileName = config['sseqidFileName']
# minimumLengthCutadaptorInLoop = config['minimumLengthCutadaptorInLoop']
# customizedCoreNumber = config['customizedCoreNumber']
# workingDirectory = config['workingDirectory']


# # Generate shell script
# script = '#!/bin/bash\n\n'
# for key, value in config.items():
#     if isinstance(value, list):
#         for i, v in enumerate(value):
#             script += f'{key}[{i}]="{v}"\n'
#     else:
#         script += f'{key}="{value}"\n'
#
# # Write shell script to file
# with open('main/config_generated.sh', 'w') as f:
#     f.write(script)

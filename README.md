# SRA Explorer in Python

---
## Description
### `sra_explorer.py`
Python script that allows users to explore the NCBI Sequence Read Archive and easily access metadata and FTP download information for project datasets. The output generated is a tab-delimited table that features the following fields: 

| Column Header  | Description |
|----------------|-------------|
| Accession  | NCBI SRA run accession number. Used to identify sequencing data used for a particular sequencing experiment. |
| Title | A descriptive title or label for given sample.  |
| Platform  | Sequencing platform used to generate the data (i.e. Illumina MiSeq, 454, etc.)  |
| Total_Bases  | Total number of nucleotide bases contained within the sample.  |
| Create_Date  | Arbitrary date that may represent the date the sample was uploaded or collected.  |
| FASTQ_File  | Name of generated fastq file (after FTP download). |
| FASTQ_URL  | FTP download link to obtain FASTQ file of sample.  |
| FASTQ_Aspera  | Aspera download link to obtain FASTQ file of sample. |

The script was created to be run on the command line, i.e. *Terminal* on macOS, and *Command Prompt* on Windows. It accepts only two input arguments: (1) a SRA project accession number and (2) an output filename.
> :warning: Please note that order does matter when providing arguments. 

The following code can be used as a reference: `$ python sra_explorer.py GSE30567 sample_metadata.tsv`

---

## Installation
**Mac OS X**: A version of Python3 is already installed.  
**Windows**: You will need to install one of the 3.x versions available at [python.org](http://www.python.org/getit/).

---

## Dependencies
The script requires ***json***, ***re***, ***sys***, ***xmltodict***, and ***urllib3*** in order to be properly executed. While sys and re packages are typically pre-installed, the json, xmltodict, and urllib3 packages are easily installed using `pip`. 

### Set-up Instructions
```
$ python
Python 3.X.X
Type "help", "copyright", "credits" or "license" for more information.
>>> pip install json xmltodict urllib3
```

---

## General usage information

1. Download the [ZIP package](https://github.com/ananata/sra_explorer/archive/main.zip) and unzip it.
2. The script will run by simply typing `python sra_explorer.py` followed by two parameters, e.g. `python sra_explorer.py PRJEB8073 PRJEB8073_metadata_ftp_links.tsv`.
3. If the script or output file is in a different directory from which you are trying to run it, you will need to provide full paths.
4. The script can be opened and modified in any text editor app (e.g. TextEdit, Notepad) or Python IDE. Comments are included in the script for user convenience.

---

## Authors
***Nana Afia Twumasi-Ankrah***, Virginia Commonwealth University 

## License

This project is licensed under the GNU GPLv3 License.
This license restricts the usage of this application for non-open sourced systems. Please contact the authors for questions related to relicensing of this software in non-open sourced systems.

## Acknowledgments

Special thanks to Phil Ewel, whose originial [HTML code](https://github.com/ewels/sra-explorer) inspired this python adaptation. 

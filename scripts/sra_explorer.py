#!/usr/bin/env python
# SRA Explorer
##
# Name: Nana Afia Twumasi-Ankrah
# Date Completed: 12/03/2020
# Code Discription: Generate a modified version of SRA Explorer table
# Requirements: SRA Project ID (i.e. GSE30567, SRP043510, PRJEB8073, or ERP009109) and output file path (i.e. ./my_project_metadata.tsv)
# Python version: 3.7.1
# Usage:
#        - Command Line: python sra_explorer.py <SRA Project ID> <output>
#        - Python IDE (i.e. Thonny) Open sra_explorer.py and click execute or "Run"
#
# Extended Description: When the script is executed a tab-delimited table is generated that contains 8 fields:
#  1.  accession
#  2.  title
#  3.  platform
#  4.  total_bases
#  5.  createdate
#  6.  fastq_file
#  7.  fastq_url
#  8.  fastq_asperaurl
# Code modified from Phil Ewel (writer of SRA Explorer[https://sra-explorer.info/])
#
#
# Example Script Execution:
# $ python sra_explorer.py GSE30567 sample_metadata.tsv
#
##

import json
import xmltodict
import urllib.request
import re
import sys

#---------------
# Set up utility functions
#---------------

# === Open URL link and save JSON formatted text in a dictionary ===
def openURL(link):
    response = urllib.request.urlopen(link)
    data = json.loads(response.read()) # Loads a dictionary object
    return(data)

# === Print tab-delimited table to an output file ===
def printTable(accessionList, expSummary, expCreateDate, fastqLinks, output):
    # Extract information from NCBI
    fastqData = json.loads(expSummary)["document"]["Summary"]
    sampleTitle = fastqData["Title"]
    simpleTitle = re.sub("/[^A-Z0-9]\S+/ig", "_", sampleTitle)
    cleanTitle = "_".join( simpleTitle.split() )
    seqPlatform = fastqData["Platform"]["@instrument_model"]
    sampleStats = "{:.2e}".format(int(fastqData["Statistics"]["@total_bases"]))

    for i in range(len(accessionList)):
        pairedFastq = fastqLinks[i].split(";")
        for path in pairedFastq:
            sampleRow = [accessionList[i], cleanTitle, seqPlatform, sampleStats, list(json.loads(expCreateDate).values())[0],
                         path.split('/')[-1], path, path.replace('ftp.sra.ebi.ac.uk/', 'era-fasp@fasp.sra.ebi.ac.uk:')]
            finalString = "\t".join(sampleRow)
            output.write(finalString + "\n") 

# === Get FASTQ ftp links ===
def getFASTQInfo(sampleList):
    ENAsearchRoot = 'https://www.ebi.ac.uk/ena/portal/api/filereport?result=read_run&fields=fastq_ftp&format=JSON&accession='
    ftpLinks = []
    if len(sampleList) > 1:
        for sample in sampleList:
            ENAsearchURL = ENAsearchRoot+sample
            fastqData = openURL(ENAsearchURL)
            ftpLinks.append(fastqData[0]["fastq_ftp"])
    if len(sampleList) == 1:
            ENAsearchURL = ENAsearchRoot+sampleList[0]
            fastqData = openURL(ENAsearchURL)
            ftpLinks.append(fastqData[0]["fastq_ftp"])
    return(ftpLinks)
    
# === Get all sample accession numbers affiliated with project ID (Helper function) ===
def extractSampleAccession(sampleDict):
    sampleList = []
    sampledata = json.loads(sampleDict)["document"]["Run"]
    if len(sampledata) > 1 and isinstance(sampledata, list):
        for data in sampledata:
            sampleList.append(data["@acc"])
    else:
        sampleList.append(sampledata["@acc"])
    if len(sampleList) > 0:
        return(sampleList)
        
# === Get all sample accession numbers affiliated with project ID === 
def getSamples(web, query, start, output):
    webenv = web
    querykey = query
    retstart = start
    retmax = 500 # Max number NCBI clipboard can handle 
    resultsURL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=sra&retmode=json&query_key="+ \
                 querykey+ \
                 "&WebEnv="+webenv+"&retstart="+str(retstart)+'&retmax='+str(retmax)
    data = openURL(resultsURL)["result"]

    # Parse XML formatted text
    # runReg =
    counter = 0
    for uid in data["uids"]:
        try:
            expXMLraw = '<document>'+data[uid]["expxml"].strip()+'</document>'
            expXMLrun = '<document>'+data[uid]["runs"]+'</document>'
            expXMLdate = '<document>'+data[uid]["createdate"]+'</document>'
        except:
            stop("Error found in XML")
            
        # Parse and extract values    
        expXML = xmltodict.parse(expXMLraw)
        expSmp = xmltodict.parse(expXMLrun)
        expCD = xmltodict.parse(expXMLdate)
        expJSON = json.dumps(expXML)
        expSample = json.dumps(expSmp)
        expDate = json.dumps(expCD)
        samples = extractSampleAccession(expSample) # TODO: Avoid storing any large lists
        counter = counter + len(samples)
        
        # Get FASTQ information
        fqLinks = getFASTQInfo(samples)
        
        # Print formatted table
        printTable(samples, expJSON, expDate, fqLinks, output)
        
    return(counter)

# Get all data associated with NCBI project accession ID ===
def getProjectInfo(project, start, output):
    # Get path to list of samples in project
    searchURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=sra&usehistory=y&retmode=json&term='+project
    
    # Parse querykey and webenv information from dictionary
    projectData = openURL(searchURL)
    webenv = projectData['esearchresult']['webenv']
    querykey = projectData['esearchresult']['querykey']
    
    # Get sample information
    return(getSamples(webenv, querykey, start, output))

#--------
# MAIN Function
#--------
def main():
    # Get required input from user (i.e. GSE30567)
    # project_accession="PRJNA588856"
    project_accession=sys.argv[1]

    # Get path to output file from user (i.e. sample_metadata_ftp_links.tsv)
    # output=open("PRJNA588856_metadata_ftp_links.tsv", "a+")
    output=open(sys.argv[2], "a+")
    output.write("\t".join(["Accession", "Title", "Platform", "Total Bases", "Date Created", "FASTQ", "FASTQ_FTP", "FASTQ_Aspera"]) + "\n")
    
    # Get ftp/fastq information
    # The while loop will process the project dataset in groups of 500 (NCBI only allows 500 samples to be analyzed at a given time)
    # Once each group is processed, the next start position (index of the first sample in the following group) will be determined using the "looper" variable
    position = 500
    looper = 0
    while position == 500:
        position = getProjectInfo(project_accession, looper, output)
        print(position)
        looper = looper + position
        
    # Close file stream
    output.close()
    print("Analyzed: " + str(looper) + " samples")
    
# Initializes Main Method
if __name__ == '__main__':
    main()
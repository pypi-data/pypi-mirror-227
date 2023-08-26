# umierrorcorrect

Pipeline for analyzing barcoded amplicon sequencing data with Unique molecular identifiers (UMI)


Reference
---------

UMIErrorCorrect has been published in Clinical Chemistry.

[Link to the Umierrorcorrect paper](https://doi.org/10.1093/clinchem/hvac136)

Osterlund T., Filges S., Johansson G., Stahlberg A. UMIErrorCorrect and UMIAnalyzer: Software for Consensus Read Generation, Error Correction, and Visualization Using Unique Molecular Identifiers, Clinical Chemistry, 2022;, hvac136

Installation
------------

To run Umierrorcorrect via Docker, see the [Docker documentation](doc/docker.md).

To install the UMI-errorcorrect pipeline from source, open a terminal and type the following:

```
pip install umierrorcorrect
```
    
After installation, try to run the pipeline:

```
run_umierrorcorrect.py -h
```

Dependencies
------------

Umi-errorcorrect runs using Python 3 and requires the following programs/libraries to be installed (if you run through docker all dependencies are already handled):

Python-libraries (should be installed automatically):

    pysam (v 0.8.4 or greater)

External programs:

    bwa (bwa mem command is used)
    Either of gzip or pigz (parallel gzip)

Install the external programs and add them to the path.

Since the umierrorcorrect pipeline is using `bwa` for mapping of reads, a bwa-indexed reference genome is needed. Index the reference genome with the command `bwa index -a bwtsw reference.fa`.

Usage
-----

Example syntax for running the whole pipeline:

    run_umierrorcorrect.py -r1 read1.fastq.gz -r2 read2.fastq.gz -ul umi_length -sl spacer_length -r reference_fasta_file.fasta -o output_directory

The ``run_umierrorcorrect.py`` pipeline performs the following steps:

- Preprocessing of fastq files (remove the UMI and spacer and puts the UMI in the header)
- Mapping of preprocessed fastq reads to the reference genome
- Perform UMI clustering, then error correcion of each UMI cluster
- Create consensus reads (one representative read per UMI cluster written to a BAM file)
- Create a consensus output file (collapsed counts per position)
- Perform variant calling.

It is also to possible to run the pipeline step-by-step.

To see the options for each step, type the following:

```
preprocess.py -h
run_mapping.py -h
umi_error_correct.py -h
get_consensus_statistics.py -h
call_variants.py -h
filter_bam.py -h
filter_cons.py -h
```
Tutorial
--------

[Link to the Umierrorcorrect tutorial](https://github.com/stahlberggroup/umierrorcorrect/wiki/Tutorial)


Example of UMI definition options
----------------------------------

[UMI definition options](https://github.com/stahlberggroup/umierrorcorrect/wiki/UMI-definition-options)

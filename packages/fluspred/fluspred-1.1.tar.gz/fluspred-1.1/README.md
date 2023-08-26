# FluSPred: Predicting Zoonotic Host Tropism of Influenza A Virus.

## Introduction

FluSPred (Flu Spread Prediction) is a machine learning-based tool designed to predict the zoonotic host tropism of the Influenza A virus using its protein and genome sequences. It determines whether a viral strain has the potential to infect human hosts, aiding the prioritisation of high-risk viral strains for further research. The tool contributes to the study of the emergence and risk posed by novel influenza viruses if they acquire the capability to spread from human to human.

## Web Server

To facilitate user-friendly access, we provide a web server where users can directly submit their sequences and download predictions in CSV format. Experience the convenience of our web server at [FluSPred Web Server](https://webs.iiitd.edu.in/raghava/fluspred).

## Reference

Roy et al. (2022) developed an in-silico method for predicting infectious strains of the influenza A virus from its genome and protein sequences. Read the publication [here](https://pubmed.ncbi.nlm.nih.gov/36318663/).

### Installation

To install the FluSPred package, use the following command:

```bash
pip install fluspred
```

Usage

To explore the available options for the command-line tool, use:

```bash
fluspred -h
```

For full usage details:

```bash
usage: fluspred [-h] 
                       [-i INPUT 
                       [-0 OPTION]
                       [-p PROTEIN]

Please provide the following arguments to proceed.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input File Name: protein or genome sequence in FASTA format
  -o OPTION, --option OPTION
                        Select the type of file you are providing: Protein (P) or Genome (G)
                        
                        P: Protein
                        G: Genome 
                        
  -p PROTEIN, --protein PROTEIN
                        This argument is required only when choosing the type as protein.
                        Enter the protein name from the list below:
                        
                        HA: Haemagglutinin 
                        PA: Polymerase Acidic
                        PB1: Polymerase Basic 1
                        PB2: Polymerase Basic 2
                        NP: Nucleoprotein
                        NA: Neuraminidase
                        M1: Matrix Protein 1
                        M2: Matrix Protein 2
                        NS1: Non-Structural 1
                        NS2: Non-Structural 2
                        PB1F2: PB1F2
                        PB1N40: PB1-N40
                        PAN155: PA-N155
                        PAN182: PA-N182
                        PAX: PAX

```


Please note that this program requires at least two arguments (three in the case of protein) to run. The first argument is the input file in FASTA format that you want to predict. The second argument specifies the type of sequences in the input file: either Genome (G) or Protein (P). If you choose Protein, you need to provide an additional argument for the protein name from the list above.

To run the program for a genome file, use the following command:



```bash
fluspred -i genomeSample.fasta -o G
```

For a protein file, run the following command:


```bash
fluspred -i ProteinSample.fasta -o P -p pax
```

An Output.csv file will be generated with your results.


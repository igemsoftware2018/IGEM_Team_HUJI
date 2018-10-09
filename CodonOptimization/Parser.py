from Bio import SeqIO
from Bio.SeqIO import FastaIO
from Bio.Alphabet import generic_protein
import numpy as np
import sys

#this is a program that parses the user input
def parse_multiple_fasta_file(input_file_name):
    """
    parses multiple fasta files within the same file
    :param input_file_name: file name
    :return: array containing name, seq tuple
    """
    fasta_sequences = SeqIO.parse(open(input_file_name), 'fasta')
    fastas=[]
    for fasta in fasta_sequences:
        name, sequence = fasta.id, fasta.seq.tostring()
        fastas.append([name, sequence])
    return fastas[0]

def parse_fasta_file(input_file_name):
    """
    parses a single fasta file using biopython
    :param input_file_name: file name
    :return:
    """

    sys.stdout.write("\nthe line is : \n")
    sys.stdout.write(str(input_file_name.readline()))
    l= len(str(input_file_name.readline()))
    sys.stdout.write("len is :"+str(l))
    sys.stdout.write("\n")
    if l >0 :
        sys.stdout.write( "readline[0] is : "+ str(input_file_name.readline()[0]))
    sys.stdout.write("\n")
    input_file_name.seek(0)
    sys.stdout.write("\nfile content is : \n")
    sys.stdout.write(str(input_file_name.read()))
    input_file_name.seek(0)
    return SeqIO.read(input_file_name, "fasta", generic_protein)

def parse_into_trios(sequence):
    """
    parses a sequence into trios , codons
    :param sequence: the input string dna or rna
    :return:
    """
    trios=[]
    for i in range(0, len(sequence), 3):
        trios.append(sequence[i:i + 3])
    return trios

def parse_codon_usage_table(file_name):
    """
    reads a .csv file containing a specified pattern.
    :param file_name: a three column file containing aa (single letter), then codon and then usage.
    :return:
    """
    import pandas
    pdf =pandas.read_csv(file_name, header =0  )
    codon_to_protein_dict = {}
    codon_usage_dict = {}
    AA_list = []
    amino_acid, codon_name, usage_name = pdf.columns.values
    list_of_dictionaries = pdf.to_dict(   orient="records" )
    for i in range(len(list_of_dictionaries)):
        cur_dict = list_of_dictionaries[i]
        aa = cur_dict[amino_acid]
        codon = cur_dict[codon_name]
        frequancy = cur_dict[usage_name]
        if aa not in AA_list:
            AA_list.append(aa)
        codon_usage_dict[codon] = frequancy
        codon_to_protein_dict[codon] = aa

    return codon_usage_dict, codon_to_protein_dict, AA_list

def delete_parnthases(line):
    """
    repleces the unwanted charachters in a line
    :param line: the string to replace from
    :return: the same line, without ( ) \n
    """
    line = line.replace("(", "")
    line = line.replace(")", "")
    line = line.replace("\n", "")
    return line



def parse_kazusa_codon_usage_table(opened_file):
    """
    parses a standart kazusa table.
    :param file_name: the cazusa .csv file
    :return: codon_usage_dict- a dictionary mapping from codon to it's usage, codon_to_protein_dict-
    a dictionary mapping from codon to protein, AA_list- a list of amino acids
    """
    codon_to_protein_dict = {}
    codon_usage_dict = {}
    AA_list = []
    # opened_file = open(file_name, mode = "r")
    lines = list(opened_file)
    lines =list(filter(('\n').__ne__,lines))
    line_np_arr = np.array(lines).reshape((16, 1))
    f = np.vectorize(delete_parnthases)
    a = f(line_np_arr)
    splitted = np.array([i[0].split() for i in a]).reshape(64,5)
    relevent_data = np.delete(splitted,(3,4),1)
    for codon_line in relevent_data:
        aa = codon_line[1]
        codon = codon_line[0]
        usage = codon_line[2]
        if aa not in AA_list:
            AA_list.append(aa)
        codon_usage_dict[codon] = float(usage)
        codon_to_protein_dict[codon] = aa
    return codon_usage_dict, codon_to_protein_dict, AA_list


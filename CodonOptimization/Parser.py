from Bio import SeqIO
import csv
import pandas
from Bio.Alphabet import generic_protein


def parse_multiple_fasta_file(input_file_name):
    """

    :param input_file_name:
    :return: array containing name, seq tuple
    """
    fasta_sequences = SeqIO.parse(open(input_file_name), 'fasta')
    fastas=[]
    for fasta in fasta_sequences:
        name, sequence = fasta.id, fasta.seq.tostring()
        fastas.append([name, sequence])
    return fastas[0] 

def parse_fasta_file(input_file_name):
    return SeqIO.read(input_file_name, "fasta", generic_protein)

def parse_into_trios(sequence):
    """

    :param sequence:
    :return:
    """
    trios=[]
    for i in range(0, len(sequence), 3):
        trios.append(sequence[i:i + 3])
    return trios

def parse_string_dna(seq):
    pass

def parse_string_protein():
    pass

def parse_codon_usage_table(file_name):

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

# file_name = "D:\LEA\BIOINFORMATICS\Year_3\Igem\data\sequence.fasta"
# name, seq = parse_fasta_file(file_name)[0]
# print(parse_into_trios(seq))

# test codon usage table
# print(parse_codon_usage_table("D:\LEA\BIOINFORMATICS\Year_3\Igem\data\e_coli_316407.csv"))

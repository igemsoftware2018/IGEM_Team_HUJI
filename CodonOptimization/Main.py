import os

from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from Bio.SeqUtils import ProtParam
from Bio.Alphabet import generic_dna
from CodonOptimization import Parser
from CodonOptimization import AminoAcid
from CodonOptimization import Calculator
import sys
from Bio import Restriction, SeqIO, SeqRecord
# import python_codon_tables as pct
import ntpath

from termcolor import colored


def main(protein_fasta_filename, list_codon_usage_filenames,output_destination ):
    #verify input
    verify_input()
    #parse protein
    record= Parser.parse_fasta_file(protein_fasta_filename)
    name, id, sequence =record.name, record.id, record.seq
    creatures = {}
    #parse table
    if len(list_codon_usage_filenames) ==0:
        print(colored("Error: Empty codon table filnames", "red"))
        exit(1)
    for i, file_name in enumerate(list_codon_usage_filenames):
        creature_name = ntpath.basename(file_name).split('.')[0] #TODO watch out
        codon_usage_dict, codon_to_protein_dict, AA_list = Parser.parse_codon_usage_table(str(file_name))
        creatures[creature_name] = codon_usage_dict, codon_to_protein_dict, AA_list
    #creates AA
    Amino_Acids_obj_list =[]
    AA_LIST= creatures[creature_name][2]
    codon_to_protein_dict = creatures[creature_name][1]
    for aa in AA_LIST:
        AA = AminoAcid.AminoAcid(aa,codon_to_protein_dict )
        Amino_Acids_obj_list.append(AA)
    for creature_name, creature_tuple in creatures.items():
        codon_usage_dict, codon_to_protein_dict, AA_list = creature_tuple
        for AA in Amino_Acids_obj_list:
            AA.add_organism_codons(codon_usage_dict, creature_name)


    prot_analisys = ProtParam.ProteinAnalysis(sequence._data)
    aa_count_dict = prot_analisys.count_amino_acids()
    ouput_protein_list = Calculator.compute_and_Switch(Amino_Acids_obj_list, sequence,aa_count_dict)
    final_sequence = "".join(ouput_protein_list)
    if len(final_sequence) != len(sequence) * 3:
        print("final sequance length does not match input sequence length")
        exit(1)

    output_file_name = os.path.join (output_destination ,"Ouput.fasta" )

    record = SeqRecord.SeqRecord(Seq(final_sequence, generic_dna) ,  name = name )
    if record.translate().seq != sequence:
        print("error- resulting DNA does not translate back to protein")
        exit(1)
    print("printing to output file....")
    with open(output_file_name, "w") as output_handle:
        SeqIO.write(record, output_handle, "fasta")
    print("ouput sucsessful")
    return True



def verify_input():
    #what kind of seq? DNA\ PROT
    # how many organizms?
    # DNA string or fasta file ?
    #prints usage ....

    pass


def check_restriction(seq, batch_list, to_print = True):
     Ana = Restriction.Analysis(batch_list, seq, linear=False)
     Ana.full()
     if to_print:
         Ana.print_that()


if __name__ == '__main__':
    if len(sys.argv)<2:
        print(colored("Usage: <FASTA FILE> <CREATURE 1 TABLE> <CREATURE 2 TABLE> ....", "green"))
a = ["D:\LEA\BIOINFORMATICS\Year_3\Igem\data\c_elegans_6239.csv", "D:\LEA\BIOINFORMATICS\Year_3\Igem\data\h_sapiens_9606.csv", r"D:\LEA\BIOINFORMATICS\Year_3\Igem\data\b_subtilis_1423.csv"]
main(r"D:\LEA\BIOINFORMATICS\Year_3\Igem\data\HMR1.fasta",a,"D:\LEA\BIOINFORMATICS\Year_3\Igem\ouput")
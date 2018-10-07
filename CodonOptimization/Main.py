import os
import numpy as np
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from Bio.Seq import Seq
from Bio.SeqUtils import ProtParam
from Bio.Alphabet import generic_dna, generic_rna
from Bio.Restriction import RestrictionBatch, FormattedSeq
# from CodonOptimization import Parser
# from CodonOptimization import AminoAcid
# from CodonOptimization import Calculator
import AminoAcid
import Calculator
import Parser
import sys
from Bio import Restriction, SeqIO, SeqRecord
# import python_codon_tables as pct
import ntpath



def main(protein_fasta_filename, list_codon_usage_filenames,output_destination, restriction_enzymes="" ):
    #verify input
    verify_input()
    #parse protein
    record= Parser.parse_fasta_file(protein_fasta_filename)
    name, id, sequence =record.name, record.id, record.seq
    creatures = {}
    #parse table
    if len(list_codon_usage_filenames) ==0:
        print("Error: Empty codon table filnames")
        exit(1)
    for i, file_name in enumerate(list_codon_usage_filenames):
        creature_name = ntpath.basename(file_name).split('.')[0] #TODO watch out
        codon_usage_dict, codon_to_protein_dict, AA_list = Parser.parse_kazusa_codon_usage_table(str(file_name))
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
    final_sequence = final_sequence.replace("U","T")
    #analyse final sequance
    if len(final_sequence) != len(sequence) * 3:
        print("final sequance length does not match input sequence length")
        exit(1)
    output_file_name = os.path.join (output_destination ,"Ouput.fasta" )
    record = SeqRecord.SeqRecord(Seq(final_sequence, ) ,  name = name )
    if record.translate().seq != sequence:
        print("error- resulting DNA does not translate back to protein")
        exit(1)

    #restriction enzymes
    if restriction_enzymes != "":
       restriction_enzymes_list = restriction_enzymes.replace(",", " ").replace('\n', ' ').replace("\t"," ").split()
       batch = RestrictionBatch(restriction_enzymes_list)
       num_cutting = len(check_restriction(Seq(final_sequence,generic_dna), batch))
       best_num_cutting = np.inf
       best_sequ = final_sequence
       iterations = 100
       no_enzymes_cut = num_cutting == 0
       while iterations> 0 and num_cutting > 0 :
           ouput_protein_list = Calculator.compute_and_Switch(Amino_Acids_obj_list, sequence, aa_count_dict)
           final_sequence = "".join(ouput_protein_list)
           final_sequence = final_sequence.replace("U", "T")
           # analyse final sequance
           if len(final_sequence) != len(sequence) * 3:
               print("final sequance length does not match input sequence length")
               exit(1)
           output_file_name = os.path.join(output_destination, "Ouput.fasta")
           record = SeqRecord.SeqRecord(Seq(final_sequence, generic_dna), name=name)
           if record.translate().seq != sequence:
               print("error- resulting DNA does not translate back to protein")
               exit(1)

           num_cutting = len(check_restriction(Seq(final_sequence, generic_dna), batch))
           if num_cutting == 0:
               check_restriction(Seq(final_sequence, generic_dna), batch, to_print= True)
               print("printing to output file....")
               with open(output_file_name, "w") as output_handle:
                   SeqIO.write(record, output_handle, "fasta")
               print("ouput sucsessful")
               return True
           best_num_cutting = min(best_num_cutting, num_cutting)
           if best_num_cutting == num_cutting:
               best_sequ = final_sequence

           iterations -= 1
       if best_num_cutting > 0 :
           cutting = check_restriction(Seq(best_sequ, generic_dna), batch, to_print=True)
           record = SeqRecord.SeqRecord(Seq(best_sequ, generic_dna), name=name)
           with open(output_file_name, "w") as output_handle:
               SeqIO.write(record, output_handle, "fasta")
           return "The enzymes the cut the sequence are:" + str(cutting)+ "\n Output printed to specified location."



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


def check_restriction(seq, batch_list, to_print = False):
     Ana = Restriction.Analysis(batch_list, seq, linear=False)
     Ana.full()
     cutting =Ana.with_sites()
     if to_print:
         Ana.print_as("map")
         Ana.print_that()
     return cutting


if __name__ == '__main__':
    if len(sys.argv)<5:
        print("Usage: <fasta file name> <Output file destination> <organism 1 codon table filename> <organism 2 codon table filename> ....")
        exit(1)
    fasta_file_name = sys.argv[1]
    output_folder = sys.argv[2]
    list_codon_usage_filenames = sys.argv[3:]
    restriction_enzymes = input("Please enter restriction enzymes, sepereted by comma:")
    main(fasta_file_name, list_codon_usage_filenames, output_folder, restriction_enzymes= restriction_enzymes)


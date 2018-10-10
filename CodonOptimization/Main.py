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


def main(protein_fasta_open_file, list_codon_usage_open_files, output_destination, thresh = 0.05 , restriction_enzymes="", run_from_server = False):
    # parse protein
    record = Parser.parse_fasta_file(protein_fasta_open_file)
    name, id, sequence = record.name, record.id, record.seq
    creatures = {}
    # parse table
    if len(list_codon_usage_open_files) == 0:
        raise Exception("Error: Empty codon table filnames")
    # parses organism files , assuming they are already open

    for fname, open_file in list_codon_usage_open_files:
        creature_name = fname.split('.')[0]
        codon_usage_dict, codon_to_protein_dict, AA_list = Parser.parse_kazusa_codon_usage_table(open_file)
        creatures[creature_name] = codon_usage_dict, codon_to_protein_dict, AA_list

    # creates AA
    Amino_Acids_obj_list = []
    AA_LIST = creatures[creature_name][2]
    codon_to_protein_dict = creatures[creature_name][1]
    for aa in AA_LIST:
        AA = AminoAcid.AminoAcid(aa, codon_to_protein_dict)
        Amino_Acids_obj_list.append(AA)
    for creature_name, creature_tuple in creatures.items():
        codon_usage_dict, codon_to_protein_dict, AA_list = creature_tuple
        for AA in Amino_Acids_obj_list:
            AA.add_organism_codons(codon_usage_dict, creature_name)

    prot_analisys = ProtParam.ProteinAnalysis(sequence._data)
    aa_count_dict = prot_analisys.count_amino_acids()

    # replaces aa with codons from codon pool
    ouput_protein_list = Calculator.compute_and_Switch(Amino_Acids_obj_list, sequence, aa_count_dict, thresh)
    final_sequence = "".join(ouput_protein_list)
    final_sequence = final_sequence.replace("U", "T")
    # analyse final sequance
    if len(final_sequence) != len(sequence) * 3:
        raise Exception("final sequance length does not match input sequence length")
    # output_file_name = os.path.join(output_destination, "Ouput.fasta")
    record = SeqRecord.SeqRecord(Seq(final_sequence, ), name=name)
    if record.translate().seq != sequence:
        raise Exception("error- resulting DNA does not translate back to protein")

    # restriction enzymes- verifies they do not cut the sequence. if they do, pick the least cut sequence
    if restriction_enzymes != "":
        restriction_enzymes_list = restriction_enzymes.replace(",", " ").replace('\n', ' ').replace("\t", " ").split()
        batch = RestrictionBatch(restriction_enzymes_list)
        num_cutting = len(check_restriction(Seq(final_sequence, generic_dna), batch))
        best_num_cutting = np.inf
        best_sequ = final_sequence
        iterations = 100
        no_enzymes_cut = num_cutting == 0
        # if the original sequence had a restriction site, repeat the sequence building 100 times , or until
        # a non- cut sequence is found
        while iterations > 0 and num_cutting > 0:
            ouput_protein_list = Calculator.compute_and_Switch(Amino_Acids_obj_list, sequence, aa_count_dict, thresh)
            final_sequence = "".join(ouput_protein_list)
            final_sequence = final_sequence.replace("U", "T")
            # analyse final sequance
            if len(final_sequence) != len(sequence) * 3:
                raise Exception("final sequance length does not match input sequence length")
            # output_file_name = os.path.join(output_destination, "Ouput.fasta")
            record = SeqRecord.SeqRecord(Seq(final_sequence, generic_dna), name=name)
            if record.translate().seq != sequence:
                raise Exception("error- resulting DNA does not translate back to protein")
            # if achieved non cutting sequence, save and return
            num_cutting = len(check_restriction(Seq(final_sequence, generic_dna), batch))
            if num_cutting == 0:
                if run_from_server:
                    return record.format("fasta")
                else:
                    check_restriction(Seq(final_sequence, generic_dna), batch, to_print=True)
                    SeqIO.write(record, output_destination, "fasta")
                    return "Output Sucsessful"
            best_num_cutting = min(best_num_cutting, num_cutting)
            if best_num_cutting == num_cutting:
                best_sequ = final_sequence

            iterations -= 1
        # return best sequence, as in one that is cut by the least amount of restriction enzymes
        if best_num_cutting > 0:
            cutting = check_restriction(Seq(best_sequ, generic_dna), batch, to_print=True)
            record = SeqRecord.SeqRecord(Seq(best_sequ, generic_dna), name=name)
            if run_from_server:
                return record.format("fasta")
            SeqIO.write(record, output_destination, "fasta")
            return "The enzymes the cut the sequence are:" + str(cutting) + "\n Output printed to specified location."

    SeqIO.write(record, output_destination, "fasta")
    if run_from_server:
        return record.format("fasta")
    return "ouput sucsessful"


def check_restriction(seq, batch_list, to_print=False):
    """
     checks, using biopython, if the restriction enzymes specified cut the given sequence.
     :param seq: the given dna sequence
     :param batch_list: the RestrictionBatch object containing the restriction enzymes
     :param to_print: True or false, to print to the screen the analysis results
     :return: a dictionary containing what enzymes cut the sequence and where
     """
    Ana = Restriction.Analysis(batch_list, seq, linear=False)
    Ana.full()
    cutting = Ana.with_sites()
    if to_print:
        Ana.print_as("map")
        Ana.print_that()
    return cutting


if __name__ == '__main__':
    # the code that runs the program from command line or directly.
    if len(sys.argv) < 5:
        raise Exception(
            "Usage: opened fasta file , opened <Output file destination>, opened organism 1 codon table opened organism 2 codon table ....")
    # get file names
    fasta_file_name = sys.argv[1]
    output_folder = sys.argv[2]
    list_codon_usage_filenames = sys.argv[3:]
    restriction_enzymes = input("Please enter restriction enzymes, sepereted by comma:")
    # runs main program
    main(fasta_file_name, list_codon_usage_filenames, output_folder, restriction_enzymes=restriction_enzymes)



import numpy as np
import AminoAcid
from collections import Counter

# different represenations of stop codons
STOP_CODONS = ["*", "-", "STOP"]

"""
this code is calculates the avrg codon usage and creates the codon pool.
"""
def compute_and_Switch(All_AAs,protein,aa_count_dict, thresh = 0.05):
    """
    :param All_AAs: list of all the amino acids
    :param protein: the input protein to switch
    :param aa_count_dict:  how many times does each aa appear in protein
    :param thresh: threshold under which not to use codon
    :return:
    """
    #choose which function to use according to user input
    means_dict = {}
    for aa in All_AAs:
        means_dict = compute_mean_dict_for_aa(aa, means_dict, thresh)

    return divide_into_result(means_dict, protein, All_AAs, aa_count_dict)

def compute_mean_dict_for_aa(aa,  means_dict, thresh):
    """
    computed the average codon usage of all the organisms, while making sure the avg stays above given threshold.
    :param aa: amino acid
    :param means_dict: a dictionary mapping each codon to it's average usage among all given orgainsms.
    :param thresh: threshold under which not to use codon
    :return: means_dict
    """
    #maximise the  AVERAGE with min better then threshould
    num_cratures = len(aa.organisms_dict)
    to_delete = []
    for codon in aa.coding_codons:
        usages =[]
        for creature_name, creature_codon_dict in aa.organisms_dict.items():
            if creature_codon_dict[codon] < thresh:
                print("codon "+ codon + " has usage smaller than threshold: " +str(thresh) + " in organism: " + creature_name)
                to_delete.append(codon)
                aa.not_to_use_codons.append(codon)
                break
            usage = creature_codon_dict[codon]
            usages.append(usage)
        mean = np.mean(usages)
        means_dict[codon] = mean
    # these codons should not be used
    for codon_name in to_delete:
        del means_dict[codon_name]
    # notify user
    if len(means_dict) ==0:
        raise Exception("No codon has usage lower than threshold. Try lowering the threshold")
    return means_dict

def divide_into_result(codon_avrg_dict, protein, Amino_Acids_list, aa_count_dict):
    """

    :param codon_avrg_dict: dict containing the codon to avrg usage across organisms
    :param protein: the original protein
    :param Amino_Acids_list: a list of al present amino acids
    :return:
    """
    # divide the length of the protein and distribute over lowest common delimeter
    output_protein_list = []
    list_protein = list(protein)
    codon_percentage_dict = {}
    aa_to_pool_dict = {}
    cnt = aa_count_dict

    for aa in Amino_Acids_list:
        #make sure it's not stop codons
        if aa.one_letter_name in STOP_CODONS:
            continue
        part_of_usage = 0
        for codon in aa.coding_codons:
            if codon in aa.not_to_use_codons:
                continue
            avrg = codon_avrg_dict[codon]
            part_of_usage += avrg

        for codon in aa.coding_codons:
            if codon in aa.not_to_use_codons:
                continue
            avr = codon_avrg_dict[codon]
            codon_percentage_dict[codon] =np.round(avr/ part_of_usage*cnt[aa.one_letter_name])
    for aa in Amino_Acids_list:
        codon_pool = []
        for x in codon_percentage_dict.keys():
            if x in aa.coding_codons:

                codon_pool += codon_percentage_dict[x].astype(np.int) * [x]
        aa_to_pool_dict[aa] = codon_pool
    #check that there is a coorespondance between the pool size and amino acids used
    for aa in Amino_Acids_list:
        if aa.one_letter_name not in STOP_CODONS:
            name = aa.one_letter_name
            checking_pool = aa_to_pool_dict[aa]
            reminder = cnt[name] - len(checking_pool)
            if ( reminder > 0):
                for j in range(reminder):
                    if len(checking_pool)> 0:
                        need_to_append_choise = np.random.choice(checking_pool)
                        checking_pool.append(need_to_append_choise)
    raise Exception(str(aa_to_pool_dicta))

    #insert codons in the aa slots
    for i, letter in enumerate(list_protein):
        for aa in Amino_Acids_list:
            if aa.one_letter_name != letter or aa.one_letter_name in STOP_CODONS:
                continue
            pool = aa_to_pool_dict[aa]
            if len(pool) <= 0 :
                continue
            choise = np.random.choice(pool)
            pool.remove(choise)
            output_protein_list.append(choise)
            break
    return output_protein_list


def translate_dna_to_protein(inputfile):
    """
    translates dna to protein
    :param inputfile: the filename to replace it's content
    :return:
    """
    f = open(inputfile, "r")
    seq = f.read()

    seq = seq.replace("\n", "")
    seq = seq.replace("\r", "")

    table = {
        'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
        'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
        'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
        'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
        'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
        'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
        'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
        'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
        'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
        'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
        'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
        'TAC': 'Y', 'TAT': 'Y', 'TAA': '*', 'TAG': '*',
        'TGC': 'C', 'TGT': 'C', 'TGA': '*', 'TGG': 'W',
    }
    protein = ""
    if len(seq) % 3 == 0:
        for i in range(0, len(seq), 3):
            codon = seq[i:i + 3]
            protein += table[codon]
    return protein


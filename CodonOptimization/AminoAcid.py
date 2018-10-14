from Bio.Alphabet import IUPAC

rna_codon_to_protein_dict = {
    "UUU":"F", "UUC":"F", "UUA":"L", "UUG":"L",
       "UCU":"S", "UCC":"S", "UCA":"S", "UCG":"S",
       "UAU":"Y", "UAC":"Y", "UAA":"STOP", "UAG":"STOP",
       "UGU":"C", "UGC":"C", "UGA":"STOP", "UGG":"W",
       "CUU":"L", "CUC":"L", "CUA":"L", "CUG":"L",
       "CCU":"P", "CCC":"P", "CCA":"P", "CCG":"P",
       "CAU":"H", "CAC":"H", "CAA":"Q", "CAG":"Q",
       "CGU":"R", "CGC":"R", "CGA":"R", "CGG":"R",
       "AUU":"I", "AUC":"I", "AUA":"I", "AUG":"M",
       "ACU":"T", "ACC":"T", "ACA":"T", "ACG":"T",
       "AAU":"N", "AAC":"N", "AAA":"K", "AAG":"K",
       "AGU":"S", "AGC":"S", "AGA":"R", "AGG":"R",
       "GUU":"V", "GUC":"V", "GUA":"V", "GUG":"V",
       "GCU":"A", "GCC":"A", "GCA":"A", "GCG":"A",
       "GAU":"D", "GAC":"D", "GAA":"E", "GAG":"E",
       "GGU":"G", "GGC":"G", "GGA":"G", "GGG":"G",}

dna_codon_to_protein_dict = {
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
    'TAC': 'Y', 'TAT': 'Y', 'TAA': 'STOP', 'TAG': 'STOP',
    'TGC': 'C', 'TGT': 'C', 'TGA': 'STOP', 'TGG': 'W',
}

# AA_to_codon_dict = dict((y,x) for x,y in dna_codon_to_protein_dict.items())

class AminoAcid:
    """
    a class representing amino acids
    """
    def __init__(self, one_letter_name, codon_to_aa_dict):
        """
        initiates the aa.
        :param one_letter_name: one letterd aa name
        :param codon_to_aa_dict: dictionary mapping from aa to codon
        """
        # self.long_name = protein_name
        if len(one_letter_name) != 1:
            print("Error: multi-lettered protein name ")
            exit(1)
        if not one_letter_name.isupper() and not one_letter_name== "*":
            print("Error: non upper-case protein name ")
            exit(1)
        self.one_letter_name = one_letter_name
        if not (one_letter_name == "STOP" or one_letter_name == "*"):
            try:

                self.three_letter_name =  IUPAC.IUPACData.protein_letters_1to3[one_letter_name]
            except:
                print("Error: no such proetin name : "+ one_letter_name )
                exit(1)
        self.coding_codons = []
        self.find_relevant_codons_in_dict(codon_to_aa_dict)
        self.organisms_dict = {}
        self.not_to_use_codons = []
        pass

    def add_organism_codons(self, codon_frequency_dict, organizm_name):
        """
        adds another organizm to the aa
        :param codon_frequency_dict: the frequency of usage dict for each codon
        :param organizm_name: the name of the beast
        :return:
        """
        filtered_dict = {k: v for (k, v) in codon_frequency_dict.items() if  k in self.coding_codons}
        self.organisms_dict[organizm_name] = filtered_dict


    def find_relevant_codons_in_dict(self, array):
        """

        :param array:
        :return:
        """

        array =[(k,v) for k,v in array.items()]
        for key, val in array:
            if val == self.one_letter_name :
                self.coding_codons.append(key)


# DNA Toolkit
# Last updated: 8/15/23
#
# This package contains DNA/RNA sequencing tools. 
#
# Classes included in this file:
#   - sequenceBuilder
#   - geneticLib
#
# https://www.stephendoescomp.bio
# Stephen Cheney © 2023

import collections
from geneticConst import *
from sequenceBuilder import *


def validateSeq(dna_seq):
    """
    Return True if input sequence is a valid DNA sequence, return False otherwise
    \nNotes: Input is converted to all upper case; 
    \n\tSpaces and tabs between nucleotides do not count towards incorrect sequence;
    \n\tEmpty sequences and sequences without any nucleotide bases are invalid;
    \n<- dna_seq: str
    \n-> bool
    """
    if type(dna_seq) != str:
        return False
    if dna_seq == '':
        return False
    output = False
    tempSeq = dna_seq.upper()
    for chr in tempSeq:
        if chr in nucleotides:
            output = True
        if chr not in nucleotides:
            if (not chr == ' ') and (not chr == '\t'):
                return False
    return output


def cleanSeq(dna_seq):
    """
    Return a clean sequence of nucleotide bases without whitespaces
    \nNotes: Input/Output is converted to all upper case;
    \n\tReturns None if no valid bases in input string;         
    \n<- dna_seq: str
    \n-> str
    """
    if dna_seq == '':
        return None
    output = ''
    isEmpty = True
    tempSeq = dna_seq.upper()
    for chr in tempSeq:
        if chr in nucleotides:
            output += chr
            isEmpty = False
    if isEmpty:
        return None
    else:
        return output


def printSeq(dna_seq, direc):
    """
    Return an annotated DNA sequence in given direction
    \nNotes: direc - 'f' for (5' -> 3'), 'r' for (3' -> 5')
    \n<- dna_seq: str, direc: chr
    \n-> str
    """
    if direc == 'f':
        return '5\' ' + dna_seq + ' 3\''
    if direc == 'r':
        return '3\' ' + dna_seq + ' 5\''
    

def nucFrequencyDict(dna_seq):
    """
    Return a frequency dict of nucleotide bases in a given sequence
    \n<- dna_seq: str
    \n-> dict
    """
    dna_dict = dict(collections.Counter(dna_seq))
    dna_dict.setdefault('A', 0)
    dna_dict.setdefault('T', 0)
    dna_dict.setdefault('G', 0)
    dna_dict.setdefault('C', 0)
    return dna_dict

def percentGC(dna_seq):
    """
    Return GC percentage of a DNA sequence in % form
    \n<- dna_seq: str
    \n-> float
    """
    bases = len(dna_seq)
    return float(nucFrequencyDict(dna_seq)['G']/bases * 100) + float(nucFrequencyDict(dna_seq)['C']/bases * 100)


def transcribe(dna_seq):
    """
    Return the RNA transcription of a given DNA sequence
    \n<- dna_seq: str
    \n-> str
    """
    output = dna_seq.replace('T', 'U')
    return output


def dnaCompliment(dna_seq):
    """
    Return the matched sequence of a given DNA sequence
    \n<- dna_seq: str
    \n-> str
    """
    translationTable = str.maketrans('ATCG', 'TAGC')
    return dna_seq.translate(translationTable)


def rnaCompliment(rna_seq):
    """
    Return the matched sequence of a given RNA sequence
    \n<- rna_seq: str
    \n-> str
    """
    translationTable = str.maketrans('AUCG', 'UAGC')
    return rna_seq.translate(translationTable)


def dna_reverseCompliment(dna_seq):
    """
    Return the reverse compliment of a given DNA sequence
    \nNotes: Returns 5' -> 3'
    \n<- dna_seq: str
    \n-> str
    """
    return dnaCompliment(dna_seq)[::-1]


def rna_reverseCompliment(rna_seq):
    """
    Return the reverse compliment of a given RNA sequence
    \nNotes: Returns 5' -> 3'
    \n<- rna_seq: str
    \n-> str
    """
    return rnaCompliment(rna_seq)[::-1]


def rnaCompliment(rna_seq):
    """
    Return the matched sequence of a given RNA sequence
    \n<- rna_seq: str
    \n-> str
    """
    translationTable = str.maketrans('AUCG', 'UAGC')
    return rna_seq.translate(translationTable)


def printBasePairs(dna_seq):
    """
    Return the complimentary base pairs of a given DNA sequence
    \n<- dna_seq: str
    \n-> str
    """
    return printSeq(dna_seq,'f') + '\n   ' + '|'*len(dna_seq) + '\n' + printSeq(dnaCompliment(dna_seq),'r')


def hammingDist(seq1, seq2):
    """
    Returns Hamming Distance of 2 given sequences
    \n<- seq1: str,\n\tseq2: str
    \n-> int
    """
    seq1Len = len(seq1)
    seq2Len = len(seq2)
    
    tempseq1 = seq1
    tempseq2 = seq2

    if seq1Len < seq2Len:
        tempseq1 = seq1 + ('X' * (seq2Len - seq1Len))
    if seq2Len < seq1Len:
        tempseq2 = seq2 + ('X' * (seq1Len - seq2Len))
    
    h_dist = 0
    for i in range(len(tempseq1)):
        if tempseq1[i] != tempseq2[i]:
            h_dist += 1
    return h_dist


def seqCompare(seq1, seq2):    
    """
    Returns a visual comparison of 2 input sequences
    \n<- seq1: str,\n\tseq2: str
    \n-> str
    """
    seqLen = min(len(seq1), len(seq2))
    compStr = ''
    for i in range(seqLen):
        if seq1[i] == seq2[i]:
            compStr += '|'
        else:
            compStr += ' '
    return seq1 + '\n' + compStr + '\n' + seq2


def translate(rna_seq, init_pos = 0):
    """
    Return the list of codons of a given RNA sequence and starting position in sequence
    \n<- rna_seq: str, init_pos: int
    \n-> chr[]
    """
    return [codons[rna_seq[pos:pos + 3]] for pos in range(init_pos, len(rna_seq) - 2, 3)]


def get_reading_frames(rna_seq):
    """
    Given an RNA seq, return a list of translated codon reading frames
    \n<- rna_seq: str 
    \n-> [str[]]
    """
    frames = []
    for i in range(0,3):
        frames.append(translate(rna_seq, i))
    for i in range(0,3):
        frames.append(translate(rna_reverseCompliment(rna_seq), i))
    return frames

def dnaSummary(dna_seq, seq_name = ''):
    """
    Return summary details of a given DNA sequence.
    \n Notes: seq_name [Optional] is a given name of a sequence for ease of use
    \n Format:
    \n\t Nucleotide Frequency
    \n\t GC Content
    \n\t Forward Strand
    \n\t Compliment
    \n\t Reverse Compliment
    \n\t RNA Transcription
    \n<- rna_seq: str, seq_name: str [Optional]
    \n-> None
    """
    summary = ''
    summary += f'==== Sequence: {seq_name} ====\n'
    summary += f'Nucleotide Freq: {nucFrequencyDict(dna_seq)}\n'
    summary += f'GC Content: {percentGC(dna_seq)}\n'
    summary += f'Base Pairs: \n{printBasePairs(dna_seq)}\n'
    summary += f'Reverse Compliment:\n'
    summary += printSeq(dna_reverseCompliment(dna_seq), 'f')
    summary += f'\nTranscribed:\n{printSeq(transcribe(dna_seq),"f")}'

    return summary


def gcContentFromFASTA(fasta_File):
    """
    Given a FASTA file, return a dict of sequence names and their respective GC content
    \n<- fasta_File: FASTA formatted file 
    \n-> dict
    """
    seqDict = seqsFromFASTA(fasta_File)
    seqDictClean = {k:cleanSeq(v) for k,v in seqDict.items()}
    gcDict = {k:percentGC(v) for k,v in seqDictClean.items()}
    return gcDict


def getMaxGCFromFASTA(fasta_File):
    """
    Given a FASTA file, return the sequence with the largest GC content
    \n<- fasta_File: FASTA formatted file 
    \n-> dict
    """    
    gcDict = gcContentFromFASTA(fasta_File)
    maxKey = max(gcDict, key=gcDict.get)
    return {maxKey:gcDict[maxKey]}


def getProteinsFromRF(amino_acid_seq):
    """
    Given an amino acid sequence, return all possible proteins
    \n<- amino_acid_seq: chr[]
    \n-> str[]
    """    
    curr_protein = ""
    proteins = []

    for each in amino_acid_seq:
        if each == "_":
            if bool(curr_protein):
                proteins.append(curr_protein)
                curr_protein = ""
        else:
            if each == "M":
                curr_protein += each
            if bool(curr_protein):
                curr_protein += each

    return proteins

# ====== Function Comment Template ======

    """
    Purpose of Function
    \nNotes: [notes]
    \n\t[more notes]    
    \n<- input: type
    \n-> type
    """
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skew, kurtosis
from .quantum_dna_encoding import is_valid_dna_seq

def analyze_dna_seq(seq):
    """
    Analyzes a DNA sequence and performs various computations and visualizations

    Args:
        seq (str): The DNA sequence to analyze.

    Returns:
        tuple: A tuple containing the following analysis results:
            - base_counts (dict): A dictionary containing the count of each nucleotide in the sequence.
            - expectation_values (dict): A dictionary containing the probability of each nucleotide in the sequence.
            - variance (float): The variance of the nucleotide counts.
            - std_deviation (float): The standard deviation of the nucleotide counts.
            - covariance (ndarray): The covariance matrix of the nucleotide counts.
            - correlation (ndarray): The correlation matrix of the nucleotide counts.
            - data_skewness (float): The skewness of the nucleotide counts.
            - data_kurtosis (float): The kurtosis of the nucleotide counts.
    """
    seq = seq.upper()  # Convert the sequence to uppercase

    base_counts = {'A': 0, 'T': 0, 'G': 0, 'C': 0}
    # Check if the sequence is a valid DNA sequence
    #it can be loaded from quantum_dna_encoding
    '''def is_valid_dna_seq(seq):
        valid_letters = {'A', 'T', 'C', 'G', 'a', 't', 'c', 'g'}  # Include both lowercase and uppercase letters
        if any(letter not in valid_letters for letter in seq):
            return False
        return True'''    
    if not is_valid_dna_seq(seq):
        print("Error: This is not a DNA sequence. Please provide a valid DNA sequence.")
        return None
    # Count the occurrences of each nucleotide    
    for base in seq:
        if base in base_counts:
            base_counts[base] += 1
    # Compute probability distribution and visualize base counts            
    labels = base_counts.keys()
    counts = list(base_counts.values())

    # Visualize base counts as a pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=labels, autopct='%1.1f%%')
    plt.title('Base Counts')
    # Save the figure as 'base_counts.png' and 'base_counts.pdf'
    plt.savefig('base_counts.png')
    plt.savefig('base_counts.pdf')
     # Compute total bases and probabilities
    total_bases = sum(counts)
    probabilities = [count / total_bases for count in counts]
    # Visualize base probabilities as a bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(labels, probabilities)
    plt.xlabel('Bases')
    plt.ylabel('Probability')
    plt.title('Base Probability Distribution')
    # Save the figure as 'base_probabilities.png' and 'base_probabilities.pdf'
    plt.savefig('base_probabilities.png')
    plt.savefig('base_probabilities.pdf')
    # Visualize base counts as a line plot
    plt.figure(figsize=(8, 6))
    x = np.arange(len(labels))
    plt.plot(x, counts, marker='o', linestyle='-', linewidth=2)
    plt.xticks(x, labels)
    plt.xlabel('Bases')
    plt.ylabel('Count')
    plt.title('Base Count Distribution')
    # Save the figure as 'base_counts_line.png' and 'base_counts_line.pdf'
    plt.savefig('base_counts_line.png')
    plt.savefig('base_counts_line.pdf')
    
    # Compute additional statistical measures
    expectation_values = {base: count / total_bases for base, count in base_counts.items()}
    variance = np.var(counts)
    std_deviation = np.std(counts)
    covariance = np.cov(counts)
    correlation = np.corrcoef(counts)
    data_skewness = skew(counts)
    data_kurtosis = kurtosis(counts)

    return base_counts, expectation_values, variance, std_deviation, covariance, correlation, data_skewness, data_kurtosis 

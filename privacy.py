import pandas as pd
from collections import Counter
import random

def calculate_probability_distribution(dataset):
    """
    Calculates the probability distribution for a given dataset.
    
    Args:
    dataset (list): The input dataset containing raw numbers.
    
    Returns:
    dict: A dictionary representing the probability distribution of the input dataset.
         The keys are unique numbers from the dataset, and the values are the probabilities.
    """
    total_items = len(dataset)
    counter = Counter(dataset)
    probability_distribution = {number: count / total_items for number, count in counter.items()}
    return probability_distribution

def create_sampling_distribution(dataset, sample_no):
    """
    Creates a sampling distribution based on the input dataset.
    
    Args:
    dataset (list): The input dataset containing raw numbers.
    
    Returns:
    list: A list containing items sampled from the input dataset based on their probabilities.
    """
    probability_distribution = calculate_probability_distribution(dataset)
    sampling_distribution = random.choices(list(probability_distribution.keys()), 
                                          weights=list(probability_distribution.values()), 
                                          k=sample_no)
    return sampling_distribution

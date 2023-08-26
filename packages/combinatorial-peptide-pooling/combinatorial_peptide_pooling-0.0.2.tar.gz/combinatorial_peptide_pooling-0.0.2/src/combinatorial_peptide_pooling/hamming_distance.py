def hamming_distance(s1, s2):
    
    """
    For A-hamiltonian path search.
    Takes two messages (0/1 string) and returns their Hamming distance.
    Used in function(address_rearrangement_A).
    """
    
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))
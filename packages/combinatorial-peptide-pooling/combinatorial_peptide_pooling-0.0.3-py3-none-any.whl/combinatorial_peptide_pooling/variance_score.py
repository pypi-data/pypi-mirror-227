def variance_score(bit_sums, s):
    
    """
    For both versions of Hamiltonian path search.
    Takes an address (or union), measures how it influences the balance in path is being added.
    Returns penalty: difference between variance of balance before and after.
    Is dependent on function(bit_sums).
    Used in function(address_rearrangement_AU), function(address_rearrangement_A)
    """
    
    n = len(bit_sums)
    mean = sum(bit_sums) / n
    variance = sum((xi - mean) ** 2 for xi in bit_sums) / n

    new_bit_sums = bit_sums[:]
    for i, bit in enumerate(s):
        new_bit_sums[i] += int(bit)

    new_mean = sum(new_bit_sums) / n
    new_variance = sum((xi - new_mean) ** 2 for xi in new_bit_sums) / n

    penalty = new_variance - variance
    
    return penalty
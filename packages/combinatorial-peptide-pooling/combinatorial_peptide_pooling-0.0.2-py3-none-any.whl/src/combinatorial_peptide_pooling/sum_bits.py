def sum_bits(arr):
    
    """
    For both versions of hamiltonian path search.
    Takes list of addresses and returns their balance.
    Used in function(address_rearrangement_A), function(address_rearrangement_AU),
    function(hamiltonian_path_A), function(hamiltonian_path_AU).
    """
    
    bit_sums = [0]*len(arr[0])

    for s in arr:
        for i, bit in enumerate(s):
            bit_sums[i] += int(bit)
    return bit_sums
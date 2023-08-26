def address_union(address, union):
    
    """
    For AU-hamiltonian path search.
    Takes union and address, returns possible addresses.
    Used in function(hamiltonian_path_AU).
    """
    
    one_bits = []
    for i in range(len(address)):
        if address[i] == '0' and union[i] == '1':
            zero_bit = i
        elif address[i] == '1' and union[i] == '1':
            one_bits.append(i)
    addresses = []
    string = ['0']*len(address)
    one_combs = list(combinations(one_bits, len(one_bits)-1))
    for one_comb in one_combs:
        new_bit = string.copy()
        new_bit[zero_bit] = '1'
        for one_bit in one_comb:
            new_bit[one_bit] = '1'
        addresses.append(''.join(new_bit))
    return addresses
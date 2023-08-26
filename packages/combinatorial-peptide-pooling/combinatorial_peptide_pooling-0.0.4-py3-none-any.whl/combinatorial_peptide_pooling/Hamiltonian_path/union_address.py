def union_address(address, union):
    
    """
    For AU-hamiltonian path search.
    Takes address and union, returns possible unions.
    Used in function(hamiltonian_path_AU).
    """
    
    one_bits = []
    zero_bits = []
    for i in range(len(address)):
        if address[i] == '1' and union[i] == '1':
            one_bits.append(i)
        elif address[i] == '0' and union[i] == '0':
            zero_bits.append(i)
    unions = []
    string = ['0']*len(union)
    for one_bit in one_bits:
        string[one_bit] = '1'
    for zero_bit in zero_bits:
        new_bit = string.copy()
        new_bit[zero_bit] = '1'
        unions.append(''.join(new_bit))
    return unions
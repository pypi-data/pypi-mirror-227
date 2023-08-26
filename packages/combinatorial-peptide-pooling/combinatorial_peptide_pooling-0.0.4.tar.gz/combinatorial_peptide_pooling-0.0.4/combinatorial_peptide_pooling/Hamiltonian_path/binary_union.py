def binary_union(bin_list):
    
    """
    For A-hamiltonian path search.
    Takes list of addresses, returns list of their unions.
    Is dependent on function(return_address_message).
    Used in function(hamiltonian_path_A).
    """
    
    union_list = []
    for i in range(len(bin_list)-1):
        
        set1 = set(return_address_message(bin_list[i], mode = 'a'))
        set2 = set(return_address_message(bin_list[i+1], mode = 'a'))
        set_union = set1.union(set2)
        union = return_address_message(set_union, mode = 'm'+str(len(bin_list[i])))
        union_list.append(union)
    
    return union_list
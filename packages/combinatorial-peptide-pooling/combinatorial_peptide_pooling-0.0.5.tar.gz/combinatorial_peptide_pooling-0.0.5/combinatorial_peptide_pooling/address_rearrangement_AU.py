def address_rearrangement_AU(n_pools, iters, len_lst):
    
    """
    For AU-hamiltonian path search.
    Takes number of pools, iters, and length of the path.
    Returns balance of the path and list of addresses.
    Is dependent on function(hamiltonian_path_AU) and function(sum_bits).
    """
    
    start_a = ''.join(['1']*iters + ['0']*(n_pools-iters))
    start_u = ''.join(['1']*(iters+1) + ['0']*(n_pools-iters-1))

    arrangement = hamiltonian_path_AU(size=len_lst, point = start_a, t = 'a', unions = [start_u])
    
    addresses = []
    for item in arrangement:
        address = []
        for i in range(len(item)):
            if item[i] == '1':
                address.append(i)
        addresses.append(address)
    #print(sum_bits(arrangement))
    return sum_bits(arrangement), addresses
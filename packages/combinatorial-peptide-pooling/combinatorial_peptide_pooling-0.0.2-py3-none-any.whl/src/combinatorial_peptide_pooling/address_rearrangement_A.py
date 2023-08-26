from itertool import combinations

def address_rearrangement_A(n_pools, iters, len_lst):
    
    """
    For A-hamiltonian path search.
    Takes number of pools, iters, and length of the path.
    Returns balance of the path and list of addresses.
    Is dependent on function(hamiltonian_path_A) and function(sum_bits).
    """
    
    vertices = []
    for combo in combinations(range(n_pools), iters):
        v = ['0']*n_pools
        for i in combo:
            v[i] = '1'
        vertices.append(''.join(v))
        
    G = {v: [] for v in vertices}
    for v1 in vertices:
        for v2 in vertices:
            if hamming_distance(v1, v2) == 2:
                G[v1].append(v2)
            
    arrangement = hamiltonian_path_A(G, len_lst, vertices[0])
    
    addresses = []
    for item in arrangement:
        address = []
        for i in range(len(item)):
            if item[i] == '1':
                address.append(i)
        addresses.append(address)
    #print(sum_bits(arrangement))
    return sum_bits(arrangement), addresses
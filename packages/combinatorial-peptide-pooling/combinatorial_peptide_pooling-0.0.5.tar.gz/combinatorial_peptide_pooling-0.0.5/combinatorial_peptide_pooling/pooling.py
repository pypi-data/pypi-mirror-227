def pooling(lst, addresses, n_pools):
    
    """
    Takes list of peptides, list of addresses, number of pools.
    Returns pools - list of peptides for each pool, and peptide_address - for each peptide its address.
    """
    
    pools = {key: [] for key in range(n_pools)}
    peptide_address = dict()

    for i in range(len(lst)):
        peptide = lst[i]
        peptide_pools = addresses[i]
        peptide_address[peptide] = peptide_pools
        for item in peptide_pools:
            pools[item].append(peptide)
    return pools, peptide_address
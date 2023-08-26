def pools_activation(pools, epitope):
    
    """
    Takes peptide pooling scheme (pools) and epitope.
    Returns which pools will be activated given this epitope.
    Is used in function(run_experiment).
    """
    
    activated_pools = []
    for key in pools.keys():
        for item in pools[key]:
            if epitope in item:
                activated_pools.append(key)
                    
    activated_pools = list(set(activated_pools))              
    return activated_pools
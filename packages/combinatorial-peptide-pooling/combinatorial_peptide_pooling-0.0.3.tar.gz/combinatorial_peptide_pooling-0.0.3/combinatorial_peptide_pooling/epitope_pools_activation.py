def epitope_pools_activation(peptide_address, lst, ep_length):
    
    """
    Takes dictionary of peptide_addresses, list of peptides, epitope length.
    Returns activated pools for each possible epitope from peptides.
    Is used in function(run_experiment).
    """
    
    epitopes = []
    act_profile = dict()
    for item in lst:
        for i in range(len(item)):
            if len(item[i:i+ep_length]) == ep_length and item[i:i+ep_length] not in epitopes:
                epitopes.append(item[i:i+ep_length])
    for ep in epitopes:
        act = []
        for peptide in peptide_address.keys():
            if ep in peptide:
                act = act + list(peptide_address[peptide])
        act = sorted(list(set(act)))
        str_act = str(act)
        if str_act not in act_profile.keys():
            act_profile[str_act] = [ep]
        else:
            act_profile[str_act].append(ep)
    return act_profile
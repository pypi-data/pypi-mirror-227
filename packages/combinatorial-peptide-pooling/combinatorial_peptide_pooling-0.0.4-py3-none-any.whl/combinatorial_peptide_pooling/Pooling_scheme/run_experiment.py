import pandas as pd
from itertools import combinations

def run_experiment(lst, peptide_address, ep_length, pools, iters, n_pools, regime):
    
    """
    Imitates experiment. Has two regimes: with and without dropouts.
    Takes list of peptides and runs experiment for every possible epitope.
    Returns activated pools, predicted peptides based on these activated pools.
    With dropouts imitates dropouts and returns number of possible peptides given each possible dropout combination.
    Is dependent on function(pools_activation), function(peptide_search), function(epitope_pools_activation).
    """
    
    act_profile = epitope_pools_activation(peptide_address, lst, ep_length)
    
    check_results = pd.DataFrame(columns = ['Peptide', 'Address', 'Epitope', 'Act Pools',
                                        '# of pools', '# of epitopes', '# of peptides', 'Remained', '# of lost',
                                           'Right peptide', 'Right epitope'])
    for peptide in lst:
        for i in range(len(peptide)):
            ep = peptide[i:i+ep_length]
            if len(ep) == ep_length:
                act = pools_activation(pools, ep)
                if regime == 'without dropouts':
                    peps, eps = peptide_search(lst=lst, act_profile=act_profile,
                                           act_pools = act,
                                           iters = iters, n_pools = n_pools,
                                           regime = 'without dropouts')
                    right_pep = str(peptide in peps)
                    right_ep = str(ep in eps)
                    row = {'Peptide':peptide, 'Address':str(peptide_address[peptide]), 'Epitope':ep,
                           'Act Pools':str(sorted(list(act))), '# of pools':len(act),
                           '# of epitopes':len(eps), '# of peptides':len(peps), 'Remained':'-', '# of lost':0,
                           'Right peptide':right_pep, 'Right epitope':right_ep}
                    check_results = pd.concat([check_results, pd.DataFrame(row, index = [0])])
                elif regime == 'with dropouts':
                    l = len(act)
                    for i in range(1, l+1):
                        lost = len(act) - i
                        lost_combs = list(combinations(act, i))
                        for lost_comb in lost_combs:
                            peps, eps = peptide_search(lst=lst, act_profile=act_profile,
                                           act_pools = list(lost_comb),
                                           iters = iters, n_pools = n_pools,
                                           regime = 'with dropouts')
                            right_pep = str(peptide in peps)
                            right_ep = str(ep in eps)
                
                            row = {'Peptide':peptide, 'Address':str(peptide_address[peptide]), 'Epitope':ep,
                                   'Act Pools':str(sorted(list(act))), '# of pools':len(act),
                                   '# of epitopes':len(eps), '# of peptides':len(peps),
                                   'Remained':str(list(lost_comb)), '# of lost':lost,
                                   'Right peptide':right_pep, 'Right epitope':right_ep}
                            check_results = pd.concat([check_results, pd.DataFrame(row, index = [0])])
    return check_results
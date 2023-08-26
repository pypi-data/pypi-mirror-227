import random

def hamiltonian_path_A(G, size, pt, path=None):
    
    """
    A-hamiltonian path search.
    Is dependent on function(binary_union), function(variance_score), function(sum_bits).
    Used in function(address_rearrangement_A).
    """
    
    if path is None:
        path = []
    if (pt not in set(path)) and (len(binary_union(path+[pt]))==len(set(binary_union(path+[pt])))):
        path.append(pt)
        if len(path)==size:
            return path
        next_points = G.get(pt, [])
        next_points.sort(key=lambda s: (variance_score(sum_bits(path), s), random.random()))
        for pt_next in next_points:
            res_path = hamiltonian_path_A(G, size, pt_next, path)
            if res_path:
                return res_path
        path.remove(pt)
    return None
import random

def hamiltonian_path_AU(size, point, t, unions, path=None):
    
    """
    AU-hamiltonian path search.
    Is dependent on function(union_address), function(address_union), function(variance_score), function(sum_bits).
    Used in function(address_rearrangement_AU).
    """
    
    if path is None:
        path = []
    if unions is None:
        unions = []
    
    if t == 'a':
        if point not in set(path):
            path.append(point)
            if len(path) == size:
                return path
            next_points = union_address(address=path[-1], union=unions[-1] if unions else None)
            next_points.sort(key=lambda s: (variance_score(sum_bits(unions), s), random.random()))
            for nxt in next_points:
                res_path = hamiltonian_path_AU(size, nxt, 'u', unions, path)
                if res_path:
                    return res_path
            path.remove(point)
        else:
            return None
        
    elif t == 'u':
        if point not in set(unions):
            unions.append(point)
            next_points = address_union(address=path[-1], union=unions[-1])
            next_points.sort(key=lambda s: (variance_score(sum_bits(unions), s), random.random()))
            for nxt in next_points:
                res_path = hamiltonian_path_AU(size, nxt, 'a', unions, path)
                if res_path:
                    return res_path   
            unions.remove(point)
        else:
            return None
    return None
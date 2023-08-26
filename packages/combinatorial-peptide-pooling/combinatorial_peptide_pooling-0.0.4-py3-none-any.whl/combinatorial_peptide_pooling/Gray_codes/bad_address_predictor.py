def bad_address_predictor(all_ns):
    
    """
    Takes list of addresses, searches for three consecutive addresses with the same union, removes the middle one.
    Returns list of addresses.
    """
    
    wb = all_ns.copy()
    
    for i in range(len(wb)-1, 1, -1):
        n1 = wb[i]
        n2 = wb[i-1]
        n3 = wb[i-2]
        if set(n1 + n2) == set(n2 + n3) or set(n1 + n2) == set(n1 + n3):
            wb.remove(n2)
    return wb
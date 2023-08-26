def find_pair_with_overlap(strings, target_overlap):
    
    """
    Takes list of peptides and overlap length.
    Returns peptides with this overlap.
    """
    
    target = []
    for i in range(len(strings) - 1):  
        if string_overlap(strings[i], strings[i+1]) == target_overlap:
            target.append([strings[i], strings[i+1]])
    return target
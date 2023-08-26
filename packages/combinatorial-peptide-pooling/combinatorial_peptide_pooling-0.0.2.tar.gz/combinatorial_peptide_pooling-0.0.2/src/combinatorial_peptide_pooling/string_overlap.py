def string_overlap(str1, str2):
    
    """
    Takes two peptides, returns length of their overlap.
    """
    
    overlap_len = 0
    for i in range(1, min(len(str1), len(str2)) + 1):
        if str1[-i:] == str2[:i]:
            overlap_len = i
    return overlap_len
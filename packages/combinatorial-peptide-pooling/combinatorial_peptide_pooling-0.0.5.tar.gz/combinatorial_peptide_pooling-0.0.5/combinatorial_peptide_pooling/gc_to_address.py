def gc_to_address(s_2, iters, n):
    
    """
    Takes BGC transition sequence and returns BGC with particular number of 1 (iters).
    Returns list of addresses.
    """
    
    codes = [['0']*n]
    for item in s_2:
        n_item = codes[-1].copy()
        if n_item[item-1] == '0':
            n_item[item-1] = '1'
        else:
            n_item[item-1] = '0'
        codes.append(n_item)
    addresses = []
    for item in codes:
        if item.count('1') == iters:
            ad = []
            for i in range(len(item)):
                if item[i] == '1':
                    ad.append(i)
            if ad not in addresses:
                addresses.append(ad)
    return addresses
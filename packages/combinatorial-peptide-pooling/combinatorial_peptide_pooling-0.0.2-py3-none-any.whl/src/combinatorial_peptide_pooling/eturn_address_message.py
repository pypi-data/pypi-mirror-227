def return_address_message(code, mode):
    
    """
    For A-hamiltonian path search.
    Takes an address and returns message (0/1 string).
    Or takes a message and returns an address.
    Used in function(binary_union).
    """
    
    if mode == 'a':
        address = []
        for i in range(len(code)):
            if code[i] == '1':
                address.append(i)
        return address
    if mode[0] == 'm':
        n = int(mode[1:])
        message = ''
        for i in range(n):
            if i in code:
                message = message + '1'
            else:
                message = message + '0'
        return message
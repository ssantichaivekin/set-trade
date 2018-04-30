def get_symbols() :
    '''
    Read the list of SET symbols from file.
    '''
    with open('assets/symbol_list.txt', 'r') as f :
        # read the file as array of lines
        lines = f.readlines()
        # strip the newline \n character
        lines = [ line.strip() for line in lines ]
        return lines

# Driver function :
if __name__ == '__main__' :
    # print all symbols to the console
    print(*get_symbols(), sep='\n')

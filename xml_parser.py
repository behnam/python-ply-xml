
from ply import lex

import xml_rules

def main():
    import sys


    # Test it out
    data = open(sys.argv[1]).read()
    print data

    xml_lexer = lex.lex(module=xml_rules)
    xml_lexer.input(data)

    print '________'
    print xml_lexer.lexstateinfo

    print '________'
    print 'INITIAL', xml_lexer.lexstatere['INITIAL']
    print '________'
    print 'tag', xml_lexer.lexstatere['tag']

    print '________'

    # Tokenize
    while 1:
        tok = xml_lexer.token()
        if not tok: break
        print tok

if __name__ == '__main__':
    main()


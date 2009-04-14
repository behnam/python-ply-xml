#!/usr/bin/env python


from ply import lex, yacc


# ########
# tokens:
#

tokens = [

    # INITIAL
    'CDATA',

    'OPENTAGOPEN',
    'CLOSETAGOPEN',

    # tag
    'TAGATTRNAME',

    'TAGCLOSE',
    'LONETAGCLOSE',

    'ATTRASSIGN',

    # attrvalue1
    'ATTRVALUE1OPEN',
    'ATTRVALUE1STRING',
    'ATTRVALUE1CLOSE',

    # attrvalue2
    'ATTRVALUE2OPEN',
    'ATTRVALUE2STRING',
    'ATTRVALUE2CLOSE',

    # escaped

]


class XmlLexer:
    # The XML Tokenizer

    # ########
    # states:
    #
    #   default:
    #     The default context, non-tag texts
    #   tag:
    #     A document tag
    #   string:
    #     Within quote-delimited strings inside tags
    #   escaped:
    #     A single-use state that treats the next character literally.

    states = (
        ('tag', 'exclusive'),
        ('attrvalue1', 'exclusive'),
        ('attrvalue2', 'exclusive'),
        ('escaped', 'exclusive'),
    )

    def state_push(self, lexer, state):
        lexer.push_state(state)

    def state_pop(self, lexer):
        lexer.pop_state()


    tokens = tokens


    # ########
    # ANY

    def t_ANY_error(self, t):
        # XX
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)


    # ########
    # INITIAL

    t_ignore  = ''

    def t_CDATA(self, t):
        '[a-zA-Z\t]+'

        return t

    def t_CLOSETAGOPEN(self, t):
        r'</'

        self.state_push(t.lexer, 'tag')
        return t

    def t_OPENTAGOPEN(self, t):
        r'<'

        self.state_push(t.lexer, 'tag')
        return t


    # ########
    # tag

    t_tag_ignore  = ' \t'


    def t_tag_TAGCLOSE(self, t):
        r'>'

        self.state_pop(t.lexer)
        return t

    def t_tag_LONETAGCLOSE(self, t):
        r'/>'

        self.state_pop(t.lexer)
        return t


    digit       = r'([0-9])'
    nondigit    = r'([_A-Za-z])'
    identifier  = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'

    def t_tag_TAGATTRNAME(self, t):

        return t

    t_tag_TAGATTRNAME.__doc__ = identifier


    t_tag_ATTRASSIGN    = r'='

    def t_tag_ATTRVALUE1OPEN(self, t):
        r'\''

        self.state_push(t.lexer, 'attrvalue1')
        return t

    def t_tag_ATTRVALUE2OPEN(self, t):
        r'"'

        self.state_push(t.lexer, 'attrvalue2')
        return t


    # ########
    # attrvalue1

    def t_attrvalue1_ATTRVALUE1STRING(self, t):
        r'[^\']+'

        t.value = unicode(t.value)
        return t

    def t_attrvalue1_ATTRVALUE1CLOSE(self, t):
        r'\''

        self.state_pop(t.lexer)
        return t


    # ########
    # attrvalue2

    def t_attrvalue2_ATTRVALUE2STRING(self, t):
        r'[^"]+'

        t.value = unicode(t.value)
        return t

    def t_attrvalue2_ATTRVALUE2CLOSE(self, t):
        r'"'

        self.state_pop(t.lexer)
        return t


    # ########
    # escaped

    t_escaped_ignore  = ''


    # ########
    # MISC

    literals = '$%^'

    def t_ANY_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)


    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)

    # Test it output
    def test(self, data):
        self.lexer.input(data)

        print
        print 'TOKEN LIST:'
        print '--------'

        while 1:
            tok = self.lexer.token()
            if not tok: break
            print '[%12s] %s' % (self.lexer.lexstate, tok)

        print '--------'
        print

    # XmlLexer ends


class Element:
    # Document object model
    #
    # Parser returns the root Element of the XML document

    def __init__ (self, name, attr={}, children=[], string=''):
        self.name = name
        self.attr = attr
        self.children = children
        self.string = string

# Parser

# INITIAL 'CDATA', 'OPENTAGOPEN', 'CLOSETAGOPEN',
# tag 'TAGATTRNAME', 'TAGCLOSE', 'LONETAGCLOSE', 'ATTRASSIGN',
# attrvalue1 'ATTRVALUE1OPEN', 'ATTRVALUE1STRING', 'ATTRVALUE1CLOSE',
# attrvalue2 'ATTRVALUE2OPEN', 'ATTRVALUE2STRING', 'ATTRVALUE2CLOSE',


# ########
# Grammer

def p_root(p):
    'root : opentag'

    print 'p_root:', p
    p[0] = p[1]


def p_opentag(p):
    'opentag : OPENTAGOPEN TAGATTRNAME TAGCLOSE'

    print 'p_opentag:', p
    p[0] = Element(p[2])


# ########
# General

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print "Parse error:", p
    pass


# Disabled

"""
def p_opentag(p):
    'opentag : OPENTAGOPEN TAGATTRNAME attributes TAGCLOSE'

    p[0] = Element(p[2])

def p_attributes(p):
    '
    attributes : attribute attributes
               | attribute
               | empty
    '

    p[0] = p[1]

def p_attribute(p):
    'attribute : TAGATTRNAME ATTRASSIGN attrvalue'

    p[0] = {p[1]: p[3]}

def p_opentag_name_attr(p):
    'opentag_name_attr : OPENTAGOPEN TAGATTRNAME '

    p[0] = p[1]

def p_attr_string(p):
    'attr_string : '
    pass
"""


# Main
def main():
    import sys

    # Read data
    data = open(sys.argv[1]).read()
    print
    print 'INPUT:'
    print '--------'
    print data
    print '--------'

    # Tokenizer
    xml_lexer = XmlLexer()
    xml_lexer.build()

    xml_lexer.test(data)

    # Parser
    yacc.yacc(method="SLR")

    result = yacc.parse(data)
    print
    print 'RESULT:'
    print '--------'
    print 'root:', result
    print '--------'


# Customization

def yacc_production_str(p):
    return "YaccProduction(%s, %s)" % (str(p.slice),str(p.stack))

yacc.YaccProduction.__str__ = yacc_production_str


if __name__ == '__main__':
    main()


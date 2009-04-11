
reserved = {
}


tokens = [

    # Tag & Attr names
    'NAME',

    # Tag
    'OPENTAGOPEN',
    'CLOSETAGOPEN',

    'TAGCLOSE',
    'LONETAGCLOSE',

    # Attr
    'ATTRASSIGN',

    'ATTRVALUE',

    # Strings
    'CDATA',

] + reserved.values()


# RegEx

t_CLOSETAGOPEN  = r'<\/'
t_OPENTAGOPEN   = r'<'
t_LONETAGCLOSE  = r'/>'
t_TAGCLOSE      = r'>'

t_ATTRASSIGN    = r'='

#t_CDATA    = r'.'



# States

states = [
    ('tag', 'exclusive'),
]


def t_begin_tag(t):
    r'<'

    print "TAG starts"

    #t.lexer.begin('tag')
    t.lexer.push_state('tag')


def t_tag_end(t):
    r'>'

    print "TAG ends"

    #t.lexer.begin('INITIAL')
    t.lexer.pop_state()


# Names
digit       = r'([0-9])'
nondigit    = r'([_A-Za-z])'
identifier  = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'

def t_ANY_NAME(t):

    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

t_ANY_NAME.__doc__ = identifier


def t_ANY_ATTRVALUE(t):
    r'[\'"][^\'"]*[\'"]'

    t.value = unicode(t.value)

    return t

def t_tag_ATTRVALUE(t):
    r'[\'"][^\'"]*[\'"]'

    t.value = unicode(t.value)

    return t


'''
def t_NUMBER(t):
    r'\d+'
    try:
         t.value = int(t.value)
    except ValueError:
         print "Line %d: Number %s is too large!" % (t.lineno,t.value)
	 t.value = 0
    return t
'''


# Ignore

t_ANY_ignore  = ' \t'

literals = '$%^'

def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ANY_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


# Important Libraries
import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from nltk.tree import *


# Defining token types
class Token_type(Enum):
    # Arithmetic Operators
    PlusOp = 1
    MinusOp = 2
    MultiplyOp = 3
    DivideOp = 4
    AssignmentOp = 5

    # Relational Operators
    LessThanOp = 6
    GreaterThanOp = 7
    EqualOp = 8
    NotEqualOp = 9
    GreatEqual = 10
    LessEqual = 11

    # Keywords
    ANDWORD = 12
    ARRAY = 13
    Begin = 14
    CASE = 15
    CONST = 16
    DIV = 17
    Do = 18
    DOWNTO = 19
    Else = 20
    End = 21
    FILE = 22
    FOR = 23
    FUNCTION = 24
    GOTO = 25
    If = 26
    IN = 27
    LABEL = 28
    MOD = 29
    NIL = 30
    NOT = 31
    OF = 32
    OR = 33
    PACKED = 34
    PROCEDURE = 35
    PROGRAM = 36
    RECORD = 37
    REPEAT = 38
    SET = 39
    THEN = 40
    TO = 41
    TYPE = 42
    UNTIL = 43
    VAR = 44
    WHILE = 45
    WITH = 46

    # Others
    CONSTANT = 47
    IDENTIFIER = 48
    STRING = 49
    ERROR = 50
    LEFT_PAR = 51
    RIGHT_PAR = 52
    Colon = 53
    Semicolon = 54
    Comma = 55
    ENDDOT = 56

    # Data types
    Integer = 57
    Real = 58
    Boolean = 59
    Char = 60
    String = 61
    Enumerated = 62
    Subrange = 63

    # Functions
    Write = 64
    WriteLine = 65
    Read = 66
    ReadLine = 67
    Uses = 68


# class token to hold string and token type
class token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }


# Symbol mapping using python dictionaries
ReservedWords = {
    "and": Token_type.ANDWORD,
    "array": Token_type.ARRAY,
    "begin": Token_type.Begin,
    "case": Token_type.CASE,
    "const": Token_type.CONST,
    "div": Token_type.DIV,
    "do": Token_type.Do,
    "downto": Token_type.DOWNTO,
    "else": Token_type.Else,
    "end": Token_type.End,
    "end.": Token_type.ENDDOT,
    "file": Token_type.FILE,
    "for": Token_type.FOR,
    "functions": Token_type.FUNCTION,
    "goto": Token_type.GOTO,
    "if": Token_type.If,
    "in": Token_type.IN,
    "label": Token_type.LABEL,
    "mod": Token_type.MOD,
    "nil": Token_type.NIL,
    "not": Token_type.NOT,
    "of": Token_type.OF,
    "or": Token_type.OR,
    "packed": Token_type.PACKED,
    "procedure": Token_type.PROCEDURE,
    "program": Token_type.PROGRAM,
    "record": Token_type.RECORD,
    "repeat": Token_type.REPEAT,
    "set": Token_type.SET,
    "then": Token_type.THEN,
    "to": Token_type.TO,
    "type": Token_type.TYPE,
    "until": Token_type.UNTIL,
    "var": Token_type.VAR,
    "while": Token_type.WHILE,
    "with": Token_type.WITH,
    "write": Token_type.Write,
    "writeln": Token_type.WriteLine,
    "read": Token_type.Read,
    "readln": Token_type.ReadLine,
    "uses": Token_type.Uses
}

Arithmetic_Operators = {
             "+": Token_type.PlusOp,
             "-": Token_type.MinusOp,
             "*": Token_type.MultiplyOp,
             "/": Token_type.DivideOp,
             ":=": Token_type.AssignmentOp,
             }

Symbols = {
             ";": Token_type.Semicolon,
             ",": Token_type.Comma,
             ":": Token_type.Colon
           }

Relational_Operators = {
    "<": Token_type.LessThanOp,
    ">": Token_type.GreaterThanOp,
    "=": Token_type.EqualOp,
    "<>": Token_type.NotEqualOp,
    ">=": Token_type.GreatEqual,
    "<=": Token_type.LessEqual,
}
Parenthesis = {
    "(": Token_type.LEFT_PAR,
    ")": Token_type.RIGHT_PAR
}

Data_Types = {
    "integer": Token_type.Integer,
    "real": Token_type.Real,
    "boolean": Token_type.Boolean,
    "char": Token_type.Char,
    "string": Token_type.String,
    "enumerated": Token_type.Enumerated,
    "subrange": Token_type.Subrange
}
TOKENS = []
errors = []
newDataTypes = []

# TODO write in the first 2 if conditions sub.lowercase()
# Lexical Analysis
# Defining the string checking functions
def checkSub(sub):
    # Reserved Words
    if sub in ReservedWords:
        TOKENS.append(token(sub, ReservedWords[sub]))

    # Data types
    elif sub in Data_Types:
        TOKENS.append(token(sub, Data_Types[sub]))

    # Constants - Numbers
    elif re.match("\d+\.?\d*", sub):
        TOKENS.append(token(sub, Token_type.CONSTANT))

    # Strings
    elif re.match("^\'(\s|\S)*\'$", sub):
        TOKENS.append(token(sub, Token_type.STRING))

    # Identifiers - Variables Nomenclature
    elif re.match("^[a-zA-Z][a-zA-Z0-9]*$", sub):
        TOKENS.append(token(sub, Token_type.IDENTIFIER))

    else:
        TOKENS.append(token(sub, Token_type.ERROR))

    sub = ''


# Defining the temp symbols string checking function
def checkSym(temp):
    # Arithmetic Operators
    if temp in Arithmetic_Operators:
        TOKENS.append(token(temp, Arithmetic_Operators[temp]))
    # Symbols
    elif temp in Symbols:
        TOKENS.append(token(temp, Symbols[temp]))
    # Relational Operators
    elif temp in Relational_Operators:
        TOKENS.append(token(temp, Relational_Operators[temp]))
    else:
        TOKENS.append(token(temp, Token_type.ERROR))


def find_token(text):
    text += ' '
    ''' Operation variables '''
    symbols = ['=', '<', '>', ':', '+', '-', '*', '/', ',', ';']
    sub = ''
    isCom = False  # Boolean to decide whether the upcoming text is a comment section and should be skipped
    isMCom = False  # Boolean to decide whether the upcoming text is a Multi-line comment section and should be skipped
    isMCom_star = False  # Boolean to decide whether the upcoming text is a Multi-line comment section and should be skipped
    endSCom = False  # Boolean to decide whether the SingleComment is finished
    isStr = False  # Boolean to decide whether the upcoming text is a string literal and should be tokenized
    isSym = False  # Boolean to decide whether the upcoming text is a group of symbols

    for i in text:
        ###################### Comments ######################
        if isMCom:
            if i == '*':
                isMCom_star = True
            elif i == '}' and isMCom_star:
                isMCom = False
            else:
                isMCom_star = False
                continue

        elif endSCom:
            if i == '\n':
                TOKENS.append(token("UnRecoginsed", Token_type.ERROR))
                endSCom = False
            elif i == '}':
                endSCom = False
            else:
                continue

        elif isCom:
            if i == '*':
                isMCom = True
                isCom = False
            else:
                endSCom = True
                isCom = False

        elif i == '{':
            isCom = True


        ###################### Strings ######################
        elif isStr:
            sub += i
            if i == '\'':
                isStr = False
                checkSub(sub)
                sub = ''

        elif i == '\'':
            isStr = True
            sub += i


        ###################### Symbols ######################
        elif i in Parenthesis:
            if isSym:
                checkSym(sub)
                isSym = False
            elif not (sub == ''):
                checkSub(sub)
            sub = ''
            TOKENS.append(token(i, Parenthesis[i]))

        elif isSym:
            if i in symbols:
                sub += i
            else:
                checkSym(sub)
                isSym = False
                if i.isalnum():
                    sub = i
                else:
                    sub = ''

        elif i in symbols:
            if not (sub == ''):
                checkSub(sub)
            isSym = True
            sub = i

        elif i.isalnum() or i == '.':
            sub += i


        ###################### Strange Symbols ######################
        else:
            if sub == '':
                continue
            checkSub(sub)
            sub = ''
    if isMCom:
        TOKENS.append(token("UnRecoginsed", Token_type.ERROR))


# Parsing
# Match Function
def Match(a, j):
    output = dict()
    if (j < len(TOKENS)):
        Temp = TOKENS[j].to_dict()
        if (Temp['token_type'] == a):
            j += 1
            output["node"] = [Temp['Lex']]
            output["index"] = j
            return output
        else:
            output["node"] = ["error"]
            output["index"] = j + 1
            errors.append("Syntax error : " + Temp['Lex'])  ######### HN3'AYARHAAA
            return output
    else:
        output["node"] = ["error"]
        output["index"] = j + 1
        return output


## Header
# Header Function
def Header(j):
    Children = []
    out = dict()
    out_pro = Match(Token_type.PROGRAM, j)
    Children.append(out_pro['node'])
    out_id = Match(Token_type.IDENTIFIER, out_pro['index'])
    Children.append(out_id['node'])
    out_semi = Match(Token_type.Semicolon, out_id['index'])
    Children.append(out_semi['node'])

    # Creating a node in the tree
    node = Tree('Header', Children)
    out['node'] = node
    out['index'] = out_semi['index']
    return out


## Libraries
def libraries(j):
    temp = TOKENS[j].to_dict()
    if (temp['token_type'] == Token_type.Uses):
        Children = []
        out = dict()
        out_uses = Match(Token_type.Uses, j)
        Children.append(out_uses['node'])
        out_lib = librarynames(out_uses['index'])
        Children.append(out_lib['node'])
        out_semi = Match(Token_type.Semicolon, out_lib['index'])
        Children.append(out_semi['node'])

        # Create a tree node
        node = Tree('Libraries', Children)
        out['node'] = node
        out['index'] = out_semi['index']
        return out
    else:
        out = {'node': '', 'index': j}
        return out


def librarynames(j):
    Children = []
    out = dict()
    out_id = Match(Token_type.IDENTIFIER, j)
    Children.append(out_id['node'])
    out_ex = extralibnames(out_id['index'])
    if (not (out_ex['node'] == '')):
        Children.append(out_ex['node'])

    # Create a tree node
    node = Tree('Library Names', Children)
    out['node'] = node
    out['index'] = out_ex['index']
    return out


def extralibnames(j):
    temp = TOKENS[j].to_dict()
    if temp['token_type'] == Token_type.Comma:
        Children = []
        out = dict()
        out_comma = Match(Token_type.Comma, j)
        Children.append(out_comma['node'])
        out_id = Match(Token_type.IDENTIFIER, out_comma['index'])
        Children.append(out_id['node'])
        out_ex = extralibnames_d(out_id['index'])
        Children.append(out_ex['node'])

        # Create a tree node
        node = Tree('Extra Library Names', Children)
        out['node'] = node
        out['index'] = out_ex['index']
        return out
    else:
        out = {'node': '', 'index': j}
        return out


def extralibnames_d(j):
    temp = TOKENS[j].to_dict()
    if temp['token_type'] == Token_type.Comma:
        Children = []
        out = dict()
        out_comma = Match(Token_type.Comma, j)
        Children.append(out_comma['node'])
        out_id = Match(Token_type.IDENTIFIER, out_comma['index'])
        Children.append(out_id['node'])
        out_exd = extralibnames_d(out_id['index'])
        if (not (out_exd['node'] == '')):
            Children.append(out_exd['node'])

        # Create a tree node
        node = Tree('Library Name', Children)
        out['node'] = node
        out['index'] = out_id['index']
        return out
    else:
        out = {'node': '', 'index': j}
        return out


## Variables
def variables(j):
    temp = TOKENS[j].to_dict()
    if temp['token_type'] == Token_type.VAR:
        Children = []
        out = dict()
        out_var = Match(Token_type.VAR, j)
        Children.append(out_var['node'])
        out_variable = variable(out_var['index'])
        if (not (out_variable['node'] == '')):
            Children.append(out_variable['node'])

        # Create a tree node
        node = Tree('Variables', Children)
        out['node'] = node
        out['index'] = out_variable['index']
        return out

    else:
        out = {'node': '', 'index': j}
        return out


def variable(j):
    Children = []
    out = dict()
    out_vs = vstatement(j)
    Children.append(out_vs['node'])
    out_vd = variable_d(out_vs['index'])
    if (not (out_vd['node'] == '')):
        Children.append(out_vd['node'])

    # Create a tree node
    node = Tree('Variable', Children)
    out['node'] = node
    out['index'] = out_vd['index']
    return out


def variable_d(j):
    temp = TOKENS[j].to_dict()
    if temp['token_type'] == Token_type.IDENTIFIER:
        Children = []
        out = dict()
        out_vs = vstatement(j)
        Children.append(out_vs['node'])
        out_vd = variable_d(out_vs['index'])
        if (not (out_vd['node'] == '')):
            Children.append(out_vd['node'])

        # Create a tree node
        node = Tree('Variable', Children)
        out['node'] = node
        out['index'] = out_vd['index']
        return out

    else:
        out = {'node': '', 'index': j}
        return out


def vstatement(j):
    Children = []
    out = dict()
    out_vn = vnames(j)
    Children.append(out_vn['node'])
    out_colon = Match(Token_type.Colon, out_vn['index'])
    Children.append(out_colon['node'])
    temp = TOKENS[out_colon['index']].to_dict()
    out_dt = dict()
    if temp['Lex'] in Data_Types or temp['Lex'] in newDataTypes:
        out_dt = Match(temp['token_type'], out_colon["index"])
    else:
        out_dt["node"] = ["error"]
        out_dt["index"] = out_colon['index'] + 1
    Children.append(out_dt["node"])
    out_semi = Match(Token_type.Semicolon, out_dt["index"])
    Children.append(out_semi["node"])

    # Create a tree node
    node = Tree('Variable Name', Children)
    out['node'] = node
    out['index'] = out_semi['index']
    return out


def vnames(j):
    Children = []
    out = dict()
    out_id = Match(Token_type.IDENTIFIER, j)
    Children.append(out_id['node'])
    out_evn = extravnames(out_id['index'])
    if (not (out_evn['node'] == '')):
        Children.append(out_evn['node'])

    # Create a tree node
    node = Tree('Variable Names', Children)
    out['node'] = node
    out['index'] = out_evn['index']
    return out


def extravnames(j):
    temp = TOKENS[j].to_dict()
    if temp['token_type'] == Token_type.Comma:
        Children = []
        out = dict()
        out_comma = Match(Token_type.Comma, j)
        Children.append(out_comma['node'])
        out_id = Match(Token_type.IDENTIFIER, out_comma['index'])
        Children.append(out_id['node'])
        out_ex = extravnames_d(out_id['index'])
        if (not (out_ex['node'] == '')):
            Children.append(out_ex['node'])
        # Create a tree node
        node = Tree('Variable Names', Children)
        out['node'] = node
        out['index'] = out_ex['index']
        return out
    else:
        out = {'node': '', 'index': j}
        return out


def extravnames_d(j):
    temp = TOKENS[j].to_dict()
    if temp['token_type'] == Token_type.Comma:
        Children = []
        out = dict()
        out_comma = Match(Token_type.Comma, j)
        Children.append(out_comma['node'])
        out_id = Match(Token_type.IDENTIFIER, out_comma['index'])
        Children.append(out_id['node'])
        out_ex = extravnames_d(out_id['index'])
        if (not (out_ex['node'] == '')):
            Children.append(out_ex['node'])
        # Create a tree node
        node = Tree('Variable Names', Children)
        out['node'] = node
        out['index'] = out_ex['index']
        return out
    else:
        out = {'node': '', 'index': j}
        return out

# TODO Enum type and subrange
## Types
def TypeBlock(j):
    temp = TOKENS[j].to_dict()
    if temp['token_type'] == Token_type.TYPE:
        Children = []
        out = dict()
        out_type = Match(Token_type.TYPE, j)
        Children.append(out_type['node'])
        out_TypeDec = TypeDec(out_type['index'])
        if (not (out_TypeDec['node'] == '')):
            Children.append(out_TypeDec['node'])

        # Create a tree node
        node = Tree('TypeBlock', Children)
        out['node'] = node
        out['index'] = out_TypeDec['index']
        return out

    else:
        out = {'node': '', 'index': j}
        return out


def TypeDec(j):
    Children = []
    out = dict()
    out_ts = TStatement(j)
    Children.append(out_ts['node'])
    out_tdd = TypeDec_d(out_ts['index'])
    if (not (out_tdd['node'] == '')):
        Children.append(out_tdd['node'])


    # Create a tree node
    node = Tree('TypeDec', Children)
    out['node'] = node
    out['index'] = out_tdd['index']
    return out


def TypeDec_d(j):
    Children = []
    out = dict()
    # if (TOKENS[j-1]==TOKENS[-1]): ##########for not accessing out of index
    #     out = {'node': '', 'index': j-1}
    #     return out
    temp = TOKENS[j].to_dict()
    if temp["token_type"] == Token_type.IDENTIFIER:
        out_ts = TStatement(j)
        Children.append(out_ts['node'])
        out_tdd = TypeDec_d(out_ts['index'])
        if (not (out_tdd['node'] == '')):
            Children.append(out_tdd['node'])

        # Create a tree node
        node = Tree('TypeDec_d', Children)
        out['node'] = node
        out['index'] = out_tdd['index']
        return out

    else:
        out = {'node': '', 'index': j}
        return out


def TStatement(j):
    Children = []
    out = dict()
    out_tn = TNames(j)
    Children.append(out_tn['node'])
    out_equal = Match(Token_type.EqualOp, out_tn['index'])
    Children.append(out_equal['node'])
    temp = TOKENS[out_equal['index']].to_dict()
    out_dt = dict()
    if temp['Lex'] in Data_Types:
        out_dt = Match(temp['token_type'], out_equal['index'])
        if not (out_tn['node'] == ["error"]):
            for i in out_tn['node'].leaves():
                if not (i[0] == ','):
                    newDataTypes.extend(i)
            #print(newDataTypes)
    elif temp['token_type'] == Token_type.LEFT_PAR:
        newDataTypes.append(out_tn['node'][0][0])
        out_lp = Match(Token_type.LEFT_PAR, out_equal['index'])
        Children.append(out_lp['node'])
        out_tn = TNames(out_lp['index'])
        Children.append(out_tn['node'])
        out_dt = Match(Token_type.RIGHT_PAR, out_tn['index'])
        #print(newDataTypes)
    else:
        out_dt['node'] = ["error"]
        out_dt['index'] = out_equal["index"] + 1
    Children.append(out_dt["node"])
    out_semi = Match(Token_type.Semicolon, out_dt["index"])
    Children.append(out_semi["node"])

    # Create a tree node
    node = Tree('TStatement', Children)
    out['node'] = node
    out['index'] = out_semi['index']
    return out


def TNames(j):
    Children = []
    out = dict()
    out_id = Match(Token_type.IDENTIFIER, j)
    #Data_Types[out_id['node']] =
    Children.append(out_id['node'])
    out_etn = ExtraTNames(out_id['index'])
    if (not (out_etn['node'] == '')):
        Children.append(out_etn['node'])
    # Create a tree node
    node = Tree('TNames', Children)
    out['node'] = node
    out['index'] = out_etn['index']
    return out


def ExtraTNames(j):
    temp = TOKENS[j].to_dict()
    if temp['token_type'] == Token_type.Comma:
        Children = []
        out = dict()
        out_comma = Match(Token_type.Comma, j)
        Children.append(out_comma['node'])
        out_id = Match(Token_type.IDENTIFIER, out_comma['index'])
        #Data_Types[out_id['node']] =
        Children.append(out_id['node'])
        out_etnd = ExtraTNames_d(out_id['index'])
        if (not (out_etnd['node'] == '')):
            Children.append(out_etnd['node'])
        # Create a tree node
        node = Tree('Variable Names', Children)
        out['node'] = node
        out['index'] = out_etnd['index']
        return out
    else:
        out = {'node': '', 'index': j}
        return out


def ExtraTNames_d(j):
    temp = TOKENS[j].to_dict()
    if temp['token_type'] == Token_type.Comma:
        Children = []
        out = dict()
        out_comma = Match(Token_type.Comma, j)
        Children.append(out_comma['node'])
        out_id = Match(Token_type.IDENTIFIER, out_comma['index'])
        #Data_Types[out_id['node']] =
        Children.append(out_id['node'])
        out_etnd = ExtraTNames_d(out_id['index'])
        if (not (out_etnd['node'] == '')):
            Children.append(out_etnd['node'])
        # Create a tree node
        node = Tree('Variable Names', Children)
        out['node'] = node
        out['index'] = out_etnd['index']
        return out
    else:
        out = {'node': '', 'index': j}
        return out

def DecBlock(j):
    Children = []
    out = dict()
    temp = TOKENS[j].to_dict()
    if temp['token_type'] == Token_type.VAR:
        out_dic = variables(j)
        Children.append(out_dic['node'])
        out_dic = DecBlock(out_dic['index'])
        if (not (out_dic['node'] == '')):
            Children.append(out_dic['node'])
        node = Tree('Declaration Block:', Children)
        out['node'] = node
        out['index'] = out_dic['index']
        return out
    # elif temp['token_type'] == Token_type.CONST:
    #     ###########################out_const = constants
    #
    elif temp['token_type'] == Token_type.TYPE:
        out_dic = TypeBlock(j)
        Children.append(out_dic['node'])
        out_dic = DecBlock(out_dic['index'])
        if (not (out_dic['node'] == '')):
            Children.append(out_dic['node'])
        node = Tree('Declaration Block:', Children)
        out['node'] = node
        out['index'] = out_dic['index']
        return out
    else:
        out = {'node': '', 'index': j}
        return out

def Block(j):
    Token_types_aux =\
        [Token_type.If, Token_type.Read, Token_type.FOR, Token_type.REPEAT,
         Token_type.IDENTIFIER, Token_type.ReadLine, Token_type.Write, Token_type.WriteLine]
    children = []
    out = dict()
    temp = TOKENS[j].to_dict()
    if temp["token_type"] == Token_type.Begin:
        out_begin = Match(Token_type.Begin, j)
        children.append(out_begin['node'])
        out_stat = Statements(out_begin['index'])
        children.append(out_stat['node'])
        out_end = Match(Token_type.End, out_stat['index'])
        children.append(out_end['node'])
        out_semi = Match(Token_type.Semicolon, out_end['index'])
        children.append(out_semi['node'])
        node = Tree('Block', children)
        out['node'] = node
        out['index'] = out_semi['index']
        return out
    elif temp["token_type"] in Token_types_aux:
        out_stats = Statements(j)
        children.append(out_stats['node'])
        node = Tree('Statement', children)
        out['node'] = node
        out['index'] = out_stats['index']
        return out
    else:
        out = {"node": '', 'index': j}
        return out

def Statements(j):
    pass

def Statement(j):
    pass

def Statements_d(j):
    children = []
    out = dict()
    temp = TOKENS[j].to_dict()
    
    #Replace Statement with correct code
    if temp["token_type"] == "Statement":
        pass
    else:
        out = {"node": '', 'index': j}
        return out

# Start symbol
def Parse():
    j = 0
    Children = []

    # Headers
    Header_dict = Header(j)
    Children.append(Header_dict['node'])

    # Library
    Library_dict = libraries(Header_dict['index'])
    if (not (Library_dict['node'] == '')):
        Children.append(Library_dict['node'])

    # Declaration
    Dec_dic = DecBlock(Library_dict['index'])
    Children.append(Dec_dic['node'])

    #Block
    # Block_dict = Block(Dec_dic['index'])
    # Children.append(Block_dict['node'])
    # Dec_dic = DecBlock(Library_dict['index'])
    # Children.append(Dec_dic['node'])

    #Block
    Block_dict = Block(Dec_dic["index"])
    Children.append(Block_dict['node'])

    Node = Tree('Program', Children)
    return Node


# Presentation
##### GUI
root = tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Scanner Phase')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Source code:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)


def Scan():
    x1 = entry1.get()
    find_token(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in TOKENS])
    # print(df)

    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    # start Parsing
    Node = Parse()

    # to display errorlist
    df1 = pandas.DataFrame(errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()
    Node.draw()


button1 = tk.Button(text='Scan', command=Scan, bg='brown',
                    fg='white', font=('helvetica', 9, 'bold'))

canvas1.create_window(200, 180, window=button1)
root.mainloop()

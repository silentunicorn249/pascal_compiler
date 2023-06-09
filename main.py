# Important Libraries
import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from nltk.tree import *
from PIL import ImageTk, Image
from visual_automata.fa.dfa import VisualDFA



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
    "function": Token_type.FUNCTION,
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
functionnames = []
SemiColonsErrorsFollow = []
current_SemiColon = 0
# TODO write in the first 2 if conditions sub.lowercase()
# Lexical Analysis
# Defining the string checking functions
def checkSub(sub):
    # Reserved Words
    tmp = sub.lower()
    if tmp in ReservedWords:
        TOKENS.append(token(sub, ReservedWords[tmp]))

    # Data types
    elif tmp in Data_Types:
        TOKENS.append(token(sub, Data_Types[tmp]))

    # Constants - Numbers
    elif re.match("\d+\.?\d*", sub):
        TOKENS.append(token(sub, Token_type.CONSTANT))

    # Strings
    elif re.match("^\'(\s|\S)*\'$", sub):
        TOKENS.append(token(sub, Token_type.STRING))

    # Identifiers - Variables Nomenclature
    elif re.match("^[a-zA-Z]([a-zA-Z0-9]|_)*$", sub):
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
            if i == '\n':
                isStr = False
                TOKENS.append(token("UnRecoginsed String", Token_type.ERROR))
                sub = ''
            elif i == '\'':
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

        elif i.isalnum() or i == '.' or i == '_':
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
    global current_SemiColon
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
            errors.append("Syntax error : " + Temp['Lex'] )  ######### HN3'AYARHAAA
            return output
    else:
        output["node"] = ["error"]
        output["index"] = j + 1
        return output


## Header
# Header Function
def Header(j):
    global current_SemiColon
    Children = []
    out = dict()
    out_pro = Match(Token_type.PROGRAM, j)
    Children.append(out_pro['node'])
    out_id = Match(Token_type.IDENTIFIER, out_pro['index'])
    Children.append(out_id['node'])

    temp = SemiColonsErrorsFollow[current_SemiColon]
    current_SemiColon += 1
    print("CurrentSemiColon: ")
    print(temp)
    out_semi = Match(Token_type.Semicolon, temp-1)
    Children.append(out_semi['node'])

    # Creating a node in the tree
    node = Tree('Header', Children)
    out['node'] = node
    out['index'] = out_semi['index']
    return out


## Libraries
def libraries(j):
    global current_SemiColon
    if (TOKENS[j - 1] == TOKENS[-1]):  ##########for not accessing out of index
        out = {'node': '', 'index': j-1}
        return out
    temp = TOKENS[j].to_dict()
    if (temp['token_type'] == Token_type.Uses):
        Children = []
        out = dict()
        out_uses = Match(Token_type.Uses, j)
        Children.append(out_uses['node'])
        out_lib = librarynames(out_uses['index'])
        Children.append(out_lib['node'])
        temp = SemiColonsErrorsFollow[current_SemiColon]
        current_SemiColon += 1
        print("CurrentSemiColon: ")
        print(temp)
        out_semi = Match(Token_type.Semicolon, temp-1)
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
    global current_SemiColon
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
    global current_SemiColon
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
    global current_SemiColon
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
    global current_SemiColon
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
    global current_SemiColon
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
    global current_SemiColon
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
    global current_SemiColon
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
        errors.append("Syntax error : " + temp['Lex'])
    Children.append(out_dt["node"])
    temp = SemiColonsErrorsFollow[current_SemiColon]
    current_SemiColon += 1
    # print("CurrentSemiColon: ")
    # print(temp)
    out_semi = Match(Token_type.Semicolon, temp - 1)
    Children.append(out_semi["node"])

    # Create a tree node
    node = Tree('Variable Name', Children)
    out['node'] = node
    out['index'] = out_semi['index']
    return out


def vnames(j):
    global current_SemiColon
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
    global current_SemiColon
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
    global current_SemiColon
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
    global current_SemiColon
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
    global current_SemiColon
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
    global current_SemiColon
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
    global current_SemiColon
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
        errors.append("Syntax error : " + temp['Lex'])
    Children.append(out_dt["node"])
    temp = SemiColonsErrorsFollow[current_SemiColon]
    current_SemiColon += 1
    print("CurrentSemiColon: ")
    print(temp)
    out_semi = Match(Token_type.Semicolon, temp - 1)
    Children.append(out_semi["node"])

    # Create a tree node
    node = Tree('TStatement', Children)
    out['node'] = node
    out['index'] = out_semi['index']
    return out


def TNames(j):
    global current_SemiColon
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
    global current_SemiColon
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
    global current_SemiColon
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
    global current_SemiColon
    Children = []
    out = dict()
    if (TOKENS[j - 1] == TOKENS[-1]):  ##########for not accessing out of index
        out = {'node': '', 'index': j-1}
        return out
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
    elif temp['token_type'] == Token_type.CONST:
        out_dic = ConstBlock(j)
        Children.append(out_dic['node'])
        out_dic = DecBlock(out_dic['index'])
        if (not (out_dic['node'] == '')):
            Children.append(out_dic['node'])
        node = Tree('Declaration Block:', Children)
        out['node'] = node
        out['index'] = out_dic['index']
        return out


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
    global current_SemiColon
    Token_types_aux =\
        [Token_type.If, Token_type.Read, Token_type.FOR, Token_type.REPEAT,
         Token_type.IDENTIFIER, Token_type.ReadLine, Token_type.Write, Token_type.WriteLine]
    children = []
    out = dict()
    if (TOKENS[j - 1] == TOKENS[-1]):  ##########for not accessing out of index
        out = {'node': '', 'index': j-1}
        return out
    temp = TOKENS[j].to_dict()
    if temp["token_type"] == Token_type.Begin:
        out_begin = Match(Token_type.Begin, j)
        children.append(out_begin['node'])
        out_stat = Statements(out_begin['index'])
        children.append(out_stat['node'])
        out_end = Match(Token_type.End, out_stat['index'])
        children.append(out_end['node'])
        if current_SemiColon >= len(SemiColonsErrorsFollow):
            out = {'node': '', 'index': j - 1}
            return out
        temp1 = SemiColonsErrorsFollow[current_SemiColon]
        current_SemiColon += 1
        print("CurrentSemiColon: ")
        print(temp1)
        out_semi = Match(Token_type.Semicolon, temp1-1)
        children.append(out_semi['node'])
        out_block = Block(out_semi['index'])
        if (not (out_block['node'] == '')):
            children.append(out_block['node'])
        node = Tree('Block', children)
        out['node'] = node
        out['index'] = out_block['index']
        return out
    elif temp["token_type"] in Token_types_aux:
        out_stats = Statements(j)
        children.append(out_stats['node'])
        node = Tree('Block', children)
        out['node'] = node
        out['index'] = out_stats['index']
        return out
    else:
        out = {"node": '', 'index': j}
        return out

def Statements(j):
    global current_SemiColon
    children = []
    out = dict()
    out_stat = Statement(j)
    if (not (out_stat['node'] == '')):
        children.append(out_stat['node'])
    out_stats_d = Statements_d(out_stat['index'])
    if (not (out_stats_d['node'] == '')):
        children.append(out_stats_d['node'])
    node = Tree('Statements', children)
    out['node'] = node
    out['index'] = out_stats_d['index']
    return out

def Statements_d(j):
    global current_SemiColon
    Token_types_aux =\
        [Token_type.If, Token_type.Read, Token_type.FOR, Token_type.REPEAT,
         Token_type.IDENTIFIER, Token_type.ReadLine, Token_type.Write, Token_type.WriteLine,Token_type.Begin]
    children = []
    out = dict()
    temp = TOKENS[j].to_dict()
    if temp["token_type"] in Token_types_aux:
        out_stat = Statement(j)
        children.append(out_stat['node'])
        out_stats_d = Statements_d(out_stat['index'])
        if (not (out_stats_d['node'] == '')):
            children.append(out_stats_d['node'])
        node = Tree('Statements_d', children)
        out['node'] = node
        out['index'] = out_stats_d['index']
        return out
    else:
        out = {"node": '', 'index': j}
        return out

def Statement(j):
    global current_SemiColon
    Children = []
    out = dict()
    temp = TOKENS[j].to_dict()
    print(temp)
    if temp["token_type"] == Token_type.If:
        out_if = ifStatement(j)
        Children.append(out_if['node'])
        # Create a tree node
        node = Tree('If', Children)
        out['node'] = node
        out['index'] = out_if['index']
        return out


    elif temp["token_type"] == Token_type.REPEAT:
        print(temp["token_type"])
        out_repeat = RepeatStatement(j)
        Children.append(out_repeat['node'])
        # Create a tree node
        node = Tree('Repeat Until', Children)
        out['node'] = node
        out['index'] = out_repeat['index']
        return out


    elif temp["token_type"] == Token_type.FOR:
        out_for = forStatement(j)
        Children.append(out_for['node'])
        # Create a tree node
        node = Tree('For', Children)
        out['node'] = node
        out['index'] = out_for['index']
        return out

    elif temp["token_type"] == Token_type.IDENTIFIER:
        out_assign = Assign(j)
        Children.append(out_assign['node'])
        # Create a tree node
        node = Tree('Assign', Children)
        out['node'] = node
        out['index'] = out_assign['index']
        return out

    elif (temp['token_type'] == Token_type.Write):
        out_write = Match(Token_type.Write, j)
        Children.append(out_write['node'])

        out_lpar = Match(Token_type.LEFT_PAR, out_write['index'])
        Children.append(out_lpar['node'])

        out_vs = vs(out_lpar['index'])
        Children.append(out_vs['node'])

        out_rpar = Match(Token_type.RIGHT_PAR, out_vs['index'])
        Children.append(out_rpar['node'])
        if current_SemiColon >= len(SemiColonsErrorsFollow):
            out = {'node': '', 'index': j - 1}
            return out
        temp = SemiColonsErrorsFollow[current_SemiColon]
        current_SemiColon += 1
        print("CurrentSemiColon: ")
        print(temp)
        out_semi = Match(Token_type.Semicolon, temp-1)
        Children.append(out_semi['node'])

        # Create a tree node
        node = Tree('Write', Children)
        out['node'] = node
        out['index'] = out_semi['index']
        return out

    elif (temp['token_type'] == Token_type.WriteLine):
        out_write = Match(Token_type.WriteLine, j)
        Children.append(out_write['node'])

        out_lpar = Match(Token_type.LEFT_PAR, out_write['index'])
        Children.append(out_lpar['node'])

        out_vs = vs(out_lpar['index'])
        Children.append(out_vs['node'])

        out_rpar = Match(Token_type.RIGHT_PAR, out_vs['index'])
        Children.append(out_rpar['node'])
        if current_SemiColon >= len(SemiColonsErrorsFollow):
            out = {'node': '', 'index': j - 1}
            return out
        temp = SemiColonsErrorsFollow[current_SemiColon]
        current_SemiColon += 1
        print("CurrentSemiColon: ")
        print(temp)
        out_semi = Match(Token_type.Semicolon, temp-1)
        Children.append(out_semi['node'])

        # Create a tree node
        node = Tree('WriteLine', Children)
        out['node'] = node
        out['index'] = out_semi['index']
        return out

    elif (temp['token_type'] == Token_type.Read):
        out_read = Match(Token_type.Read, j)
        Children.append(out_read['node'])

        out_lpar = Match(Token_type.LEFT_PAR, out_read['index'])
        Children.append(out_lpar['node'])

        out_id = Match(Token_type.IDENTIFIER, out_lpar['index'])
        Children.append(out_id['node'])

        out_rpar = Match(Token_type.RIGHT_PAR, out_id['index'])
        Children.append(out_rpar['node'])
        if current_SemiColon >= len(SemiColonsErrorsFollow):
            out = {'node': '', 'index': j - 1}
            return out
        temp = SemiColonsErrorsFollow[current_SemiColon]
        current_SemiColon += 1
        print("CurrentSemiColon: ")
        print(temp)
        out_semi = Match(Token_type.Semicolon, temp-1)
        Children.append(out_semi['node'])

        # Create a tree node
        node = Tree('Read', Children)
        out['node'] = node
        out['index'] = out_semi['index']
        return out

    elif (temp['token_type'] == Token_type.ReadLine):
        out_read = Match(Token_type.ReadLine, j)
        Children.append(out_read['node'])

        out_lpar = Match(Token_type.LEFT_PAR, out_read['index'])
        Children.append(out_lpar['node'])

        out_id = Match(Token_type.IDENTIFIER, out_lpar['index'])
        Children.append(out_id['node'])

        out_rpar = Match(Token_type.RIGHT_PAR, out_id['index'])
        Children.append(out_rpar['node'])
        if current_SemiColon >= len(SemiColonsErrorsFollow):
            out = {'node': '', 'index': j - 1}
            return out
        temp = SemiColonsErrorsFollow[current_SemiColon]
        current_SemiColon += 1
        print("CurrentSemiColon: ")
        print(temp)
        out_semi = Match(Token_type.Semicolon, temp-1)
        Children.append(out_semi['node'])

        # Create a tree node
        node = Tree('ReadLine', Children)
        out['node'] = node
        out['index'] = out_semi['index']
        return out

    elif (temp['token_type'] == Token_type.Begin):
        out_block = Block(j)
        Children.append(out_block['node'])

        # Create a tree node
        node = Tree('Block', Children)
        out['node'] = node
        out['index'] = out_block['index']
        return out
    else:
        out = {"node": '', 'index': j}
        return out

def Assign(j):
    global current_SemiColon
    Children = []
    out = dict()
    out_id = Match(Token_type.IDENTIFIER,j)
    Children.append(out_id['node'])
    out_ass = Match(Token_type.AssignmentOp, out_id['index'])
    Children.append(out_ass['node'])
    out_value = Value(out_ass['index'])
    Children.append(out_value['node'])
    if current_SemiColon >= len(SemiColonsErrorsFollow):
        out = {'node': '', 'index': j - 1}
        return out
    temp = SemiColonsErrorsFollow[current_SemiColon]
    temp1 = TOKENS[out_value['index']].to_dict()

    #print("CurrentSemiColon: ")
    #print(temp)
    if(temp1['token_type']==Token_type.UNTIL):
        node = Tree('Assign', Children)
        out['node'] = node
        out['index'] = out_value['index']
        return out
    else:
        current_SemiColon += 1
        out_semi = Match(Token_type.Semicolon, temp-1)
        Children.append(out_semi['node'])

    node = Tree('Assign', Children)
    out['node'] = node
    out['index'] = out_semi['index']
    return out

def forStatement(j):
    global current_SemiColon
    children = []
    out = dict()
    for_key = Match(Token_type.FOR, j)
    children.append(for_key['node'])
    identifier = Match(Token_type.IDENTIFIER, for_key['index'])
    children.append(identifier['node'])
    assi_op = Match(Token_type.AssignmentOp, identifier['index'])
    children.append(assi_op['node'])
    forvar_dic = forVar(assi_op['index'])
    children.append(forvar_dic['node'])
    out_to = Match(Token_type.TO, forvar_dic['index'])
    children.append(out_to['node'])
    forvar_dic = forVar(out_to['index'])
    children.append(forvar_dic['node'])
    do_key = Match(Token_type.Do, forvar_dic['index'])
    children.append(do_key['node'])
    block_dic = Block(do_key['index'])
    children.append(block_dic['node'])

    node = Tree('forStatement:', children)
    out['node'] = node
    out['index'] = block_dic['index']
    return out

def forVar(j):
    global current_SemiColon
    children = []
    out = dict()
    temp = TOKENS[j].to_dict()
    if temp['token_type'] == Token_type.IDENTIFIER:
        identifier = Match(Token_type.IDENTIFIER, j)
        children.append(identifier['node'])
        node = Tree('forVar:', children)
        out['node'] = node
        out['index'] = identifier['index']
        return out
    elif temp["token_type"] == Token_type.CONSTANT:
        identifier = Match(Token_type.CONSTANT, j)
        children.append(identifier['node'])
        node = Tree('forVar:', children)
        out['node'] = node
        out['index'] = identifier['index']
        return out
    else:
        out['node'] = ["error"]
        out['index'] = j
        errors.append("Syntax error : " + temp['Lex'])
        return out

# Start symbol
def vs(j):
    global current_SemiColon
    Children = []
    out = dict()
    out_val = Value(j)
    Children.append(out_val['node'])
    out_vss = vss(out_val['index'])
    if (not (out_vss['node'] == '')):
        Children.append(out_vss['node'])

    # Create a tree node
    node = Tree('vs', Children)
    out['node'] = node
    out['index'] = out_vss['index']
    return out

def vss(j):
    global current_SemiColon
    Children = []
    out = dict()
    temp = TOKENS[j].to_dict()

    if (temp['token_type'] == Token_type.Comma):
        out_comma = Match(Token_type.Comma, j)
        Children.append(out_comma['node'])

        out_val = Value(out_comma['index'])
        Children.append(out_val['node'])

        out_vss = vss_d(out_val['index'])
        if (not (out_vss['node'] == '')):
            Children.append(out_vss['node'])

        # Create a tree node
        node = Tree('vss', Children)
        out['node'] = node
        out['index'] = out_vss['index']
        return out

    else:
        out = {'node': '', 'index': j}
        return out

def vss_d(j):
    global current_SemiColon
    Children = []
    out = dict()
    temp = TOKENS[j].to_dict()

    if (temp['token_type'] == Token_type.Comma):
        out_comma = Match(Token_type.Comma, j)
        Children.append(out_comma['node'])

        out_val = Value(out_comma['index'])
        Children.append(out_val['node'])

        out_vss = vss_d(out_val['index'])
        if (not (out_vss['node'] == '')):
            Children.append(out_vss['node'])

        # Create a tree node
        node = Tree('vss', Children)
        out['node'] = node
        out['index'] = out_vss['index']
        return out

    else:
        out = {'node': '', 'index': j}
        return out

def Value(j):
    global current_SemiColon
    Children = []
    out = dict()
    temp1 = TOKENS[j].to_dict()
    temp2 = TOKENS[j+1].to_dict()
    if temp1['Lex'] in functionnames:
        out_value = Match(Token_type.IDENTIFIER, j)
        Children.append(out_value['node'])
        out_leftpar = Match(Token_type.LEFT_PAR, out_value['index'])
        Children.append(out_leftpar['node'])
        out_vfnames = vfnames(out_leftpar['index'])
        Children.append(out_vfnames['node'])
        out_rightpar = Match(Token_type.RIGHT_PAR, out_vfnames['index'])
        Children.append(out_rightpar['node'])

        node = Tree('FunctionParameters', Children)
        out['node'] = node
        out['index'] = out_rightpar['index']
        return out

    elif temp1['token_type'] == Token_type.IDENTIFIER:
        if temp2['token_type'] == Token_type.PlusOp or temp2['token_type'] == Token_type.MinusOp or temp2[
            'token_type'] == Token_type.MultiplyOp or temp2['token_type'] == Token_type.DivideOp:
            out_value = Experssion(j, "id")
            Children.append(out_value['node'])
            # Create a tree node
            node = Tree('Value', Children)
            out['node'] = node
            out['index'] = out_value['index']
            return out
        else:
            out_value = Match(Token_type.IDENTIFIER, j)
            Children.append(out_value['node'])
            # Create a tree node
            node = Tree('Value', Children)
            out['node'] = node
            out['index'] = out_value['index']
            return out
    elif temp1['token_type'] == Token_type.CONSTANT:
        if temp2['token_type'] == Token_type.PlusOp or temp2['token_type'] == Token_type.MinusOp or temp2['token_type'] == Token_type.MultiplyOp or temp2['token_type'] == Token_type.DivideOp :
            out_value = Experssion(j, "constant")
            Children.append(out_value['node'])
            # Create a tree node
            node = Tree('Value', Children)
            out['node'] = node
            out['index'] = out_value['index']
            return out
        else:
            out_value = Match(Token_type.CONSTANT, j)
            Children.append(out_value['node'])
            # Create a tree node
            node = Tree('Value', Children)
            out['node'] = node
            out['index'] = out_value['index']
            return out
    elif temp1['token_type'] == Token_type.STRING:
        if temp2['token_type'] == Token_type.PlusOp:
            out_value = Experssion(j, "string")
            Children.append(out_value['node'])
            # Create a tree node
            node = Tree('Value', Children)
            out['node'] = node
            out['index'] = out_value['index']
            return out
        else:
            out_value = Match(Token_type.STRING, j)
            Children.append(out_value['node'])
            # Create a tree node
            node = Tree('Value', Children)
            out['node'] = node
            out['index'] = out_value['index']
            return out
    else:
        out['node'] = ["error"]
        out['index'] = j
        errors.append("Syntax error." + temp1['Lex'])
        return out

def Experssion(j, type):
    global current_SemiColon
    Children = []
    out = dict()
    temp = TOKENS[j].to_dict()
    print(temp)
    if type == "constant":
        out_const1 = Match(Token_type.CONSTANT, j)
        Children.append(out_const1['node'])
        temp3 = TOKENS[out_const1['index']].to_dict()['token_type']
        print(temp3)
        out_operator = Match(temp3, out_const1['index'])
        Children.append(out_operator['node'])
        temp4 = TOKENS[out_operator['index']].to_dict()['token_type']
        if (temp4 == Token_type.IDENTIFIER):
            out_id2 = Match(Token_type.IDENTIFIER, out_operator['index'])
        elif (temp4 == Token_type.CONSTANT):
            out_id2 = Match(Token_type.CONSTANT, out_operator['index'])
        Children.append(out_id2['node'])
        # Create a tree node
        node = Tree('Expression', Children)
        out['node'] = node
        out['index'] = out_id2['index']
        return out
    elif type == "string":
        out_string1 = Match(Token_type.STRING, j)
        Children.append(out_string1['node'])
        out_operator = Match(Token_type.PlusOp, out_string1['index'])
        Children.append(out_operator['node'])
        out_string2 = Match(Token_type.STRING, out_operator['index'])
        Children.append(out_string2['node'])
        # Create a tree node
        node = Tree('Expression', Children)
        out['node'] = node
        out['index'] = out_string2['index']
        return out
    elif type == "id":
        out_id = Match(Token_type.IDENTIFIER, j)
        Children.append(out_id['node'])
        temp3 = TOKENS[out_id['index']].to_dict()['token_type']
        print(temp3)
        out_operator = Match(temp3, out_id['index'])
        Children.append(out_operator['node'])
        temp4 = TOKENS[out_operator['index']].to_dict()['token_type']
        if (temp4 == Token_type.IDENTIFIER):
            out_id2 = Match(Token_type.IDENTIFIER, out_operator['index'])
        elif (temp4 == Token_type.CONSTANT):
            out_id2 = Match(Token_type.CONSTANT, out_operator['index'])
        Children.append(out_id2['node'])
        # Create a tree node
        node = Tree('Expression', Children)
        out['node'] = node
        out['index'] = out_id2['index']
        return out

##Const BLock
def ConstBlock(j):
    global current_SemiColon
    temp = TOKENS[j].to_dict()
    if(temp['token_type']==Token_type.CONST):
        print("After If Temp")
        Children = []
        out = dict()
        out_Const = Match(Token_type.CONST, j)
        Children.append(out_Const['node'])
        out_ConstVar=ConstVar(out_Const['index'])
        Children.append(out_ConstVar['node'])

        #Create a tree node
        node = Tree('ConstBlock', Children)
        out['node'] = node
        out['index'] = out_ConstVar['index']
        return out
    else:
        out = {'node':'', 'index':j}
        return out

def ConstVar(j):
    global current_SemiColon
    Children = []
    out = dict()
    out_cs = ConstStat(j)
    Children.append(out_cs['node'])
    out_constvard = constVar_d(out_cs['index'])
    if (not (out_constvard['node'] == '')):
        Children.append(out_constvard['node'])

    node = Tree('ConstVar', Children)
    out['node'] = node
    out['index'] = out_constvard['index']
    return out

def constVar_d(j):
    global current_SemiColon
    Children = []
    out = dict()
    temp = TOKENS[j].to_dict()
    if temp["token_type"] == Token_type.IDENTIFIER:
        out_conststat = ConstStat(j)
        Children.append(out_conststat['node'])
        out_ConstVar_d = constVar_d(out_conststat['index'])
        if (not (out_ConstVar_d['node'] == '')):
            Children.append(out_ConstVar_d['node'])

        # Create a tree node
        node = Tree('ConstVar_d', Children)
        out['node'] = node
        out['index'] = out_ConstVar_d['index']
        return out

    else:
        out = {'node': '', 'index': j}
        return out

def ConstStat(j):
    global current_SemiColon
    Children = []
    out = dict()
    out_id = Match(Token_type.IDENTIFIER, j)
    Children.append(out_id['node'])
    out_equal = Match(Token_type.EqualOp, out_id['index'])
    Children.append(out_equal['node'])
    out_value = Constvalue(out_equal['index'])
    Children.append(out_value['node'])
    if current_SemiColon >= len(SemiColonsErrorsFollow):
        out = {'node': '', 'index': j - 1}
        return out
    temp = SemiColonsErrorsFollow[current_SemiColon]
    current_SemiColon += 1
    #print("CurrentSemiColon: ")
    #print(temp)
    out_semi = Match(Token_type.Semicolon, temp - 1)
    Children.append(out_semi['node'])

    node = Tree('ConstStat', Children)
    out['node'] = node
    out['index'] = out_semi['index']
    return out

def Constvalue(j):
    global current_SemiColon
    temp = TOKENS[j].to_dict()
    #for integer/real
    if temp['token_type']== Token_type.CONSTANT:
        Children = []
        out = dict()
        out_int = Match(Token_type.CONSTANT, j)
        Children.append(out_int['node'])

        node = Tree('Constvalue', Children)
        out['node'] = node
        out['index'] = out_int['index']
        return out
    # for real if we change lexical real/integer
    # elif temp['token_type'] == Token_type.Real:
    #     Children = []
    #     out = dict()
    #     out_real = Match(Token_type.Real, j)
    #     Children.append(out_real['node'])
    #
    #     node = Tree('ConstValue', Children)
    #     out['node'] = node
    #     out['index'] = out_real['index']
    #     return out
    elif temp['token_type'] == Token_type.STRING:
        Children = []
        out = dict()
        out_string = Match(Token_type.STRING, j)
        Children.append(out_string['node'])

        node = Tree('ConstValue', Children)
        out['node'] = node
        out['index'] = out_string['index']
        return out
    elif temp['token_type'] == Token_type.SET:
        Children = []
        out = dict()
        out_set = Match(Token_type.SET, j)
        Children.append(out_set['node'])
        out_of = Match(Token_type.OF, out_set['index'])
        Children.append(out_of['node'])
        out_leftpar = Match(Token_type.LEFT_PAR, out_of['index'])
        Children.append(out_leftpar['node'])
        out_vnames = vnames(out_leftpar['index'])
        Children.append(out_vnames['node'])
        out_rightPar = Match(Token_type.RIGHT_PAR, out_vnames['index'])
        Children.append(out_rightPar['node'])

        #Tree
        node = Tree('ConstValue', Children)
        out['node'] = node
        out['index'] = out_rightPar['index']
        return out


def ifStatement(j):
    global current_SemiColon
    Children = []
    out = dict()
    out_if = Match(Token_type.If, j)
    Children.append(out_if['node'])
    out_cond = Cond(out_if['index'])
    Children.append(out_cond['node'])
    out_then = Match(Token_type.THEN, out_cond['index'])
    Children.append(out_then['node'])
    out_statement = Statement(out_then['index'])
    Children.append(out_statement['node'])
    out_ifstatement_d = ifStatement_d(out_statement['index'])
    if (not (out_ifstatement_d['node'] == '')):
        Children.append(out_ifstatement_d['node'])

    #Tree
    node = Tree('IfStatement', Children)
    out['node'] = node
    out['index'] = out_ifstatement_d['index']
    return out
def ifStatement_d(j):
    global current_SemiColon
    Children = []
    out = dict()
    if (TOKENS[j -1] == TOKENS[-1]):  ##########for not accessing out of index
        out = {'node': '', 'index': j-1}
        return out
    temp = TOKENS[j].to_dict()
    if(temp['token_type']==Token_type.ENDDOT):
        out = {'node': '', 'index': j}
        return out
    # print(temp)
    temp2 = TOKENS[j+1].to_dict()
    if temp["token_type"]==Token_type.Else:
        if temp2["token_type"]==Token_type.If:
            Children.append('Else if')
            out_cond = Cond(j+2)
            Children.append(out_cond['node'])
            out_then = Match(Token_type.THEN, out_cond['index'])
            Children.append(out_then['node'])
            out_statement = Statements(out_then['index'])
            Children.append(out_statement['node'])
            out_ifstatement_d = ifStatement_d(out_statement['index'])
            Children.append(out_ifstatement_d['node'])
            # Tree
            node = Tree('Else if', Children)
            out['node'] = node
            out['index'] = out_ifstatement_d['index']
            return out
        else:
            out_else = Match(Token_type.Else, j)
            Children.append(out_else['node'])
            out_statement = Statement(out_else['index'])
            Children.append(out_statement['node'])
            # Tree
            node = Tree('Else', Children)
            out['node'] = node
            out['index'] = out_statement['index']
            return out


    else:
        out = {'node': '', 'index': j}
        return out

def RepeatStatement(j):
    global current_SemiColon
    Children = []
    out = dict()
    out_repeat = Match(Token_type.REPEAT,j)
    Children.append(out_repeat['node'])
    out_Statement = Statement(out_repeat['index'])
    Children.append(out_Statement['node'])
    while(True):
        out_Statement = Statement(out_Statement['index'])
        Children.append(out_Statement['node'])
        temp=TOKENS[out_Statement['index']].to_dict()
        if(temp['token_type']==Token_type.UNTIL):
            break
    out_until = Match(Token_type.UNTIL, out_Statement['index'])
    Children.append(out_until['node'])
    out_Cond = Cond(out_until['index'])
    Children.append(out_Cond['node'])
    if current_SemiColon >= len(SemiColonsErrorsFollow):
        out = {'node': '', 'index': j - 1}
        return out
    temp = SemiColonsErrorsFollow[current_SemiColon]
    current_SemiColon += 1
    print("CurrentSemiColon: ")
    print(temp)
    out_semi = Match(Token_type.Semicolon, temp - 1)
    Children.append(out_semi['node'])
    # Tree
    node = Tree('RepeatStatement',Children)
    out['node'] = node
    out['index'] = out_semi['index']
    return out

# cond -> (boolex) eq (boolex) | boolex
# boolex -> boolvar relop boolvar
# boolvar -> id | constant
# eq -> <> | =

def Cond(j):
    global current_SemiColon
    Children = []
    out = dict()
    if (TOKENS[j - 1] == TOKENS[-1]):  ##########for not accessing out of index
        out = {'node': '', 'index': j-1}
        return out
    temp = TOKENS[j].to_dict()
    if (temp['token_type'] == Token_type.LEFT_PAR):
        out_lp = Match(Token_type.LEFT_PAR, j)
        Children.append(out_lp['node'])
        out_bol = boolex(out_lp['index'])
        Children.append(out_bol['node'])
        out_rp = Match(Token_type.RIGHT_PAR, out_bol['index'])
        Children.append(out_rp['node'])


        # Matching equal operators
        temp2 = TOKENS[out_rp['index']].to_dict()
        eq = ['<>', '=']
        if temp2['Lex'] in eq:
            Children.append(temp2['Lex'])
        else:
            node = Tree('Condition', Children)
            out['node'] = node
            out['index'] = out_rp['index']
            return out

        out_lp = Match(Token_type.LEFT_PAR, out_rp['index'] + 1)
        Children.append(out_lp['node'])
        out_bol = boolex(out_lp['index'])
        Children.append(out_bol['node'])
        out_rp = Match(Token_type.RIGHT_PAR, out_bol['index'])
        Children.append(out_rp['node'])

        # Create a tree node
        node = Tree('Condition', Children)
        out['node'] = node
        out['index'] = out_rp['index']
        return out


    elif (temp['token_type'] == Token_type.IDENTIFIER) or (temp['token_type'] == Token_type.CONSTANT):
        out_bol = boolex(j)
        Children.append(out_bol['node'])
        # Create a tree node
        node = Tree('Condition', Children)
        out['node'] = node
        out['index'] = out_bol['index']
        return out

    else:
        out['node'] = ['error']
        out['index'] = j + 1
        errors.append("Syntax error." + temp['Lex'])
        return out


def boolex(j):
    global current_SemiColon
    Children = []
    out = dict()
    temp = TOKENS[j].to_dict()

    # Matching variables
    if (temp['token_type'] == Token_type.IDENTIFIER):
        out_var = Match(Token_type.IDENTIFIER, j)
        Children.append(out_var['node'])

    else:
        out_var = Match(Token_type.CONSTANT, j)
        Children.append(out_var['node'])

    # Matching relational operator
    temp = TOKENS[out_var['index']].to_dict()
    if temp['Lex'] in Relational_Operators:
        Children.append(temp['Lex'])
    else:
        out_err = dict()
        out_err['node'] = ['error']
        Children.append(out_err['node'])

    # Matching variables
    temp = TOKENS[out_var['index'] + 1].to_dict()
    if (temp['token_type'] == Token_type.IDENTIFIER):
        out_var2 = Match(Token_type.IDENTIFIER, out_var['index'] + 1)
        Children.append(out_var2['node'])

    else:
        out_var2 = Match(Token_type.CONSTANT, out_var['index'] + 1)
        Children.append(out_var2['node'])

    # Create a tree node
    node = Tree('Boolean Expression', Children)
    out['node'] = node
    out['index'] = out_var2['index']
    return out

# FuncBlock
def FuncBlock(j):
    global current_SemiColon
    Children = []
    out = dict()
    out_function = Match(Token_type.FUNCTION, j)
    Children.append(out_function['node'])
    print(out_function)
    out_id = Match(Token_type.IDENTIFIER, out_function['index'])
    if not (out_id['node'] == ["error"]):
        temp4 = out_id['node']
        functionnames.append(temp4[0])
    # print(temp4)
    # print(functionnames)
    Children.append(out_id['node'])
    out_leftpar = Match(Token_type.LEFT_PAR, out_id['index'])
    Children.append(out_leftpar['node'])

    #F
    out_F = F(out_leftpar['index'])
    Children.append(out_F['node'])

    out_rightpar = Match(Token_type.RIGHT_PAR, out_F['index'])
    Children.append(out_rightpar['node'])
    out_colon = Match(Token_type.Colon, out_rightpar['index'])
    Children.append(out_colon['node'])

    temp = TOKENS[out_colon['index']].to_dict()
    out_dt = dict()
    if temp['Lex'] in Data_Types or temp['Lex'] in newDataTypes:
        out_dt = Match(temp['token_type'], out_colon["index"])
    else:
        out_dt["node"] = ["error"]
        out_dt["index"] = out_colon['index'] + 1
        errors.append("Syntax error : " + temp['Lex'])
    Children.append(out_dt["node"])
    if current_SemiColon >= len(SemiColonsErrorsFollow):
        out = {'node': '', 'index': j - 1}
        return out
    temp = SemiColonsErrorsFollow[current_SemiColon]
    current_SemiColon += 1
    # print("CurrentSemiColon: ")
    # print(temp)
    out_semi = Match(Token_type.Semicolon, temp - 1)
    Children.append(out_semi['node'])

    out_variables = variables(out_semi['index'])
    Children.append(out_variables['node'])
    out_block = fBlock(out_variables['index'])
    Children.append(out_block['node'])

    #Tree
    node = Tree('FuncBlock', Children)
    out['node'] = node
    out['index'] = out_block['index']
    return out
def F(j):
    global current_SemiColon
    temp = TOKENS[j].to_dict()
    if temp['token_type'] == Token_type.VAR or temp['token_type'] == Token_type.IDENTIFIER:
        Children = []
        out = dict()
        out_vs = fvstatement(j)
        Children.append(out_vs['node'])

        # Tree
        node = Tree('F', Children)
        out['node'] = node
        out['index'] = out_vs['index']
        return out

    else:
        out = {'node': '', 'index': j}
        return out
def FP(j):
    global current_SemiColon
    temp = TOKENS[j].to_dict()
    Children = []
    out = dict()
    if (temp['token_type'] == Token_type.FUNCTION):
        print("Entered Function")
        out_FB = FuncBlock(j)
        Children.append(out_FB['node'])

        # Create a tree node
        node = Tree('Function', Children)
        out['node'] = node
        out['index'] = out_FB['index']
        return out
    else:
        out = {'node': '', 'index': j}
        return out
def fvstatement(j):
    global current_SemiColon
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
        errors.append("Syntax error : " + temp['Lex'])
    Children.append(out_dt["node"])
    temp2 = TOKENS[out_dt['index']].to_dict()
    if temp2['Lex'] == Token_type.Semicolon:
        temp = SemiColonsErrorsFollow[current_SemiColon]
        current_SemiColon += 1
           #print("CurrentSemiColon: ")
        #print(temp)
        out_semi = Match(Token_type.Semicolon, temp - 1)
        Children.append(out_semi["node"])

        # Create a tree node
        node = Tree('Variable Name', Children)
        out['node'] = node
        out['index'] = out_semi['index']
        return out
    else:
        # Create a tree node
        node = Tree('Variable Name', Children)
        out['node'] = node
        out['index'] = out_dt['index']
        return out
def fBlock(j):
    global current_SemiColon
    Token_types_aux =\
        [Token_type.If, Token_type.Read, Token_type.FOR, Token_type.REPEAT,
         Token_type.IDENTIFIER, Token_type.ReadLine, Token_type.Write, Token_type.WriteLine]
    children = []
    out = dict()
    if (TOKENS[j - 1] == TOKENS[-1]):  ##########for not accessing out of index
        out = {'node': '', 'index': j-1}
        return out
    temp = TOKENS[j].to_dict()
    if temp["token_type"] == Token_type.Begin:
        out_begin = Match(Token_type.Begin, j)
        children.append(out_begin['node'])
        out_stat = Statements(out_begin['index'])
        children.append(out_stat['node'])
        out_end = Match(Token_type.End, out_stat['index'])
        children.append(out_end['node'])
        if current_SemiColon >= len(SemiColonsErrorsFollow):
            out = {'node': '', 'index': j - 1}
            return out
        temp1 = SemiColonsErrorsFollow[current_SemiColon]
        current_SemiColon += 1
        print("CurrentSemiColon: ")
        print(temp1)
        out_semi = Match(Token_type.Semicolon, temp1-1)
        children.append(out_semi['node'])

        node = Tree('Block', children)
        out['node'] = node
        out['index'] = out_semi['index']
        return out
    elif temp["token_type"] in Token_types_aux:
        out_stats = Statements(j)
        children.append(out_stats['node'])
        node = Tree('Block', children)
        out['node'] = node
        out['index'] = out_stats['index']
        return out
def vfnames(j):
    global current_SemiColon
    Children = []
    out = dict()
    temp = TOKENS[j].to_dict()
    if temp['token_type'] == Token_type.IDENTIFIER:
        out_id = Match(Token_type.IDENTIFIER, j)
    elif temp['token_type'] == Token_type.CONSTANT:
        out_id = Match(Token_type.IDENTIFIER, j)
    Children.append(out_id['node'])
    out_evn = extravfnames(out_id['index'])
    if (not (out_evn['node'] == '')):
        Children.append(out_evn['node'])

    # Create a tree node
    node = Tree('Variable Names', Children)
    out['node'] = node
    out['index'] = out_evn['index']
    return out


def extravfnames(j):
    global current_SemiColon
    temp = TOKENS[j].to_dict()
    if temp['token_type'] == Token_type.Comma:
        Children = []
        out = dict()
        out_comma = Match(Token_type.Comma, j)
        Children.append(out_comma['node'])
        temp3 = out_comma['index']
        temp2 = TOKENS[temp3].to_dict()
        if temp2['token_type'] == Token_type.IDENTIFIER:
            out_id = Match(Token_type.IDENTIFIER, temp3)
        elif temp2['token_type'] == Token_type.CONSTANT:
            out_id = Match(Token_type.IDENTIFIER, temp3)
        Children.append(out_id['node'])
        out_ex = extravfnames(out_id['index'])
        if (not (out_ex['node'] == '')):
            Children.append(out_ex['node'])
        # Create a tree node
        node = Tree('Function Variables', Children)
        out['node'] = node
        out['index'] = out_ex['index']
        return out
    else:
        out = {'node': '', 'index': j}
        return out


def Parse():
    global current_SemiColon
    count = 0
    for i in TOKENS:
        count += 1
        temp = i.to_dict()
        if temp['token_type'] == Token_type.Semicolon:
            SemiColonsErrorsFollow.append(count)
    print(SemiColonsErrorsFollow)
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
    if (not (Dec_dic['node'] == '')):
        Children.append(Dec_dic['node'])

    # Function
    func_dic = FP(Dec_dic['index'])
    if (not (func_dic['node'] == '')):
        Children.append(func_dic['node'])

    print("Finished Function")
    #Begin
    Beg_dic = Match(Token_type.Begin,func_dic['index'])
    Children.append(Beg_dic['node'])

    print("Finished Begin")

    #Block
    Block_dict = Block(Beg_dic["index"])
    if (not (Block_dict['node'] == '')):
        Children.append(Block_dict['node'])
    print("Finished Block")
    #Enddot
    End_dict = Match(Token_type.ENDDOT, Block_dict['index'])
    Children.append(End_dict['node'])

    Node = Tree('Program', Children)
    return Node


# Presentation
##### GUI
root = tk.Tk()
root.title('Pascal compiler')
root.resizable(False, False)

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

# n stands for a number
# l stands for a letter
# . stands for a .
# ' stands for a '
# o stands for other symbols
constants_graph = VisualDFA(
    states={'A', 'B', 'C'},
    input_symbols={'n', '.', 'o', 'l', '\''},
    transitions={
        'A': {'n':'B', 'o':'C', 'l':'C', '.':'C', '\'':'C'},
        'B': {'n':'B', 'o':'C', 'l':'C', '.':'B', '\'':'C'},
        'C': {'n':'C', 'o':'C', 'l':'C', '.':'C', '\'':'C'}
    },
    initial_state='A',
    final_states={'B'}
)


strings_graph = VisualDFA(
    states={'A', 'B', 'C', 'D'},
    input_symbols={'n', '.', 'o', 'l', '\''},
    transitions={
        'A': {'n':'D', 'o':'D', 'l':'D', '.':'D', '\'':'B'},
        'B': {'n':'B', 'o':'B', 'l':'B', '.':'B', '\'':'C'},
        'C': {'n':'D', 'o':'D', 'l':'D', '.':'D', '\'':'D'},
        'D': {'n':'D', 'o':'D', 'l':'D', '.':'D', '\'':'D'}
    },
    initial_state='A',
    final_states={'C'}
)

identifiers_graph = VisualDFA(
    states={'A', 'B', 'C'},
    input_symbols={'n', '.', 'o', 'l', '\''},
    transitions={
        'A': {'n':'C', 'o':'C', 'l':'B', '.':'C', '\'':'C'},
        'B': {'n':'B', 'o':'C', 'l':'B', '.':'C', '\'':'C'},
        'C': {'n':'C', 'o':'C', 'l':'C', '.':'C', '\'':'C'}
    },
    initial_state='A',
    final_states={'B'}
)

def get_in(sub):
    out = ''
    for i in sub:
        if i.isnumeric():
            out+='n'
        elif i=='.' or i=='\'':
            out+=i
        elif i.isalpha() or i=='_':
            out+='l'
        else:
            out+='o'
    return out


def open_dfa():
    new_window = tk.Toplevel(root)
    new_window.resizable(False, False)
    token_label = tk.Label(new_window, text=result_val, fg='black', font=('helvetica', 16, 'bold'))
    constant_text = tk.Label(new_window, text='constants', fg='black', font=('helvetica', 16, 'bold'))
    constant_image = tk.Label(new_window)
    const_img = Image.open('Constants.png')
    width, height = const_img.size
    const_img = const_img.resize((int(width/2), int(height/2)), Image.LANCZOS)
    const_photo = ImageTk.PhotoImage(const_img)
    constant_image.image = const_photo
    constant_image['image'] = const_photo

    identifier_text = tk.Label(new_window, text='identifiers', fg='black', font=('helvetica', 16, 'bold'))
    identifier_image = tk.Label(new_window)
    id_img = Image.open('Identifiers.png')
    width, height = id_img.size
    id_img = id_img.resize((int(width/2), int(height/2)), Image.LANCZOS)
    id_photo = ImageTk.PhotoImage(id_img)
    identifier_image.image = id_photo
    identifier_image['image'] = id_photo

    strings_text = tk.Label(new_window, text='strings', fg='black', font=('helvetica', 16, 'bold'))
    strings_image = tk.Label(new_window)
    st_img = Image.open('Strings.png')
    width, height = st_img.size
    st_img = st_img.resize((int(width/2), int(height/2)), Image.LANCZOS)
    st_photo = ImageTk.PhotoImage(st_img)
    strings_image.image = st_photo
    strings_image['image'] = st_photo

    token_label.grid(row=0, column=0)
    constant_text.grid(row=1, column=0)
    constant_image.grid(row=2, column=0)
    identifier_text.grid(row=1, column=1)
    identifier_image.grid(row=2, column=1)
    strings_text.grid(row=1, column=2)
    strings_image.grid(row=2, column=2)

def on_cell_clicked(event, dTDaPT: pt.Table):
    global result_val
    row = dTDaPT.get_row_clicked(event)
    col = dTDaPT.get_col_clicked(event)
    if row is not None and col is not None:
        cell_value = dTDaPT.model.getValueAt(row, col)
        print("Cell clicked: row={}, col={}, value={}".format(row, col, cell_value))
        result_val = cell_value
        graph_input = get_in(cell_value)
        print(graph_input)
        constants_graph.show_diagram(graph_input, filename='Constants', format_type='png')
        strings_graph.show_diagram(graph_input, filename='Strings', format_type='png')
        identifiers_graph.show_diagram(graph_input, filename='Identifiers', format_type='png')
        open_dfa()


def Scan():
    global current_SemiColon, TOKENS, errors, newDataTypes, SemiColonsErrorsFollow, functionnames
    TOKENS = []
    errors = []
    newDataTypes = []
    SemiColonsErrorsFollow = []
    functionnames = []
    current_SemiColon = 0

    x1 = entry1.get()
    find_token(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in TOKENS])
    # print(df)

    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    dTDaPT.bind("<ButtonRelease-1>", lambda event: on_cell_clicked(event,dTDaPT))    # start Parsing
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

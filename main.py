import tkinter as tk
from enum import Enum
import re
import pandas


class Token_type(Enum):  # listing all tokens type
    Begin = 1
    End = 2
    Do = 3
    Else = 4
    NOT = 5
    If = 6
    Integer = 7
    Dot = 8
    Semicolon = 9
    EqualOp = 10
    LessThanOp = 11
    GreaterThanOp = 12
    NotEqualOp = 13
    PlusOp = 14
    MinusOp = 15
    MultiplyOp = 16
    DivideOp = 17
    Identifier = 18
    Constant = 19
    LEFTPARENTHESIS = 20
    RIGHTPARENTHESIS = 21
    STRING = 22
    LEFTLINECOMMENT = 23
    ANDWORD = 24
    ARRAY = 25
    CASE = 26
    CONST = 27
    DIV = 28
    DOWNTO = 29
    FILE = 30
    FOR = 31
    FUNCTION = 32
    GOTO = 33
    IN = 34
    LABEL = 35
    MOD = 36
    NIL = 37
    OF=38
    OR=39
    PACKED=40
    PROCEDURE=41
    PROGRAM=42
    RECORD=43
    REPEAT=44
    SET=45
    THEN=46
    TO=47
    TYPE=48
    UNTIL=49
    VAR=50
    WHILE=51
    WITH=52
    COMMENT=53
    Error = 54
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


# Reserved word Dictionary
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
    "file":Token_type.FILE,
    "for": Token_type.FOR,
    "functions": Token_type.FUNCTION,
    "goto": Token_type.GOTO,
    "if": Token_type.If,
    "in": Token_type.IN,
    "label":Token_type.LABEL,
    "mod":Token_type.MOD,
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
}
Operators = {".": Token_type.Dot,
             ";": Token_type.Semicolon,
             "=": Token_type.EqualOp,
             "+": Token_type.PlusOp,
             "-": Token_type.MinusOp,
             "*": Token_type.MultiplyOp,
             "/": Token_type.DivideOp
             }
Tokens = []  # to add tokens to list


def find_token(text):
    tokens = text.split()
    for TOKEN in tokens:
        if TOKEN in ReservedWords:
            Tokens.append(token(TOKEN, ReservedWords[TOKEN]))
        elif TOKEN in Operators:
            Tokens.append(token(TOKEN, Operators[TOKEN]))
        elif re.match("^{(\s|\S)*}$",TOKEN):
            t = token(TOKEN, Token_type.COMMENT)
            Tokens.append(t)
        elif re.match("^[0-9]+(\.[0-9]*)?$", TOKEN):
            Tokens.append(token(TOKEN, Token_type.Constant))
        elif re.match("^[a-zA-Z][a-zA-Z0-9]*$", TOKEN):
            Tokens.append(token(TOKEN, Token_type.Identifier))
        else:
            Tokens.append(token(TOKEN, Token_type.Error))

    # complete


# GUI
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
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    print(df)
    label3 = tk.Label(root, text='Lexem ' + x1 +
                      ' is:', font=('helvetica', 10))
    canvas1.create_window(200, 210, window=label3)

    label4 = tk.Label(root, text="Token_type"+x1,
                      font=('helvetica', 10, 'bold'))
    canvas1.create_window(200, 230, window=label4)


button1 = tk.Button(text='Scan', command=Scan, bg='brown',
                    fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)
root.mainloop()

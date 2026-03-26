"""
KashaLang Lexer - Tokenizer for African-inspired programming language
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Iterator
import re

class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    NULL = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # African-inspired Keywords (Kinyarwanda/Swahili based)
    VUGA = auto()           # print
    SHYIRAMO = auto()       # variable declaration (let/var)
    NIBA = auto()           # if
    NANONE = auto()         # else
    SUBIRAMO = auto()       # loop/for/while
    KUGEZA = auto()         # until/for range
    IGIHE = auto()          # while
    FATA = auto()           # function
    SUBIZA = auto()         # return
    KANDI = auto()          # and
    CYANGWA = auto()        # or
    SIYO = auto()           # not
    KUBERA = auto()         # break
    KOMEZA = auto()         # continue
    REKA = auto()           # stop/exit
    INJIZA = auto()         # input
    UBWOKO = auto()         # type
    URUTONDE = auto()       # list/array
    IKIGONDO = auto()       # dictionary/object
    UMUBARE = auto()        # number
    UMUTWE = auto()         # string
    UKURI = auto()          # boolean true
    IBINYA = auto()         # boolean false
    TARUZA = auto()         # null/none
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    ASSIGN = auto()
    
    # Comparison
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    SEMICOLON = auto()
    ARROW = auto()          # -> for function returns
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    INDENT = auto()
    DEDENT = auto()
    COMMENT = auto()

@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"

class Lexer:
    """KashaLang Lexer - Converts source code into tokens"""
    
    # African-inspired keywords mapping
    KEYWORDS = {
        'vuga': TokenType.VUGA,
        'shyiramo': TokenType.SHYIRAMO,
        'niba': TokenType.NIBA,
        'nanone': TokenType.NANONE,
        'subiramo': TokenType.SUBIRAMO,
        'kugeza': TokenType.KUGEZA,
        'igihe': TokenType.IGIHE,
        'fata': TokenType.FATA,
        'subiza': TokenType.SUBIZA,
        'kandi': TokenType.KANDI,
        'cyangwa': TokenType.CYANGWA,
        'siyo': TokenType.SIYO,
        'kubera': TokenType.KUBERA,
        'komeza': TokenType.KOMEZA,
        'reka': TokenType.REKA,
        'injiza': TokenType.INJIZA,
        'ubwoko': TokenType.UBWOKO,
        'urutonde': TokenType.URUTONDE,
        'ikigondo': TokenType.IKIGONDO,
        'umubare': TokenType.UMUBARE,
        'umutwe': TokenType.UMUTWE,
        'ukuri': TokenType.UKURI,
        'ibinya': TokenType.IBINYA,
        'taruza': TokenType.TARUZA,
        # English aliases for accessibility
        'print': TokenType.VUGA,
        'let': TokenType.SHYIRAMO,
        'var': TokenType.SHYIRAMO,
        'if': TokenType.NIBA,
        'else': TokenType.NANONE,
        'loop': TokenType.SUBIRAMO,
        'for': TokenType.KUGEZA,
        'while': TokenType.IGIHE,
        'fn': TokenType.FATA,
        'func': TokenType.FATA,
        'return': TokenType.SUBIZA,
        'and': TokenType.KANDI,
        'or': TokenType.CYANGWA,
        'not': TokenType.SIYO,
        'break': TokenType.KUBERA,
        'continue': TokenType.KOMEZA,
        'stop': TokenType.REKA,
        'input': TokenType.INJIZA,
        'type': TokenType.UBWOKO,
        'list': TokenType.URUTONDE,
        'dict': TokenType.IKIGONDO,
        'number': TokenType.UMUBARE,
        'string': TokenType.UMUTWE,
        'true': TokenType.UKURI,
        'false': TokenType.IBINYA,
        'null': TokenType.TARUZA,
        'none': TokenType.TARUZA,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.indent_stack = [0]
        
    def error(self, message: str):
        from .errors import KashaError
        raise KashaError(message, self.line, self.column)
    
    def peek(self, offset: int = 0) -> str:
        pos = self.pos + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def advance(self) -> str:
        char = self.peek()
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        while self.peek() in ' \t\r':
            self.advance()
    
    def read_string(self, quote: str) -> str:
        """Read a string literal"""
        self.advance()  # consume opening quote
        result = ""
        while self.peek() != quote and self.peek() != '\0':
            if self.peek() == '\\':
                self.advance()
                escape_char = self.advance()
                if escape_char == 'n':
                    result += '\n'
                elif escape_char == 't':
                    result += '\t'
                elif escape_char == '\\':
                    result += '\\'
                elif escape_char == quote:
                    result += quote
                else:
                    result += escape_char
            else:
                result += self.advance()
        if self.peek() == quote:
            self.advance()  # consume closing quote
        else:
            self.error("Unterminated string literal")
        return result
    
    def read_number(self) -> Token:
        """Read a number (integer or float)"""
        start_line = self.line
        start_col = self.column
        result = ""
        is_float = False
        
        while self.peek().isdigit():
            result += self.advance()
        
        if self.peek() == '.' and self.peek(1).isdigit():
            is_float = True
            result += self.advance()  # consume '.'
            while self.peek().isdigit():
                result += self.advance()
        
        # Scientific notation
        if self.peek() in 'eE':
            result += self.advance()
            if self.peek() in '+-':
                result += self.advance()
            while self.peek().isdigit():
                result += self.advance()
        
        value = float(result) if is_float else int(result)
        return Token(TokenType.NUMBER, value, start_line, start_col)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword"""
        start_line = self.line
        start_col = self.column
        result = ""
        
        while self.peek().isalnum() or self.peek() == '_':
            result += self.advance()
        
        # Check if it's a keyword (case insensitive for African keywords)
        token_type = self.KEYWORDS.get(result.lower(), TokenType.IDENTIFIER)
        
        # Handle boolean literals
        if token_type == TokenType.UKURI:
            return Token(TokenType.BOOLEAN, True, start_line, start_col)
        elif token_type == TokenType.IBINYA:
            return Token(TokenType.BOOLEAN, False, start_line, start_col)
        elif token_type == TokenType.TARUZA:
            return Token(TokenType.NULL, None, start_line, start_col)
        
        return Token(token_type, result, start_line, start_col)
    
    def read_comment(self):
        """Read a comment (starts with # or //)"""
        if self.peek() == '#':
            while self.peek() != '\n' and self.peek() != '\0':
                self.advance()
        elif self.peek() == '/' and self.peek(1) == '/':
            self.advance()
            self.advance()
            while self.peek() != '\n' and self.peek() != '\0':
                self.advance()
    
    def handle_indentation(self) -> List[Token]:
        """Handle Python-style indentation"""
        tokens = []
        current_indent = 0
        
        # Count spaces/tabs at start of line
        while self.peek() == ' ':
            current_indent += 1
            self.advance()
        
        if self.peek() == '\t':
            self.error("Tabs are not allowed for indentation. Use spaces.")
        
        # Skip empty lines and comments
        if self.peek() == '\n' or self.peek() == '#' or (self.peek() == '/' and self.peek(1) == '/'):
            return tokens
        
        # Compare with previous indentation
        if current_indent > self.indent_stack[-1]:
            self.indent_stack.append(current_indent)
            tokens.append(Token(TokenType.INDENT, current_indent, self.line, self.column))
        elif current_indent < self.indent_stack[-1]:
            while current_indent < self.indent_stack[-1]:
                self.indent_stack.pop()
                tokens.append(Token(TokenType.DEDENT, current_indent, self.line, self.column))
            if current_indent != self.indent_stack[-1]:
                self.error("Inconsistent indentation")
        
        return tokens
    
    def tokenize(self) -> List[Token]:
        """Main tokenization method"""
        while self.pos < len(self.source):
            char = self.peek()
            start_line = self.line
            start_col = self.column
            
            # Handle newlines and indentation
            if char == '\n':
                self.advance()
                self.tokens.append(Token(TokenType.NEWLINE, '\n', start_line, start_col))
                # Handle indentation on next line
                indent_tokens = self.handle_indentation()
                self.tokens.extend(indent_tokens)
                continue
            
            # Skip regular whitespace
            if char in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Comments
            if char == '#' or (char == '/' and self.peek(1) == '/'):
                self.read_comment()
                continue
            
            # Strings
            if char in '"\'':
                string_val = self.read_string(char)
                self.tokens.append(Token(TokenType.STRING, string_val, start_line, start_col))
                continue
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Two-character operators
            two_char = char + self.peek(1)
            if two_char == '==':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQUAL, '==', start_line, start_col))
                continue
            elif two_char == '!=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', start_line, start_col))
                continue
            elif two_char == '<=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', start_line, start_col))
                continue
            elif two_char == '>=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', start_line, start_col))
                continue
            elif two_char == '->':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ARROW, '->', start_line, start_col))
                continue
            elif two_char == '**':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.POWER, '**', start_line, start_col))
                continue
            
            # Single-character operators and delimiters
            single_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '=': TokenType.ASSIGN,
                '<': TokenType.LESS,
                '>': TokenType.GREATER,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ',': TokenType.COMMA,
                '.': TokenType.DOT,
                ':': TokenType.COLON,
                ';': TokenType.SEMICOLON,
            }
            
            if char in single_tokens:
                self.advance()
                self.tokens.append(Token(single_tokens[char], char, start_line, start_col))
                continue
            
            # Unknown character
            self.error(f"Unexpected character: '{char}'")
        
        # Add DEDENT tokens for remaining indentation levels
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, 0, self.line, self.column))
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        
        return self.tokens


def tokenize(source: str) -> List[Token]:
    """Convenience function to tokenize source code"""
    lexer = Lexer(source)
    return lexer.tokenize()

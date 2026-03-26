"""
KashaLang Core - The heart of the African-inspired programming language
"""

from .lexer import Lexer, Token, TokenType, tokenize
from .parser import Parser, parse
from .interpreter import Interpreter, interpret, Environment
from .ast_nodes import *
from .errors import (
    KashaError,
    KashaSyntaxError,
    KashaRuntimeError,
    KashaTypeError,
    KashaNameError,
    KashaImportError,
    format_traceback
)

__version__ = "1.0.0"
__author__ = "KashaLang Team"
__description__ = "An African-inspired programming language"

__all__ = [
    # Lexer
    'Lexer', 'Token', 'TokenType', 'tokenize',
    # Parser
    'Parser', 'parse',
    # Interpreter
    'Interpreter', 'interpret', 'Environment',
    # AST Nodes
    'ASTNode', 'NumberLiteral', 'StringLiteral', 'BooleanLiteral', 'NullLiteral',
    'ListLiteral', 'DictLiteral', 'Identifier', 'BinaryOp', 'UnaryOp',
    'Assignment', 'IndexAccess', 'PropertyAccess', 'FunctionCall',
    'ExpressionStatement', 'VariableDeclaration', 'Block', 'IfStatement',
    'WhileLoop', 'ForLoop', 'RangeLoop', 'ReturnStatement', 'BreakStatement',
    'ContinueStatement', 'PrintStatement', 'InputStatement', 'Parameter',
    'FunctionDefinition', 'Program', 'ImportStatement', 'ExportStatement',
    'print_ast',
    # Errors
    'KashaError', 'KashaSyntaxError', 'KashaRuntimeError', 'KashaTypeError',
    'KashaNameError', 'KashaImportError', 'format_traceback',
]

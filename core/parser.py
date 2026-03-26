"""
KashaLang Parser - Converts tokens into an Abstract Syntax Tree (AST)
Uses recursive descent parsing with operator precedence
"""

from typing import List, Optional
from .lexer import Token, TokenType
from .ast_nodes import *
from .errors import KashaSyntaxError


class Parser:
    """Recursive descent parser for KashaLang"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.indent_level = 0
    
    def peek(self, offset: int = 0) -> Token:
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[pos]
    
    def advance(self) -> Token:
        token = self.peek()
        self.pos += 1
        return token
    
    def expect(self, token_type: TokenType, message: str = None) -> Token:
        token = self.peek()
        if token.type != token_type:
            msg = message or f"Expected {token_type.name}, got {token.type.name}"
            raise KashaSyntaxError(msg, token.line, token.column)
        return self.advance()
    
    def match(self, *types: TokenType) -> bool:
        return self.peek().type in types
    
    def match_advance(self, *types: TokenType) -> Optional[Token]:
        if self.match(*types):
            return self.advance()
        return None
    
    def skip_newlines(self):
        """Skip newline tokens"""
        while self.match(TokenType.NEWLINE):
            self.advance()
    
    def parse(self) -> Program:
        """Parse the entire program"""
        statements = []
        
        while not self.match(TokenType.EOF):
            self.skip_newlines()
            if self.match(TokenType.EOF):
                break
            
            # Handle indentation
            if self.match(TokenType.INDENT):
                self.advance()
                continue
            if self.match(TokenType.DEDENT):
                self.advance()
                continue
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        return Program(statements, 1, 1)
    
    def parse_statement(self) -> Optional[ASTNode]:
        """Parse a single statement"""
        self.skip_newlines()
        
        if self.match(TokenType.EOF, TokenType.DEDENT, TokenType.RBRACE):
            return None
        
        # Handle indentation
        if self.match(TokenType.INDENT):
            self.advance()
            return self.parse_statement()
        
        token = self.peek()
        
        # Variable declaration: shyiramo x = 5
        if self.match(TokenType.SHYIRAMO):
            return self.parse_variable_declaration()
        
        # If statement: niba condition { ... }
        if self.match(TokenType.NIBA):
            return self.parse_if_statement()
        
        # While loop: igihe condition { ... }
        if self.match(TokenType.IGIHE):
            return self.parse_while_loop()
        
        # For loop: subiramo x in iterable { ... }
        if self.match(TokenType.SUBIRAMO):
            return self.parse_for_loop()
        
        # Range loop: kugeza i from start to end [step step] { ... }
        if self.match(TokenType.KUGEZA):
            return self.parse_range_loop()
        
        # Function definition: fata name(params) { ... }
        if self.match(TokenType.FATA):
            return self.parse_function_definition()
        
        # Return statement: subiza value
        if self.match(TokenType.SUBIZA):
            return self.parse_return_statement()
        
        # Break statement: kubera
        if self.match(TokenType.KUBERA):
            return self.parse_break_statement()
        
        # Continue statement: komeza
        if self.match(TokenType.KOMEZA):
            return self.parse_continue_statement()
        
        # Print statement: vuga expr
        if self.match(TokenType.VUGA):
            return self.parse_print_statement()
        
        # Input statement: injiza [prompt]
        if self.match(TokenType.INJIZA):
            return self.parse_input_statement()
        
        # Block statement
        if self.match(TokenType.LBRACE):
            return self.parse_block()
        
        # Expression statement
        return self.parse_expression_statement()
    
    def parse_variable_declaration(self) -> VariableDeclaration:
        """Parse variable declaration: shyiramo name = value"""
        token = self.advance()  # consume 'shyiramo'
        line, col = token.line, token.column
        
        name_token = self.expect(TokenType.IDENTIFIER, "Expected variable name")
        name = name_token.value
        
        self.expect(TokenType.ASSIGN, "Expected '=' after variable name")
        
        value = self.parse_expression()
        
        return VariableDeclaration(name, value, line, col)
    
    def parse_if_statement(self) -> IfStatement:
        """Parse if statement: niba condition { ... } [nanone { ... }]"""
        token = self.advance()  # consume 'niba'
        line, col = token.line, token.column
        
        condition = self.parse_expression()
        
        # Handle both brace and indent-based blocks
        if self.match(TokenType.LBRACE):
            then_block = self.parse_block()
        else:
            then_block = self.parse_indented_block()
        
        else_block = None
        if self.match(TokenType.NANONE):
            self.advance()  # consume 'nanone'
            if self.match(TokenType.LBRACE):
                else_block = self.parse_block()
            else:
                else_block = self.parse_indented_block()
        
        return IfStatement(condition, then_block, else_block, line, col)
    
    def parse_while_loop(self) -> WhileLoop:
        """Parse while loop: igihe condition { ... }"""
        token = self.advance()  # consume 'igihe'
        line, col = token.line, token.column
        
        condition = self.parse_expression()
        
        if self.match(TokenType.LBRACE):
            body = self.parse_block()
        else:
            body = self.parse_indented_block()
        
        return WhileLoop(condition, body, line, col)
    
    def parse_for_loop(self) -> ForLoop:
        """Parse for-in loop: subiramo var in iterable { ... }"""
        token = self.advance()  # consume 'subiramo'
        line, col = token.line, token.column
        
        var_token = self.expect(TokenType.IDENTIFIER, "Expected loop variable")
        variable = var_token.value
        
        # Expect 'in' keyword (we'll use identifier 'in' or just skip it)
        if self.peek().value == 'in':
            self.advance()
        
        iterable = self.parse_expression()
        
        if self.match(TokenType.LBRACE):
            body = self.parse_block()
        else:
            body = self.parse_indented_block()
        
        return ForLoop(variable, iterable, body, line, col)
    
    def parse_range_loop(self) -> RangeLoop:
        """Parse range loop: kugeza i from start to end [step step] { ... }"""
        token = self.advance()  # consume 'kugeza'
        line, col = token.line, token.column
        
        var_token = self.expect(TokenType.IDENTIFIER, "Expected loop variable")
        variable = var_token.value
        
        # Support: kugeza i from 0 to 10 step 2
        # Or: kugeza i = 0 to 10
        if self.match(TokenType.ASSIGN):
            self.advance()
            start = self.parse_expression()
        elif self.peek().value in ('from', 'kuva'):
            self.advance()
            start = self.parse_expression()
        else:
            start = NumberLiteral(0, line, col)
        
        # Expect 'to' or 'kugeza'
        if self.peek().value in ('to', 'kugeza', 'gushika'):
            self.advance()
        
        end = self.parse_expression()
        
        step = None
        if self.peek().value in ('step', 'intambwe'):
            self.advance()
            step = self.parse_expression()
        
        if self.match(TokenType.LBRACE):
            body = self.parse_block()
        else:
            body = self.parse_indented_block()
        
        return RangeLoop(variable, start, end, step, body, line, col)
    
    def parse_function_definition(self) -> FunctionDefinition:
        """Parse function definition: fata name(params) { ... }"""
        token = self.advance()  # consume 'fata'
        line, col = token.line, token.column
        
        name_token = self.expect(TokenType.IDENTIFIER, "Expected function name")
        name = name_token.value
        
        self.expect(TokenType.LPAREN, "Expected '(' after function name")
        
        parameters = []
        if not self.match(TokenType.RPAREN):
            while True:
                param_token = self.expect(TokenType.IDENTIFIER, "Expected parameter name")
                param_name = param_token.value
                default_value = None
                
                if self.match(TokenType.ASSIGN):
                    self.advance()
                    default_value = self.parse_expression()
                
                parameters.append(Parameter(param_name, default_value, param_token.line, param_token.column))
                
                if not self.match(TokenType.COMMA):
                    break
                self.advance()  # consume ','
        
        self.expect(TokenType.RPAREN, "Expected ')' after parameters")
        
        if self.match(TokenType.LBRACE):
            body = self.parse_block()
        else:
            body = self.parse_indented_block()
        
        return FunctionDefinition(name, parameters, body, line, col)
    
    def parse_block(self) -> Block:
        """Parse a brace-delimited block: { ... }"""
        token = self.advance()  # consume '{'
        line, col = token.line, token.column
        
        statements = []
        self.skip_newlines()
        
        # Skip any INDENT at the beginning of the block
        if self.match(TokenType.INDENT):
            self.advance()
        
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            # Also exit on DEDENT followed by RBRACE (for indented brace blocks)
            if self.match(TokenType.DEDENT):
                self.advance()
                if self.match(TokenType.RBRACE):
                    break
                continue
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE, "Expected '}' to close block")
        
        return Block(statements, line, col)
    
    def parse_indented_block(self) -> Block:
        """Parse an indentation-based block"""
        line, col = self.peek().line, self.peek().column
        
        self.expect(TokenType.COLON, "Expected ':' to start block")
        self.skip_newlines()
        self.expect(TokenType.INDENT, "Expected indented block")
        
        statements = []
        while not self.match(TokenType.DEDENT, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        if self.match(TokenType.DEDENT):
            self.advance()
        
        return Block(statements, line, col)
    
    def parse_return_statement(self) -> ReturnStatement:
        """Parse return statement: subiza [value]"""
        token = self.advance()  # consume 'subiza'
        line, col = token.line, token.column
        
        value = None
        if not self.match(TokenType.NEWLINE, TokenType.EOF, TokenType.DEDENT, TokenType.RBRACE):
            value = self.parse_expression()
        
        return ReturnStatement(value, line, col)
    
    def parse_break_statement(self) -> BreakStatement:
        """Parse break statement: kubera"""
        token = self.advance()  # consume 'kubera'
        return BreakStatement(token.line, token.column)
    
    def parse_continue_statement(self) -> ContinueStatement:
        """Parse continue statement: komeza"""
        token = self.advance()  # consume 'komeza'
        return ContinueStatement(token.line, token.column)
    
    def parse_print_statement(self) -> PrintStatement:
        """Parse print statement: vuga expr1, expr2, ..."""
        token = self.advance()  # consume 'vuga'
        line, col = token.line, token.column
        
        expressions = []
        
        # Allow print without arguments (prints empty line)
        if self.match(TokenType.NEWLINE, TokenType.EOF, TokenType.DEDENT, TokenType.RBRACE):
            return PrintStatement([], line, col)
        
        while True:
            expr = self.parse_expression()
            expressions.append(expr)
            
            if not self.match(TokenType.COMMA):
                break
            self.advance()  # consume ','
        
        return PrintStatement(expressions, line, col)
    
    def parse_input_statement(self) -> InputStatement:
        """Parse input statement: injiza [prompt]"""
        token = self.advance()  # consume 'injiza'
        line, col = token.line, token.column
        
        prompt = None
        if not self.match(TokenType.NEWLINE, TokenType.EOF, TokenType.DEDENT, TokenType.RBRACE):
            prompt = self.parse_expression()
        
        return InputStatement(prompt, line, col)
    
    def parse_expression_statement(self) -> ExpressionStatement:
        """Parse an expression as a statement"""
        expr = self.parse_expression()
        return ExpressionStatement(expr, expr.line if hasattr(expr, 'line') else 0, 
                                   expr.column if hasattr(expr, 'column') else 0)
    
    # ==================== Expression Parsing ====================
    
    def parse_expression(self) -> ASTNode:
        """Parse an expression with lowest precedence"""
        return self.parse_assignment()
    
    def parse_assignment(self) -> ASTNode:
        """Parse assignment: identifier = expression"""
        expr = self.parse_or()
        
        if self.match(TokenType.ASSIGN):
            if isinstance(expr, Identifier):
                self.advance()  # consume '='
                value = self.parse_assignment()
                return Assignment(expr.name, value, expr.line, expr.column)
            else:
                raise KashaSyntaxError("Invalid assignment target", expr.line, expr.column)
        
        return expr
    
    def parse_or(self) -> ASTNode:
        """Parse OR expression"""
        left = self.parse_and()
        
        while self.match(TokenType.CYANGWA):
            op = self.advance().value
            right = self.parse_and()
            left = BinaryOp(left, op, right, left.line, left.column)
        
        return left
    
    def parse_and(self) -> ASTNode:
        """Parse AND expression"""
        left = self.parse_equality()
        
        while self.match(TokenType.KANDI):
            op = self.advance().value
            right = self.parse_equality()
            left = BinaryOp(left, op, right, left.line, left.column)
        
        return left
    
    def parse_equality(self) -> ASTNode:
        """Parse equality expression: ==, !="""
        left = self.parse_comparison()
        
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self.advance().value
            right = self.parse_comparison()
            left = BinaryOp(left, op, right, left.line, left.column)
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        """Parse comparison expression: <, >, <=, >="""
        left = self.parse_additive()
        
        while self.match(TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op = self.advance().value
            right = self.parse_additive()
            left = BinaryOp(left, op, right, left.line, left.column)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        """Parse additive expression: +, -"""
        left = self.parse_multiplicative()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right, left.line, left.column)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        """Parse multiplicative expression: *, /, %"""
        left = self.parse_power()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance().value
            right = self.parse_power()
            left = BinaryOp(left, op, right, left.line, left.column)
        
        return left
    
    def parse_power(self) -> ASTNode:
        """Parse power expression: **"""
        left = self.parse_unary()
        
        if self.match(TokenType.POWER):
            op = self.advance().value
            right = self.parse_power()  # Right associative
            left = BinaryOp(left, op, right, left.line, left.column)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """Parse unary expression: -, not"""
        if self.match(TokenType.MINUS, TokenType.SIYO):
            op = self.advance().value
            operand = self.parse_unary()
            return UnaryOp(op, operand, operand.line, operand.column)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ASTNode:
        """Parse postfix expression: function calls, indexing, property access"""
        left = self.parse_primary()
        
        while True:
            # Function call: name(args)
            if self.match(TokenType.LPAREN):
                left = self.parse_call(left)
            # Index access: obj[index]
            elif self.match(TokenType.LBRACKET):
                left = self.parse_index_access(left)
            # Property access: obj.property
            elif self.match(TokenType.DOT):
                left = self.parse_property_access(left)
            else:
                break
        
        return left
    
    def parse_call(self, callee: ASTNode) -> FunctionCall:
        """Parse function call"""
        line, col = self.peek().line, self.peek().column
        self.advance()  # consume '('
        
        arguments = []
        if not self.match(TokenType.RPAREN):
            while True:
                arg = self.parse_expression()
                arguments.append(arg)
                
                if not self.match(TokenType.COMMA):
                    break
                self.advance()  # consume ','
        
        self.expect(TokenType.RPAREN, "Expected ')' after arguments")
        
        return FunctionCall(callee, arguments, line, col)
    
    def parse_index_access(self, obj: ASTNode) -> IndexAccess:
        """Parse index access"""
        line, col = self.peek().line, self.peek().column
        self.advance()  # consume '['
        
        index = self.parse_expression()
        
        self.expect(TokenType.RBRACKET, "Expected ']' after index")
        
        return IndexAccess(obj, index, line, col)
    
    def parse_property_access(self, obj: ASTNode) -> PropertyAccess:
        """Parse property access"""
        line, col = self.peek().line, self.peek().column
        self.advance()  # consume '.'
        
        prop_token = self.expect(TokenType.IDENTIFIER, "Expected property name")
        
        return PropertyAccess(obj, prop_token.value, line, col)
    
    def parse_primary(self) -> ASTNode:
        """Parse primary expression: literals, identifiers, parenthesized expressions"""
        token = self.peek()
        line, col = token.line, token.column
        
        # Number literal
        if self.match(TokenType.NUMBER):
            self.advance()
            return NumberLiteral(token.value, line, col)
        
        # String literal
        if self.match(TokenType.STRING):
            self.advance()
            return StringLiteral(token.value, line, col)
        
        # Boolean literal
        if self.match(TokenType.BOOLEAN):
            self.advance()
            return BooleanLiteral(token.value, line, col)
        
        # Null literal
        if self.match(TokenType.NULL):
            self.advance()
            return NullLiteral(line, col)
        
        # List literal
        if self.match(TokenType.LBRACKET):
            return self.parse_list_literal()
        
        # Dictionary literal
        if self.match(TokenType.LBRACE):
            return self.parse_dict_literal()
        
        # Identifier
        if self.match(TokenType.IDENTIFIER):
            self.advance()
            return Identifier(token.value, line, col)
        
        # Parenthesized expression
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        raise KashaSyntaxError(f"Unexpected token: {token.type.name}", line, col)
    
    def parse_list_literal(self) -> ListLiteral:
        """Parse list literal: [elem1, elem2, ...]"""
        token = self.advance()  # consume '['
        line, col = token.line, token.column
        
        elements = []
        if not self.match(TokenType.RBRACKET):
            while True:
                elem = self.parse_expression()
                elements.append(elem)
                
                if not self.match(TokenType.COMMA):
                    break
                self.advance()  # consume ','
        
        self.expect(TokenType.RBRACKET, "Expected ']' to close list")
        
        return ListLiteral(elements, line, col)
    
    def parse_dict_literal(self) -> DictLiteral:
        """Parse dictionary literal: {key1: value1, key2: value2, ...}"""
        token = self.advance()  # consume '{'
        line, col = token.line, token.column
        
        pairs = []
        if not self.match(TokenType.RBRACE):
            while True:
                key = self.parse_expression()
                
                self.expect(TokenType.COLON, "Expected ':' after dictionary key")
                
                value = self.parse_expression()
                pairs.append((key, value))
                
                if not self.match(TokenType.COMMA):
                    break
                self.advance()  # consume ','
        
        self.expect(TokenType.RBRACE, "Expected '}' to close dictionary")
        
        return DictLiteral(pairs, line, col)


def parse(tokens: List[Token]) -> Program:
    """Convenience function to parse tokens into an AST"""
    parser = Parser(tokens)
    return parser.parse()

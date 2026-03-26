"""
KashaLang AST Nodes - Abstract Syntax Tree representation
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from enum import Enum, auto


class ASTNode:
    """Base class for all AST nodes"""
    pass


# ==================== Literals ====================

@dataclass
class NumberLiteral(ASTNode):
    value: float
    line: int = 0
    column: int = 0


@dataclass
class StringLiteral(ASTNode):
    value: str
    line: int = 0
    column: int = 0


@dataclass
class BooleanLiteral(ASTNode):
    value: bool
    line: int = 0
    column: int = 0


@dataclass
class NullLiteral(ASTNode):
    line: int = 0
    column: int = 0


@dataclass
class ListLiteral(ASTNode):
    elements: List[ASTNode]
    line: int = 0
    column: int = 0


@dataclass
class DictLiteral(ASTNode):
    pairs: List[tuple]  # List of (key, value) tuples
    line: int = 0
    column: int = 0


# ==================== Expressions ====================

@dataclass
class Identifier(ASTNode):
    name: str
    line: int = 0
    column: int = 0


@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str  # +, -, *, /, %, ==, !=, <, >, <=, >=, and, or
    right: ASTNode
    line: int = 0
    column: int = 0


@dataclass
class UnaryOp(ASTNode):
    operator: str  # -, not
    operand: ASTNode
    line: int = 0
    column: int = 0


@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode
    line: int = 0
    column: int = 0


@dataclass
class IndexAccess(ASTNode):
    object: ASTNode
    index: ASTNode
    line: int = 0
    column: int = 0


@dataclass
class PropertyAccess(ASTNode):
    object: ASTNode
    property: str
    line: int = 0
    column: int = 0


@dataclass
class FunctionCall(ASTNode):
    name: ASTNode  # Can be Identifier or PropertyAccess
    arguments: List[ASTNode]
    line: int = 0
    column: int = 0


@dataclass
class TernaryOp(ASTNode):
    condition: ASTNode
    true_expr: ASTNode
    false_expr: ASTNode
    line: int = 0
    column: int = 0


# ==================== Statements ====================

@dataclass
class ExpressionStatement(ASTNode):
    expression: ASTNode
    line: int = 0
    column: int = 0


@dataclass
class VariableDeclaration(ASTNode):
    name: str
    value: ASTNode
    line: int = 0
    column: int = 0


@dataclass
class Block(ASTNode):
    statements: List[ASTNode]
    line: int = 0
    column: int = 0


@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_block: Block
    else_block: Optional[Block] = None
    line: int = 0
    column: int = 0


@dataclass
class WhileLoop(ASTNode):
    condition: ASTNode
    body: Block
    line: int = 0
    column: int = 0


@dataclass
class ForLoop(ASTNode):
    variable: str
    iterable: ASTNode
    body: Block
    line: int = 0
    column: int = 0


@dataclass
class RangeLoop(ASTNode):
    """For i in range(start, end, step)"""
    variable: str
    start: ASTNode
    end: ASTNode
    step: Optional[ASTNode] = None
    body: Block = field(default_factory=lambda: Block([]))
    line: int = 0
    column: int = 0


@dataclass
class ReturnStatement(ASTNode):
    value: Optional[ASTNode] = None
    line: int = 0
    column: int = 0


@dataclass
class BreakStatement(ASTNode):
    line: int = 0
    column: int = 0


@dataclass
class ContinueStatement(ASTNode):
    line: int = 0
    column: int = 0


@dataclass
class PrintStatement(ASTNode):
    expressions: List[ASTNode]
    line: int = 0
    column: int = 0


@dataclass
class InputStatement(ASTNode):
    prompt: Optional[ASTNode] = None
    line: int = 0
    column: int = 0


# ==================== Functions ====================

@dataclass
class Parameter(ASTNode):
    name: str
    default_value: Optional[ASTNode] = None
    line: int = 0
    column: int = 0


@dataclass
class FunctionDefinition(ASTNode):
    name: str
    parameters: List[Parameter]
    body: Block
    line: int = 0
    column: int = 0


# ==================== Program ====================

@dataclass
class Program(ASTNode):
    statements: List[ASTNode]
    line: int = 0
    column: int = 0


# ==================== Module System ====================

@dataclass
class ImportStatement(ASTNode):
    module: str
    aliases: Dict[str, str] = field(default_factory=dict)
    line: int = 0
    column: int = 0


@dataclass
class ExportStatement(ASTNode):
    names: List[str]
    line: int = 0
    column: int = 0


# ==================== Utility Functions ====================

def print_ast(node: ASTNode, indent: int = 0) -> str:
    """Pretty print an AST node for debugging"""
    spaces = "  " * indent
    result = []
    
    if isinstance(node, Program):
        result.append(f"{spaces}Program:")
        for stmt in node.statements:
            result.append(print_ast(stmt, indent + 1))
    
    elif isinstance(node, NumberLiteral):
        result.append(f"{spaces}NumberLiteral({node.value})")
    
    elif isinstance(node, StringLiteral):
        result.append(f"{spaces}StringLiteral({node.value!r})")
    
    elif isinstance(node, BooleanLiteral):
        result.append(f"{spaces}BooleanLiteral({node.value})")
    
    elif isinstance(node, NullLiteral):
        result.append(f"{spaces}NullLiteral")
    
    elif isinstance(node, Identifier):
        result.append(f"{spaces}Identifier({node.name})")
    
    elif isinstance(node, BinaryOp):
        result.append(f"{spaces}BinaryOp({node.operator}):")
        result.append(print_ast(node.left, indent + 1))
        result.append(print_ast(node.right, indent + 1))
    
    elif isinstance(node, UnaryOp):
        result.append(f"{spaces}UnaryOp({node.operator}):")
        result.append(print_ast(node.operand, indent + 1))
    
    elif isinstance(node, VariableDeclaration):
        result.append(f"{spaces}VariableDeclaration({node.name}):")
        result.append(print_ast(node.value, indent + 1))
    
    elif isinstance(node, Assignment):
        result.append(f"{spaces}Assignment({node.name}):")
        result.append(print_ast(node.value, indent + 1))
    
    elif isinstance(node, FunctionCall):
        result.append(f"{spaces}FunctionCall:")
        result.append(print_ast(node.name, indent + 1))
        for arg in node.arguments:
            result.append(print_ast(arg, indent + 1))
    
    elif isinstance(node, IfStatement):
        result.append(f"{spaces}IfStatement:")
        result.append(f"{spaces}  Condition:")
        result.append(print_ast(node.condition, indent + 2))
        result.append(f"{spaces}  Then:")
        result.append(print_ast(node.then_block, indent + 2))
        if node.else_block:
            result.append(f"{spaces}  Else:")
            result.append(print_ast(node.else_block, indent + 2))
    
    elif isinstance(node, WhileLoop):
        result.append(f"{spaces}WhileLoop:")
        result.append(f"{spaces}  Condition:")
        result.append(print_ast(node.condition, indent + 2))
        result.append(f"{spaces}  Body:")
        result.append(print_ast(node.body, indent + 2))
    
    elif isinstance(node, ForLoop):
        result.append(f"{spaces}ForLoop({node.variable}):")
        result.append(f"{spaces}  Iterable:")
        result.append(print_ast(node.iterable, indent + 2))
        result.append(f"{spaces}  Body:")
        result.append(print_ast(node.body, indent + 2))
    
    elif isinstance(node, RangeLoop):
        result.append(f"{spaces}RangeLoop({node.variable}):")
        result.append(f"{spaces}  Start:")
        result.append(print_ast(node.start, indent + 2))
        result.append(f"{spaces}  End:")
        result.append(print_ast(node.end, indent + 2))
        if node.step:
            result.append(f"{spaces}  Step:")
            result.append(print_ast(node.step, indent + 2))
        result.append(f"{spaces}  Body:")
        result.append(print_ast(node.body, indent + 2))
    
    elif isinstance(node, FunctionDefinition):
        result.append(f"{spaces}FunctionDefinition({node.name}):")
        result.append(f"{spaces}  Parameters: {[p.name for p in node.parameters]}")
        result.append(f"{spaces}  Body:")
        result.append(print_ast(node.body, indent + 2))
    
    elif isinstance(node, ReturnStatement):
        result.append(f"{spaces}ReturnStatement:")
        if node.value:
            result.append(print_ast(node.value, indent + 1))
    
    elif isinstance(node, BreakStatement):
        result.append(f"{spaces}BreakStatement")
    
    elif isinstance(node, ContinueStatement):
        result.append(f"{spaces}ContinueStatement")
    
    elif isinstance(node, PrintStatement):
        result.append(f"{spaces}PrintStatement:")
        for expr in node.expressions:
            result.append(print_ast(expr, indent + 1))
    
    elif isinstance(node, Block):
        result.append(f"{spaces}Block:")
        for stmt in node.statements:
            result.append(print_ast(stmt, indent + 1))
    
    elif isinstance(node, ListLiteral):
        result.append(f"{spaces}ListLiteral:")
        for elem in node.elements:
            result.append(print_ast(elem, indent + 1))
    
    elif isinstance(node, DictLiteral):
        result.append(f"{spaces}DictLiteral:")
        for key, value in node.pairs:
            result.append(f"{spaces}  Key:")
            result.append(print_ast(key, indent + 2))
            result.append(f"{spaces}  Value:")
            result.append(print_ast(value, indent + 2))
    
    elif isinstance(node, IndexAccess):
        result.append(f"{spaces}IndexAccess:")
        result.append(f"{spaces}  Object:")
        result.append(print_ast(node.object, indent + 2))
        result.append(f"{spaces}  Index:")
        result.append(print_ast(node.index, indent + 2))
    
    elif isinstance(node, PropertyAccess):
        result.append(f"{spaces}PropertyAccess({node.property}):")
        result.append(print_ast(node.object, indent + 1))
    
    else:
        result.append(f"{spaces}Unknown({type(node).__name__})")
    
    return "\n".join(result)

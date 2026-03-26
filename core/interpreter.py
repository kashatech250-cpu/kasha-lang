"""
KashaLang Interpreter - Executes the Abstract Syntax Tree (AST)
"""

from typing import Any, Dict, List, Optional, Callable
from .ast_nodes import *
from .errors import KashaRuntimeError, KashaTypeError, KashaNameError


class ReturnValue(Exception):
    """Exception used to return values from functions"""
    def __init__(self, value: Any):
        self.value = value


class BreakLoop(Exception):
    """Exception used to break out of loops"""
    pass


class ContinueLoop(Exception):
    """Exception used to continue to next loop iteration"""
    pass


class Environment:
    """Variable scope environment"""
    
    def __init__(self, parent: Optional['Environment'] = None):
        self.variables: Dict[str, Any] = {}
        self.parent = parent
    
    def define(self, name: str, value: Any):
        """Define a variable in this environment"""
        self.variables[name] = value
    
    def get(self, name: str) -> Any:
        """Get a variable value, searching up the scope chain"""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise KashaNameError(f"Variable '{name}' is not defined", 0, 0, 
                            suggestion=f"Did you forget to declare it with 'shyiramo {name} = ...'?")
    
    def set(self, name: str, value: Any):
        """Set a variable value, searching up the scope chain"""
        if name in self.variables:
            self.variables[name] = value
            return
        if self.parent:
            self.parent.set(name, value)
            return
        raise KashaNameError(f"Variable '{name}' is not defined", 0, 0)


class KashaFunction:
    """User-defined function"""
    
    def __init__(self, definition: FunctionDefinition, closure: Environment):
        self.definition = definition
        self.closure = closure
        self.name = definition.name
    
    def call(self, interpreter: 'Interpreter', arguments: List[Any]) -> Any:
        """Execute the function with given arguments"""
        # Create new environment for function scope
        env = Environment(self.closure)
        
        # Bind parameters
        params = self.definition.parameters
        
        if len(arguments) > len(params):
            raise KashaRuntimeError(
                f"Function '{self.name}' expects {len(params)} arguments, got {len(arguments)}",
                self.definition.line, self.definition.column
            )
        
        for i, param in enumerate(params):
            if i < len(arguments):
                env.define(param.name, arguments[i])
            elif param.default_value:
                default_val = interpreter.evaluate(param.default_value)
                env.define(param.name, default_val)
            else:
                raise KashaRuntimeError(
                    f"Missing required argument '{param.name}' for function '{self.name}'",
                    self.definition.line, self.definition.column
                )
        
        # Execute function body
        try:
            interpreter.execute_block(self.definition.body.statements, env)
        except ReturnValue as ret:
            return ret.value
        
        return None
    
    def __repr__(self):
        return f"<function {self.name}>"


class Interpreter:
    """KashaLang Interpreter - Executes AST nodes"""
    
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.output_buffer: List[str] = []
        self.input_handler: Callable[[str], str] = input
        self.output_handler: Callable[[str], None] = print
        
        # Initialize with standard library
        self._init_builtins()
    
    def _init_builtins(self):
        """Initialize built-in functions"""
        # Type functions
        self.globals.define('umubare', self._builtin_number)
        self.globals.define('number', self._builtin_number)
        self.globals.define('umutwe', self._builtin_string)
        self.globals.define('string', self._builtin_string)
        self.globals.define('urutonde', self._builtin_list)
        self.globals.define('list', self._builtin_list)
        self.globals.define('ikigondo', self._builtin_dict)
        self.globals.define('dict', self._builtin_dict)
        self.globals.define('ubwoko', self._builtin_type)
        self.globals.define('type', self._builtin_type)
        
        # Math functions
        self.globals.define('sin', self._builtin_sin)
        self.globals.define('kos', self._builtin_cos)
        self.globals.define('tan', self._builtin_tan)
        self.globals.define('muzani', self._builtin_sqrt)
        self.globals.define('sqrt', self._builtin_sqrt)
        self.globals.define('absolute', self._builtin_abs)
        self.globals.define('abs', self._builtin_abs)
        self.globals.define('round', self._builtin_round)
        self.globals.define('hejuru', self._builtin_ceil)
        self.globals.define('ceil', self._builtin_ceil)
        self.globals.define('hasi', self._builtin_floor)
        self.globals.define('floor', self._builtin_floor)
        self.globals.define('min', self._builtin_min)
        self.globals.define('max', self._builtin_max)
        self.globals.define('sum', self._builtin_sum)
        self.globals.define('random', self._builtin_random)
        
        # String functions
        self.globals.define('uburebure', self._builtin_len)
        self.globals.define('length', self._builtin_len)
        self.globals.define('len', self._builtin_len)
        self.globals.define('gabanya', self._builtin_split)
        self.globals.define('split', self._builtin_split)
        self.globals.define('huza', self._builtin_join)
        self.globals.define('join', self._builtin_join)
        self.globals.define('hejuru_str', self._builtin_upper)
        self.globals.define('upper', self._builtin_upper)
        self.globals.define('hasi_str', self._builtin_lower)
        self.globals.define('lower', self._builtin_lower)
        self.globals.define('gusimbuza', self._builtin_replace)
        self.globals.define('replace', self._builtin_replace)
        self.globals.define('igice', self._builtin_slice)
        self.globals.define('slice', self._builtin_slice)
        
        # List functions
        self.globals.define('ongera', self._builtin_append)
        self.globals.define('append', self._builtin_append)
        self.globals.define('kuramo', self._builtin_remove)
        self.globals.define('remove', self._builtin_remove)
        self.globals.define('shiramo', self._builtin_insert)
        self.globals.define('insert', self._builtin_insert)
        self.globals.define('urutonde', self._builtin_sort)
        self.globals.define('sort', self._builtin_sort)
        self.globals.define('birahura', self._builtin_reverse)
        self.globals.define('reverse', self._builtin_reverse)
        self.globals.define('index', self._builtin_index)
        
        # Utility functions
        self.globals.define('range', self._builtin_range)
        self.globals.define('enumerate', self._builtin_enumerate)
        self.globals.define('zip', self._builtin_zip)
        self.globals.define('map', self._builtin_map)
        self.globals.define('filter', self._builtin_filter)
    
    # ==================== Built-in Functions ====================
    
    def _builtin_number(self, x: Any) -> float:
        try:
            return float(x)
        except (ValueError, TypeError):
            raise KashaTypeError(f"Cannot convert '{x}' to number", 0, 0)
    
    def _builtin_string(self, x: Any) -> str:
        return str(x)
    
    def _builtin_list(self, x: Any = None) -> List:
        if x is None:
            return []
        if hasattr(x, '__iter__'):
            return list(x)
        return [x]
    
    def _builtin_dict(self, **kwargs) -> Dict:
        return dict(kwargs)
    
    def _builtin_type(self, x: Any) -> str:
        if x is None:
            return "taruza"
        if isinstance(x, bool):
            return "ukuri"
        if isinstance(x, (int, float)):
            return "umubare"
        if isinstance(x, str):
            return "umutwe"
        if isinstance(x, list):
            return "urutonde"
        if isinstance(x, dict):
            return "ikigondo"
        if callable(x) or isinstance(x, KashaFunction):
            return "fata"
        return type(x).__name__
    
    def _builtin_len(self, x: Any) -> int:
        try:
            return len(x)
        except TypeError:
            raise KashaTypeError(f"Object of type '{type(x).__name__}' has no length", 0, 0)
    
    def _builtin_split(self, s: str, sep: str = None) -> List[str]:
        return s.split(sep)
    
    def _builtin_join(self, items: List, sep: str = "") -> str:
        return sep.join(str(item) for item in items)
    
    def _builtin_upper(self, s: str) -> str:
        return s.upper()
    
    def _builtin_lower(self, s: str) -> str:
        return s.lower()
    
    def _builtin_replace(self, s: str, old: str, new: str) -> str:
        return s.replace(old, new)
    
    def _builtin_slice(self, s: str, start: int, end: int = None) -> str:
        return s[start:end]
    
    def _builtin_append(self, lst: List, item: Any) -> List:
        lst.append(item)
        return lst
    
    def _builtin_remove(self, lst: List, item: Any) -> List:
        lst.remove(item)
        return lst
    
    def _builtin_insert(self, lst: List, index: int, item: Any) -> List:
        lst.insert(index, item)
        return lst
    
    def _builtin_sort(self, lst: List, reverse: bool = False) -> List:
        lst.sort(reverse=reverse)
        return lst
    
    def _builtin_reverse(self, lst: List) -> List:
        lst.reverse()
        return lst
    
    def _builtin_index(self, lst: List, item: Any) -> int:
        return lst.index(item)
    
    def _builtin_range(self, start: int, end: int = None, step: int = 1) -> range:
        if end is None:
            return range(start)
        return range(start, end, step)
    
    def _builtin_enumerate(self, iterable: List, start: int = 0) -> enumerate:
        return enumerate(iterable, start)
    
    def _builtin_zip(self, *iterables) -> zip:
        return zip(*iterables)
    
    def _builtin_map(self, func: Callable, iterable: List) -> List:
        return list(map(func, iterable))
    
    def _builtin_filter(self, func: Callable, iterable: List) -> List:
        return list(filter(func, iterable))
    
    def _builtin_sin(self, x: float) -> float:
        import math
        return math.sin(x)
    
    def _builtin_cos(self, x: float) -> float:
        import math
        return math.cos(x)
    
    def _builtin_tan(self, x: float) -> float:
        import math
        return math.tan(x)
    
    def _builtin_sqrt(self, x: float) -> float:
        import math
        return math.sqrt(x)
    
    def _builtin_abs(self, x: float) -> float:
        return abs(x)
    
    def _builtin_round(self, x: float, ndigits: int = 0) -> float:
        return round(x, ndigits)
    
    def _builtin_ceil(self, x: float) -> int:
        import math
        return math.ceil(x)
    
    def _builtin_floor(self, x: float) -> int:
        import math
        return math.floor(x)
    
    def _builtin_min(self, *args) -> Any:
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            return min(args[0])
        return min(args)
    
    def _builtin_max(self, *args) -> Any:
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            return max(args[0])
        return max(args)
    
    def _builtin_sum(self, iterable: List, start: Any = 0) -> Any:
        return sum(iterable, start)
    
    def _builtin_random(self, a: float = 0, b: float = 1) -> float:
        import random
        return random.uniform(a, b)
    
    # ==================== Execution Methods ====================
    
    def interpret(self, program: Program) -> Any:
        """Execute a program"""
        result = None
        for statement in program.statements:
            result = self.execute(statement)
        return result
    
    def execute(self, node: ASTNode) -> Any:
        """Execute a statement node"""
        method_name = f'execute_{type(node).__name__}'
        method = getattr(self, method_name, self._execute_unknown)
        return method(node)
    
    def evaluate(self, node: ASTNode) -> Any:
        """Evaluate an expression node"""
        method_name = f'eval_{type(node).__name__}'
        method = getattr(self, method_name, self._eval_unknown)
        return method(node)
    
    def execute_block(self, statements: List[ASTNode], environment: Environment):
        """Execute a block of statements in a new environment"""
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
    
    def _execute_unknown(self, node: ASTNode):
        raise KashaRuntimeError(f"Unknown statement type: {type(node).__name__}", 0, 0)
    
    def _eval_unknown(self, node: ASTNode):
        raise KashaRuntimeError(f"Unknown expression type: {type(node).__name__}", 0, 0)
    
    # ==================== Statement Execution ====================
    
    def execute_Program(self, node: Program):
        result = None
        for statement in node.statements:
            result = self.execute(statement)
        return result
    
    def execute_ExpressionStatement(self, node: ExpressionStatement):
        return self.evaluate(node.expression)
    
    def execute_VariableDeclaration(self, node: VariableDeclaration):
        value = self.evaluate(node.value)
        self.environment.define(node.name, value)
        return value
    
    def execute_Block(self, node: Block):
        for statement in node.statements:
            self.execute(statement)
    
    def execute_IfStatement(self, node: IfStatement):
        condition = self.evaluate(node.condition)
        if self._is_truthy(condition):
            self.execute(node.then_block)
        elif node.else_block:
            self.execute(node.else_block)
    
    def execute_WhileLoop(self, node: WhileLoop):
        try:
            while self._is_truthy(self.evaluate(node.condition)):
                try:
                    self.execute(node.body)
                except ContinueLoop:
                    continue
        except BreakLoop:
            pass
    
    def execute_ForLoop(self, node: ForLoop):
        try:
            iterable = self.evaluate(node.iterable)
            for item in iterable:
                self.environment.define(node.variable, item)
                try:
                    self.execute(node.body)
                except ContinueLoop:
                    continue
        except BreakLoop:
            pass
    
    def execute_RangeLoop(self, node: RangeLoop):
        try:
            start = self.evaluate(node.start)
            end = self.evaluate(node.end)
            step = self.evaluate(node.step) if node.step else 1
            
            for i in range(int(start), int(end), int(step)):
                self.environment.define(node.variable, i)
                try:
                    self.execute(node.body)
                except ContinueLoop:
                    continue
        except BreakLoop:
            pass
    
    def execute_FunctionDefinition(self, node: FunctionDefinition):
        func = KashaFunction(node, self.environment)
        self.environment.define(node.name, func)
        return func
    
    def execute_ReturnStatement(self, node: ReturnStatement):
        value = None
        if node.value:
            value = self.evaluate(node.value)
        raise ReturnValue(value)
    
    def execute_BreakStatement(self, node: BreakStatement):
        raise BreakLoop()
    
    def execute_ContinueStatement(self, node: ContinueStatement):
        raise ContinueLoop()
    
    def execute_PrintStatement(self, node: PrintStatement):
        values = []
        for expr in node.expressions:
            value = self.evaluate(expr)
            values.append(self._stringify(value))
        
        output = " ".join(values)
        self.output_buffer.append(output)
        self.output_handler(output)
        return output
    
    def execute_InputStatement(self, node: InputStatement):
        prompt = ""
        if node.prompt:
            prompt = self._stringify(self.evaluate(node.prompt))
        
        try:
            user_input = self.input_handler(prompt)
            # Try to convert to number if possible
            try:
                if '.' in user_input:
                    return float(user_input)
                return int(user_input)
            except ValueError:
                return user_input
        except EOFError:
            return ""
    
    # ==================== Expression Evaluation ====================
    
    def eval_NumberLiteral(self, node: NumberLiteral):
        return node.value
    
    def eval_StringLiteral(self, node: StringLiteral):
        return node.value
    
    def eval_BooleanLiteral(self, node: BooleanLiteral):
        return node.value
    
    def eval_NullLiteral(self, node: NullLiteral):
        return None
    
    def eval_Identifier(self, node: Identifier):
        return self.environment.get(node.name)
    
    def eval_BinaryOp(self, node: BinaryOp):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        
        # Arithmetic operators
        if node.operator == '+':
            if isinstance(left, str) or isinstance(right, str):
                return self._stringify(left) + self._stringify(right)
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            if right == 0:
                raise KashaRuntimeError("Division by zero", node.line, node.column)
            return left / right
        elif node.operator == '%':
            return left % right
        elif node.operator == '**':
            return left ** right
        
        # Comparison operators
        elif node.operator == '==':
            return left == right
        elif node.operator == '!=':
            return left != right
        elif node.operator == '<':
            return left < right
        elif node.operator == '>':
            return left > right
        elif node.operator == '<=':
            return left <= right
        elif node.operator == '>=':
            return left >= right
        
        # Logical operators
        elif node.operator in ('kandi', 'and'):
            return left and right
        elif node.operator in ('cyangwa', 'or'):
            return left or right
        
        raise KashaRuntimeError(f"Unknown operator: {node.operator}", node.line, node.column)
    
    def eval_UnaryOp(self, node: UnaryOp):
        operand = self.evaluate(node.operand)
        
        if node.operator == '-':
            return -operand
        elif node.operator in ('siyo', 'not'):
            return not self._is_truthy(operand)
        
        raise KashaRuntimeError(f"Unknown unary operator: {node.operator}", node.line, node.column)
    
    def eval_Assignment(self, node: Assignment):
        value = self.evaluate(node.value)
        self.environment.set(node.name, value)
        return value
    
    def eval_FunctionCall(self, node: FunctionCall):
        callee = self.evaluate(node.name)
        
        # Evaluate arguments
        arguments = [self.evaluate(arg) for arg in node.arguments]
        
        # Call the function
        if isinstance(callee, KashaFunction):
            return callee.call(self, arguments)
        elif callable(callee):
            return callee(*arguments)
        else:
            raise KashaTypeError(f"'{callee}' is not a function", node.line, node.column)
    
    def eval_IndexAccess(self, node: IndexAccess):
        obj = self.evaluate(node.object)
        index = self.evaluate(node.index)
        
        try:
            return obj[index]
        except (IndexError, KeyError, TypeError) as e:
            raise KashaRuntimeError(f"Cannot access index: {e}", node.line, node.column)
    
    def eval_PropertyAccess(self, node: PropertyAccess):
        obj = self.evaluate(node.object)
        
        # Handle different object types
        if isinstance(obj, dict):
            if node.property in obj:
                return obj[node.property]
            raise KashaNameError(f"Dictionary has no key '{node.property}'", node.line, node.column)
        
        if hasattr(obj, node.property):
            attr = getattr(obj, node.property)
            if callable(attr):
                return attr
            return attr
        
        raise KashaNameError(f"Object has no property '{node.property}'", node.line, node.column)
    
    def eval_ListLiteral(self, node: ListLiteral):
        return [self.evaluate(elem) for elem in node.elements]
    
    def eval_DictLiteral(self, node: DictLiteral):
        result = {}
        for key, value in node.pairs:
            key_val = self.evaluate(key)
            if not isinstance(key_val, (str, int, float, bool)):
                raise KashaTypeError("Dictionary keys must be strings or numbers", node.line, node.column)
            result[key_val] = self.evaluate(value)
        return result
    
    # ==================== Helper Methods ====================
    
    def _is_truthy(self, value: Any) -> bool:
        """Check if a value is truthy"""
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, (str, list, dict)):
            return len(value) > 0
        return True
    
    def _stringify(self, value: Any) -> str:
        """Convert a value to string"""
        if value is None:
            return "taruza"
        if isinstance(value, bool):
            return "ukuri" if value else "ibinya"
        if isinstance(value, float):
            # Remove trailing zeros
            s = str(value)
            if '.' in s:
                s = s.rstrip('0').rstrip('.')
            return s
        if isinstance(value, list):
            return "[" + ", ".join(self._stringify(item) for item in value) + "]"
        if isinstance(value, dict):
            items = [f"{self._stringify(k)}: {self._stringify(v)}" for k, v in value.items()]
            return "{" + ", ".join(items) + "}"
        return str(value)


def interpret(program: Program) -> tuple[Any, List[str]]:
    """Convenience function to interpret a program"""
    interpreter = Interpreter()
    result = interpreter.interpret(program)
    return result, interpreter.output_buffer

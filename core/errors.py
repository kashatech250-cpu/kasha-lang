"""
KashaLang Error Handling - Beautiful, beginner-friendly error messages
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class KashaError(Exception):
    """Base error class for KashaLang with beautiful formatting"""
    message: str
    line: int = 0
    column: int = 0
    source_line: Optional[str] = None
    suggestion: Optional[str] = None
    
    def __str__(self):
        error_box = self._format_error()
        return error_box
    
    def _format_error(self) -> str:
        """Format error with African-inspired styling"""
        lines = []
        
        # Header with African styling
        lines.append("╔" + "═" * 58 + "╗")
        lines.append("║" + " 🔥 KASHALANG ERROR ".center(58) + "║")
        lines.append("╠" + "═" * 58 + "╣")
        
        # Error type and message
        lines.append(f"║  📍 Location: Line {self.line}, Column {self.column}".ljust(59) + "║")
        lines.append("║" + " " * 58 + "║")
        
        # Message wrapped to fit
        wrapped_msg = self._wrap_text(self.message, 54)
        for i, msg_line in enumerate(wrapped_msg):
            if i == 0:
                lines.append(f"║  ❌ {msg_line}".ljust(59) + "║")
            else:
                lines.append(f"║      {msg_line}".ljust(59) + "║")
        
        # Source line if available
        if self.source_line:
            lines.append("║" + " " * 58 + "║")
            lines.append("║  📜 Code:".ljust(59) + "║")
            source_display = self.source_line.strip()[:50]
            lines.append(f"║     {source_display}".ljust(59) + "║")
            # Error pointer
            pointer = " " * (self.column + 3) + "^" * max(1, len(str(self.source_line.strip())))
            lines.append(f"║{pointer[:58]}".ljust(59) + "║")
        
        # Suggestion if available
        if self.suggestion:
            lines.append("║" + " " * 58 + "║")
            lines.append("║  💡 Suggestion:".ljust(59) + "║")
            wrapped_sugg = self._wrap_text(self.suggestion, 50)
            for sugg_line in wrapped_sugg:
                lines.append(f"║      {sugg_line}".ljust(59) + "║")
        
        # Footer
        lines.append("║" + " " * 58 + "║")
        lines.append("║  🌍 Learn more: https://kashalang.dev/docs/errors".ljust(59) + "║")
        lines.append("╚" + "═" * 58 + "╝")
        
        return "\n".join(lines)
    
    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Wrap text to specified width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= width:
                current_line += " " + word if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines if lines else [""]


class KashaSyntaxError(KashaError):
    """Syntax error with helpful suggestions"""
    pass


class KashaRuntimeError(KashaError):
    """Runtime error with context"""
    pass


class KashaTypeError(KashaError):
    """Type mismatch error"""
    pass


class KashaNameError(KashaError):
    """Undefined variable or function"""
    pass


class KashaImportError(KashaError):
    """Module/package import error"""
    pass


class KashaValidationError(KashaError):
    """Project validation error"""
    pass


def format_traceback(error: Exception, source_lines: List[str]) -> str:
    """Format a beautiful traceback"""
    lines = []
    lines.append("╔" + "═" * 68 + "╗")
    lines.append("║" + " 📚 KASHALANG TRACEBACK ".center(68) + "║")
    lines.append("╠" + "═" * 68 + "╣")
    
    if isinstance(error, KashaError):
        lines.append(f"║  📍 Line {error.line}, Column {error.column}".ljust(69) + "║")
        if error.source_line and error.line > 0 and error.line <= len(source_lines):
            lines.append("║" + " " * 68 + "║")
            lines.append("║  📜 Source:".ljust(69) + "║")
            
            # Show context lines
            start = max(0, error.line - 3)
            end = min(len(source_lines), error.line + 2)
            
            for i in range(start, end):
                line_num = i + 1
                prefix = ">>> " if line_num == error.line else "    "
                code_line = source_lines[i].rstrip()[:55]
                lines.append(f"║  {prefix}{line_num:3d} │ {code_line}".ljust(69) + "║")
    
    lines.append("║" + " " * 68 + "║")
    lines.append(f"║  🔥 {type(error).__name__}: {str(error)[:50]}".ljust(69) + "║")
    lines.append("╚" + "═" * 68 + "╝")
    
    return "\n".join(lines)

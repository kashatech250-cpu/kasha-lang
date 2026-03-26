#!/usr/bin/env python3
"""
KashaLang CLI - Command Line Interface for the African-inspired programming language
"""

import argparse
import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import (
    tokenize, parse, interpret, 
    KashaError, KashaSyntaxError, KashaRuntimeError,
    format_traceback, print_ast
)

# ASCII Art Logo
KASHA_LOGO = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██╗  ██╗ █████╗ ███████╗██╗  ██╗ █████╗ ██╗      ██████╗   ║
║   ██║ ██╔╝██╔══██╗██╔════╝██║  ██║██╔══██╗██║     ██╔════╝   ║
║   █████╔╝ ███████║███████╗███████║███████║██║     ██║  ███╗  ║
║   ██╔═██╗ ██╔══██║╚════██║██╔══██║██╔══██║██║     ██║   ██║  ║
║   ██║  ██╗██║  ██║███████║██║  ██║██║  ██║███████╗╚██████╔╝  ║
║   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝   ║
║                                                              ║
║              🌍 The African Programming Language 🌍           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

VERSION = "1.0.0"


class KashaCLI:
    """KashaLang Command Line Interface"""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser with all subcommands"""
        parser = argparse.ArgumentParser(
            prog='kasha',
            description='KashaLang - The African-inspired programming language',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  kasha run hello.kasha          # Run a KashaLang program
  kasha init my-app              # Create a new KashaLang project
  kasha install kasha-web        # Install a package
  kasha repl                     # Start interactive shell
  kasha export web hello.kasha   # Export to HTML/CSS/JS
  kasha version                  # Show version

For more help: https://kashalang.dev/docs
            """
        )
        
        parser.add_argument('--version', '-v', action='version', version=f'KashaLang {VERSION}')
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Run command
        run_parser = subparsers.add_parser('run', help='Run a KashaLang program')
        run_parser.add_argument('file', help='KashaLang file to run')
        run_parser.add_argument('--debug', '-d', action='store_true', help='Show debug info')
        run_parser.add_argument('--ast', '-a', action='store_true', help='Print AST')
        
        # Init command
        init_parser = subparsers.add_parser('init', help='Create a new KashaLang project')
        init_parser.add_argument('name', help='Project name')
        init_parser.add_argument('--template', '-t', choices=['basic', 'web', 'api'], 
                                default='basic', help='Project template')
        init_parser.add_argument('--git', '-g', action='store_true', help='Initialize git repository')
        
        # Install command
        install_parser = subparsers.add_parser('install', help='Install a package')
        install_parser.add_argument('package', nargs='?', help='Package name to install')
        install_parser.add_argument('--save', '-s', action='store_true', help='Save to dependencies')
        install_parser.add_argument('--global', '-g', action='store_true', dest='global_install',
                                   help='Install globally')
        
        # REPL command
        repl_parser = subparsers.add_parser('repl', help='Start interactive shell')
        repl_parser.add_argument('--no-logo', action='store_true', help='Hide logo')
        
        # Export command
        export_parser = subparsers.add_parser('export', help='Export to other formats')
        export_parser.add_argument('format', choices=['web', 'html', 'js'], help='Export format')
        export_parser.add_argument('file', help='KashaLang file to export')
        export_parser.add_argument('--output', '-o', help='Output directory')
        
        # Tokenize command (debug)
        tokenize_parser = subparsers.add_parser('tokenize', help='Tokenize a file (debug)')
        tokenize_parser.add_argument('file', help='File to tokenize')
        
        # Parse command (debug)
        parse_parser = subparsers.add_parser('parse', help='Parse a file (debug)')
        parse_parser.add_argument('file', help='File to parse')
        
        # New command (create file)
        new_parser = subparsers.add_parser('new', help='Create a new KashaLang file')
        new_parser.add_argument('file', help='File name')
        new_parser.add_argument('--template', '-t', choices=['empty', 'hello', 'function', 'loop'],
                               default='hello', help='File template')
        
        # Test command
        test_parser = subparsers.add_parser('test', help='Run tests')
        test_parser.add_argument('path', nargs='?', help='Test file or directory')
        
        # Clean command
        clean_parser = subparsers.add_parser('clean', help='Clean build artifacts')
        
        # Version command
        version_parser = subparsers.add_parser('version', help='Show version info')
        
        return parser
    
    def run(self, args: Optional[List[str]] = None):
        """Run the CLI with given arguments"""
        parsed_args = self.parser.parse_args(args)
        
        if not parsed_args.command:
            print(KASHA_LOGO)
            self.parser.print_help()
            return 0
        
        command_method = getattr(self, f'cmd_{parsed_args.command}', None)
        if command_method:
            try:
                return command_method(parsed_args)
            except KeyboardInterrupt:
                print("\n\n👋 Muraho! (Goodbye!)")
                return 0
            except Exception as e:
                print(f"\n❌ Error: {e}")
                return 1
        else:
            print(f"Unknown command: {parsed_args.command}")
            return 1
    
    def cmd_run(self, args):
        """Run a KashaLang program"""
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            return 1
        
        with open(args.file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        try:
            # Tokenize
            tokens = tokenize(source)
            if args.debug:
                print("🔤 Tokens:")
                for token in tokens:
                    print(f"  {token}")
                print()
            
            # Parse
            ast = parse(tokens)
            if args.ast:
                print("🌳 AST:")
                print(print_ast(ast))
                print()
            
            # Interpret
            result, output = interpret(ast)
            
            if args.debug:
                print(f"\n📊 Return value: {result}")
            
            return 0
            
        except KashaError as e:
            source_lines = source.split('\n')
            print(format_traceback(e, source_lines))
            return 1
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    def cmd_init(self, args):
        """Create a new KashaLang project"""
        from cli.project_init import ProjectInitializer
        
        initializer = ProjectInitializer()
        return initializer.create_project(args.name, args.template, args.git)
    
    def cmd_install(self, args):
        """Install a package"""
        from cli.package_manager import PackageManager
        
        pm = PackageManager()
        
        if not args.package:
            # Install from kasha.json dependencies
            return pm.install_from_config()
        
        return pm.install(args.package, args.save, args.global_install)
    
    def cmd_repl(self, args):
        """Start interactive shell"""
        if not args.no_logo:
            print(KASHA_LOGO)
        
        print("🖥️  KashaLang Interactive Shell (REPL)")
        print("   Type 'reka' to exit, 'ubwoko' for help\n")
        
        from core import Interpreter
        
        interpreter = Interpreter()
        buffer = []
        indent_level = 0
        
        while True:
            try:
                # Show appropriate prompt
                if indent_level > 0:
                    prompt = "... " + "    " * indent_level
                else:
                    prompt = "kasha> "
                
                line = input(prompt)
                
                # Handle special commands
                if line.strip().lower() in ('reka', 'exit', 'quit'):
                    print("👋 Muraho! (Goodbye!)")
                    break
                
                if line.strip().lower() in ('ubwoko', 'help'):
                    self._print_repl_help()
                    continue
                
                if line.strip() == '':
                    if buffer:
                        # Execute buffered code
                        source = '\n'.join(buffer)
                        buffer = []
                        indent_level = 0
                        self._execute_repl_code(source, interpreter)
                    continue
                
                # Add to buffer
                buffer.append(line)
                
                # Simple indentation tracking
                if line.rstrip().endswith(':'):
                    indent_level += 1
                elif line.strip() == '' and indent_level > 0:
                    indent_level -= 1
                
                # Try to execute if line seems complete
                if indent_level == 0 and not line.rstrip().endswith(':'):
                    source = '\n'.join(buffer)
                    buffer = []
                    self._execute_repl_code(source, interpreter)
                    
            except EOFError:
                print("\n👋 Muraho! (Goodbye!)")
                break
            except KeyboardInterrupt:
                print("\n")
                buffer = []
                indent_level = 0
                continue
    
    def _execute_repl_code(self, source: str, interpreter):
        """Execute code in REPL"""
        try:
            tokens = tokenize(source)
            ast = parse(tokens)
            result = interpreter.interpret(ast)
            if result is not None:
                print(f"=> {interpreter._stringify(result)}")
        except KashaError as e:
            source_lines = source.split('\n')
            print(format_traceback(e, source_lines))
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def _print_repl_help(self):
        """Print REPL help"""
        print("""
🌍 KashaLang REPL Commands:
  reka, exit, quit  - Exit the REPL
  ubwoko, help      - Show this help

Examples:
  shyiramo x = 5           # Declare variable
  vuga x + 10              # Print expression
  niba x > 5:              # If statement
      vuga "Big!"          
  fata greet(name):        # Function
      vuga "Hello", name
  greet("Afurika")         # Call function
        """)
    
    def cmd_export(self, args):
        """Export KashaLang to other formats"""
        from cli.exporter import WebExporter
        
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            return 1
        
        exporter = WebExporter()
        output_dir = args.output or f"{Path(args.file).stem}_export"
        
        if args.format in ('web', 'html'):
            return exporter.export_web(args.file, output_dir)
        elif args.format == 'js':
            return exporter.export_js(args.file, output_dir)
        
        return 0
    
    def cmd_tokenize(self, args):
        """Tokenize a file (debug)"""
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            return 1
        
        with open(args.file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        tokens = tokenize(source)
        print(f"🔤 Tokens from {args.file}:")
        print("-" * 60)
        for i, token in enumerate(tokens):
            print(f"{i:3d}: {token.type.name:15s} = {token.value!r}")
        
        return 0
    
    def cmd_parse(self, args):
        """Parse a file (debug)"""
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            return 1
        
        with open(args.file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        tokens = tokenize(source)
        ast = parse(tokens)
        
        print(f"🌳 AST from {args.file}:")
        print("-" * 60)
        print(print_ast(ast))
        
        return 0
    
    def cmd_new(self, args):
        """Create a new KashaLang file"""
        templates = {
            'empty': '',
            'hello': '''# Muraho! Welcome to KashaLang
# This is your first program

vuga "Muraho, Afurika!"
vuga "Welcome to KashaLang"

shyiramo izina = "Developer"
vuga "Hello,", izina
''',
            'function': '''# Functions in KashaLang

# Define a function
fata greet(name)
    vuga "Muraho,", name + "!"
    subiza "Welcome to KashaLang"

# Call the function
shyiramo result = greet("Afurika")
vuga result

# Function with default parameter
fata add(a, b = 10)
    subiza a + b

vuga add(5)      # 15
vuga add(5, 3)   # 8
''',
            'loop': '''# Loops in KashaLang

# While loop
shyiramo i = 0
igihe i < 5
    vuga "Count:", i
    i = i + 1

# For loop with range
vuga ""
vuga "Range loop:"
kugeza j from 0 to 5
    vuga "J =", j

# Loop through list
vuga ""
vuga "List loop:"
shyiramo fruits = ["apple", "banana", "orange"]
subiramo fruit in fruits
    vuga "Fruit:", fruit
'''
        }
        
        content = templates.get(args.template, templates['hello'])
        
        # Add .kasha extension if not present
        filename = args.file
        if not filename.endswith('.kasha'):
            filename += '.kasha'
        
        if os.path.exists(filename):
            print(f"❌ File already exists: {filename}")
            return 1
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created {filename}")
        return 0
    
    def cmd_test(self, args):
        """Run tests"""
        test_path = args.path or '.'
        
        if os.path.isfile(test_path):
            return self._run_test_file(test_path)
        elif os.path.isdir(test_path):
            return self._run_test_directory(test_path)
        else:
            print(f"❌ Test path not found: {test_path}")
            return 1
    
    def _run_test_file(self, filepath: str) -> int:
        """Run a single test file"""
        print(f"🧪 Running test: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        
        try:
            tokens = tokenize(source)
            ast = parse(tokens)
            result, output = interpret(ast)
            print(f"✅ Test passed: {filepath}")
            return 0
        except KashaError as e:
            print(f"❌ Test failed: {filepath}")
            source_lines = source.split('\n')
            print(format_traceback(e, source_lines))
            return 1
    
    def _run_test_directory(self, directory: str) -> int:
        """Run all test files in a directory"""
        print(f"🧪 Running tests in: {directory}\n")
        
        passed = 0
        failed = 0
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.kasha') and file.startswith('test_'):
                    filepath = os.path.join(root, file)
                    if self._run_test_file(filepath) == 0:
                        passed += 1
                    else:
                        failed += 1
        
        print(f"\n📊 Results: {passed} passed, {failed} failed")
        return 0 if failed == 0 else 1
    
    def cmd_clean(self, args):
        """Clean build artifacts"""
        patterns = ['*.pyc', '__pycache__', '*.kashac', 'build', 'dist']
        
        removed = []
        for pattern in patterns:
            for path in Path('.').rglob(pattern):
                if path.is_file():
                    path.unlink()
                    removed.append(str(path))
                elif path.is_dir():
                    import shutil
                    shutil.rmtree(path)
                    removed.append(str(path))
        
        if removed:
            print(f"🧹 Cleaned {len(removed)} items:")
            for item in removed[:10]:
                print(f"  - {item}")
            if len(removed) > 10:
                print(f"  ... and {len(removed) - 10} more")
        else:
            print("🧹 Nothing to clean")
        
        return 0
    
    def cmd_version(self, args):
        """Show version info"""
        print(KASHA_LOGO)
        print(f"Version: {VERSION}")
        print(f"Python: {sys.version}")
        print(f"Platform: {sys.platform}")
        print("\n🌍 Made with love for Africa")
        print("📧 Contact: hello@kashalang.dev")
        print("🌐 Website: https://kashalang.dev")
        return 0


def main():
    """Main entry point"""
    cli = KashaCLI()
    sys.exit(cli.run())


if __name__ == '__main__':
    main()

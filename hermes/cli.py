"""
Hermes CLI - Command line interface
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        prog="hermes",
        description="Hermes Language - Cultural syntax transpiled to Python"
    )
    parser.add_argument("--version", action="version", version="hermes 0.1.0")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # run command
    run_parser = subparsers.add_parser("run", help="Run a Hermes file")
    run_parser.add_argument("file", help="Path to .herm file")
    run_parser.add_argument("--debug", action="store_true", help="Show transpiled code")
    
    # compile command
    compile_parser = subparsers.add_parser("compile", help="Transpile to Python")
    compile_parser.add_argument("file", help="Path to .herm file")
    compile_parser.add_argument("-o", "--output", help="Output file path")
    
    # check command
    check_parser = subparsers.add_parser("check", help="Syntax check only")
    check_parser.add_argument("file", help="Path to .herm file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        from .lexer import Lexer
        from .parser import Parser
        from .transpiler import Transpiler
        
        if args.command in ("run", "compile", "check"):
            path = Path(args.file)
            if not path.exists():
                print(f"Error: File not found: {args.file}", file=sys.stderr)
                return 1
            
            source = path.read_text()
            
            # Tokenize
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            # Parse
            parser_obj = Parser()
            ast = parser_obj.parse(tokens)
            
            # Transpile
            transpiler = Transpiler()
            python_code = transpiler.transpile(ast)
            
            if args.command == "check":
                print(f"OK: {args.file}")
                return 0
            
            if args.command == "compile":
                if args.output:
                    Path(args.output).write_text(python_code)
                    print(f"Compiled to: {args.output}")
                else:
                    print(python_code)
                return 0
            
            if args.command == "run":
                if getattr(args, "debug", False):
                    print("=== Transpiled Python ===")
                    print(python_code)
                    print("=== Output ===")
                
                exec(python_code, {"__name__": "__main__"})
                return 0
    
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

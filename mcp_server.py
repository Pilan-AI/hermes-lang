#!/usr/bin/env python3
"""
Hermes MCP Server
Provides auto-injection of Hermes language help and syntax
"""

import sys
import json

VERSION = "1.0.0"

class HermesMCPServer:
    """MCP server for Hermes language support"""
    
    def __init__(self):
        self.tools = {
            "hermes_inject": {
                "name": "Hermes Auto-Inject Context",
                "description": "Inject Hermes language help, syntax, and examples",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "User message or topic",
                            "required": ["query"]
                        }
                    }
                }
            },
            "hermes_help": {
                "name": "Hermes Help",
                "description": "Get Hermes language reference and usage examples",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "Specific topic (e.g., 'sangam skin', 'transpiler')",
                            "required": []
                        }
                    }
                }
            }
        }
    
    def handle_call(self, method_name, params):
        """Route tool calls to appropriate handlers"""
        if method_name == "hermes_inject":
            return self.handle_inject(params)
        elif method_name == "hermes_help":
            return self.handle_help(params)
        else:
            return {
                "error": f"Unknown tool: {method_name}"
            }
    
    def handle_inject(self, params):
        """Inject Hermes context based on query"""
        query = params.get("query", "")
        
        if not query:
            return {"content": ""}
        
        # Simple context injection based on query
        # In production, you could search documentation or provide examples
        context_map = {
            "sangam": """## Sangam Skin

The Sangam skin provides traditional Tamil cultural elements.

Usage:
```
hermes
scheme main(name: string):
    announce("Vanakkam, " + name)
```

Examples:
```
hermes
scheme greet(name: "world"):
    announce("Hello, " + name)
```
""",
            "transpiler": """## Transpiler Usage

The transpiler converts Hermes syntax to Python.

Main Features:
- Sangam skin keywords (வளல், து, etc.)
- Traditional Tamil cultural patterns
- Compile-time error checking
""",
            "syntax": """## Hermes Syntax Reference

Hermes is a cultural syntax language that transpiles to Python.

Basic Structure:
```
scheme name(parameters):
    action1
    action2
    action3

thats_it:
    action4
```

Cultural Keywords (Sangam Skin):
- வளல் (Vanakkam) - "Let it happen"
- து (Thu) - "Do"
- அ (Ka) - "Do" (command)
- ப (Pa) - "Do" (suggestion)
"""
        }
        
        # Get most relevant context based on query
        relevant_topics = []
        query_lower = query.lower()
        
        for topic, content in context_map.items():
            if topic in query_lower or any(word in query_lower for word in content.lower().split()):
                relevant_topics.append(content)
        
        if not relevant_topics:
            return {"content": ""}
        
        # Combine relevant sections
        full_context = "\n\n".join(relevant_topics)
        formatted_context = f"## Hermes Context\n\n{full_context}\n---"
        
        return {"content": formatted_context}
    
    def handle_help(self, params):
        """Get help for specific topic"""
        topic = params.get("topic", "")
        
        if not topic:
            # Return general help if no topic specified
            return {"content": self.handle_inject({"query": "syntax reference"})["content"]}
        
        # Get specific topic help
        topic_lower = topic.lower()
        context = self.handle_inject({"query": topic})["content"]
        
        return {"content": context}
    
    def send_response(self, response):
        """Send response to stdout (MCP protocol)"""
        print(json.dumps(response, ensure_ascii=False))
        sys.stdout.flush()
    
    def serve_forever(self):
        """Serve MCP requests from stdin"""
        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                
                try:
                    request = json.loads(line)
                    method_name = request.get("method", "")
                    params = request.get("params", {})
                    
                    result = self.handle_call(method_name, params)
                    self.send_response(result)
                    
                except json.JSONDecodeError as e:
                    self.send_response({
                        "error": f"Invalid JSON: {str(e)}"
                    })
                except Exception as e:
                    self.send_response({
                        "error": f"Internal error: {str(e)}"
                    })
                    
        except KeyboardInterrupt:
            print("", file=sys.stderr)
            sys.exit(0)

def main():
    print(f"Hermes MCP Server v{VERSION}", file=sys.stderr)
    print("Reading from stdin, writing to stdout...", file=sys.stderr)
    print("Press Ctrl+C to stop", file=sys.stderr)
    print()
    
    server = HermesMCPServer()
    server.serve_forever()

if __name__ == "__main__":
    main()

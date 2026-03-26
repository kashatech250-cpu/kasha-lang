"""
KashaLang Exporter - Export KashaLang programs to HTML/CSS/JS
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional


class WebExporter:
    """Export KashaLang programs to web formats"""
    
    def __init__(self):
        self.output_dir: Optional[Path] = None
    
    def export_web(self, source_file: str, output_dir: str) -> int:
        """Export a KashaLang program to a web application"""
        print(f"🌐 Exporting {source_file} to web...")
        
        if not os.path.exists(source_file):
            print(f"❌ File not found: {source_file}")
            return 1
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Read source file
        with open(source_file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse the KashaLang program to extract data
        program_data = self._parse_program(source)
        
        # Generate HTML
        html_content = self._generate_html(program_data, source_file)
        html_path = self.output_dir / 'index.html'
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"  ✓ Created {html_path}")
        
        # Generate CSS
        css_content = self._generate_css(program_data)
        css_path = self.output_dir / 'style.css'
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        print(f"  ✓ Created {css_path}")
        
        # Generate JavaScript
        js_content = self._generate_js(program_data, source)
        js_path = self.output_dir / 'app.js'
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f"  ✓ Created {js_path}")
        
        # Copy any assets
        self._copy_assets(source_file)
        
        print()
        print(f"✅ Export complete!")
        print(f"   Output: {self.output_dir.absolute()}")
        print()
        print("To view your app:")
        print(f"   cd {output_dir}")
        print("   # Open index.html in your browser")
        print("   # Or serve with: python -m http.server 8000")
        
        return 0
    
    def export_js(self, source_file: str, output_dir: str) -> int:
        """Export a KashaLang program to JavaScript only"""
        print(f"📜 Exporting {source_file} to JavaScript...")
        
        if not os.path.exists(source_file):
            print(f"❌ File not found: {source_file}")
            return 1
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        with open(source_file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        program_data = self._parse_program(source)
        js_content = self._generate_js(program_data, source)
        
        js_path = output_path / f"{Path(source_file).stem}.js"
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print(f"✅ Created {js_path}")
        return 0
    
    def _parse_program(self, source: str) -> Dict:
        """Parse a KashaLang program to extract data"""
        # This is a simplified parser for demo purposes
        # In a full implementation, this would use the actual AST
        
        data = {
            'title': 'KashaLang App',
            'heading': 'Welcome to KashaLang',
            'content': '',
            'variables': {},
            'functions': [],
            'prints': []
        }
        
        lines = source.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Extract vuga statements
            if line.startswith('vuga '):
                content = line[5:].strip()
                # Remove quotes if present
                if (content.startswith('"') and content.endswith('"')) or \
                   (content.startswith("'") and content.endswith("'")):
                    content = content[1:-1]
                data['prints'].append(content)
            
            # Extract shyiramo (variable declarations)
            if line.startswith('shyiramo '):
                parts = line[9:].split('=', 1)
                if len(parts) == 2:
                    var_name = parts[0].strip()
                    var_value = parts[1].strip()
                    data['variables'][var_name] = var_value
            
            # Extract fata (function definitions)
            if line.startswith('fata '):
                func_name = line[5:].split('(')[0].strip()
                data['functions'].append(func_name)
        
        # Try to find title in variables
        if 'title' in data['variables']:
            data['title'] = data['variables']['title'].strip('"\'')
        if 'heading' in data['variables']:
            data['heading'] = data['variables']['heading'].strip('"\'')
        
        return data
    
    def _generate_html(self, data: Dict, source_file: str) -> str:
        """Generate HTML file"""
        title = data.get('title', 'KashaLang App')
        heading = data.get('heading', 'Welcome to KashaLang')
        
        prints = data.get('prints', [])
        output_html = ''
        for p in prints:
            output_html += f'            <div class="output-line">{p}</div>\n'
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
    <!-- KashaLang Generated - {source_file} -->
</head>
<body>
    <div class="container">
        <header>
            <h1>🌍 {heading}</h1>
            <p class="subtitle">Generated by KashaLang</p>
        </header>
        
        <main>
            <div class="output-panel">
                <h2>Program Output</h2>
                <div id="output">
{output_html}                </div>
            </div>
            
            <div class="controls">
                <button id="runBtn" class="btn btn-primary">▶ Run</button>
                <button id="clearBtn" class="btn btn-secondary">Clear</button>
            </div>
            
            <div class="info-panel">
                <h3>Variables</h3>
                <pre id="variables">{json.dumps(data.get('variables', {{}}), indent=2)}</pre>
                
                <h3>Functions</h3>
                <ul id="functions">
                    {''.join(f'<li>{f}()</li>' for f in data.get('functions', []))}
                </ul>
            </div>
        </main>
        
        <footer>
            <p>Made with 🌍 <a href="https://kashalang.dev" target="_blank">KashaLang</a></p>
        </footer>
    </div>
    
    <script src="app.js"></script>
</body>
</html>
'''
        return html
    
    def _generate_css(self, data: Dict) -> str:
        """Generate CSS file"""
        css = '''/* KashaLang Generated Styles */

:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #f093fb;
    --text-color: #333;
    --bg-color: #f5f5f5;
    --panel-bg: #ffffff;
    --border-radius: 12px;
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    min-height: 100vh;
    color: var(--text-color);
    line-height: 1.6;
}

.container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
}

header {
    text-align: center;
    color: white;
    margin-bottom: 2rem;
}

header h1 {
    font-size: 3rem;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.subtitle {
    opacity: 0.9;
    font-size: 1.1rem;
}

main {
    background: var(--panel-bg);
    border-radius: var(--border-radius);
    padding: 2rem;
    box-shadow: var(--shadow);
}

.output-panel {
    background: #1e1e1e;
    border-radius: var(--border-radius);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

.output-panel h2 {
    color: #fff;
    margin-bottom: 1rem;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

#output {
    font-family: 'Fira Code', 'Consolas', monospace;
    color: #4ec9b0;
    min-height: 150px;
}

.output-line {
    padding: 0.25rem 0;
    border-bottom: 1px solid #333;
}

.output-line:last-child {
    border-bottom: none;
}

.controls {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.btn {
    padding: 0.75rem 2rem;
    border: none;
    border-radius: var(--border-radius);
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 600;
}

.btn-primary {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
    background: #e0e0e0;
    color: var(--text-color);
}

.btn-secondary:hover {
    background: #d0d0d0;
}

.info-panel {
    background: var(--bg-color);
    border-radius: var(--border-radius);
    padding: 1.5rem;
}

.info-panel h3 {
    margin-bottom: 0.75rem;
    color: var(--primary-color);
}

.info-panel pre {
    background: #fff;
    padding: 1rem;
    border-radius: 8px;
    overflow-x: auto;
    margin-bottom: 1.5rem;
}

.info-panel ul {
    list-style: none;
    padding-left: 0;
}

.info-panel li {
    padding: 0.5rem;
    background: #fff;
    margin-bottom: 0.5rem;
    border-radius: 6px;
    font-family: monospace;
}

footer {
    text-align: center;
    color: white;
    margin-top: 2rem;
    opacity: 0.9;
}

footer a {
    color: white;
    text-decoration: underline;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.output-line {
    animation: fadeIn 0.3s ease;
}

/* Responsive */
@media (max-width: 600px) {
    .container {
        padding: 1rem;
    }
    
    header h1 {
        font-size: 2rem;
    }
    
    main {
        padding: 1rem;
    }
}
'''
        return css
    
    def _generate_js(self, data: Dict, source: str) -> str:
        """Generate JavaScript file"""
        prints = data.get('prints', [])
        
        js = f'''// KashaLang Generated JavaScript
// Source: KashaLang program

console.log('🌍 KashaLang App Loaded');

// Program Data
const programData = {json.dumps(data, indent=2)};

// KashaLang Runtime (simplified)
const KashaRuntime = {{
    variables: {{}},
    functions: {{}},
    
    // vuga - print function
    vuga: function(...args) {{
        const output = args.map(arg => String(arg)).join(' ');
        console.log(output);
        return output;
    }},
    
    // shyiramo - variable declaration
    shyiramo: function(name, value) {{
        this.variables[name] = value;
        return value;
    }},
    
    // fata - function definition
    fata: function(name, fn) {{
        this.functions[name] = fn;
        return fn;
    }},
    
    // niba - if condition
    niba: function(condition, thenFn, elseFn) {{
        if (condition) {{
            return thenFn ? thenFn() : undefined;
        }} else {{
            return elseFn ? elseFn() : undefined;
        }}
    }},
    
    // subiramo - loop
    subiramo: function(iterable, fn) {{
        for (let item of iterable) {{
            fn(item);
        }}
    }},
    
    // kugeza - range loop
    kugeza: function(start, end, step = 1, fn) {{
        for (let i = start; i < end; i += step) {{
            fn(i);
        }}
    }}
}};

// DOM Ready
document.addEventListener('DOMContentLoaded', () => {{
    const outputDiv = document.getElementById('output');
    const runBtn = document.getElementById('runBtn');
    const clearBtn = document.getElementById('clearBtn');
    
    // Display initial output
    function displayOutput() {{
        const prints = {json.dumps(prints)};
        outputDiv.innerHTML = prints.map(p => `<div class="output-line">${{p}}</div>`).join('');
    }}
    
    // Run button
    runBtn.addEventListener('click', () => {{
        outputDiv.innerHTML = '';
        
        // Simulate program execution
        setTimeout(() => {{
            displayOutput();
        }}, 100);
        
        // Show animation
        runBtn.textContent = '⏳ Running...';
        setTimeout(() => {{
            runBtn.textContent = '▶ Run';
        }}, 500);
    }});
    
    // Clear button
    clearBtn.addEventListener('click', () => {{
        outputDiv.innerHTML = '<div class="output-line" style="color: #666;">Output cleared. Click Run to execute.</div>';
    }});
    
    // Initial display
    displayOutput();
}});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = {{ KashaRuntime, programData }};
}}
'''
        return js
    
    def _copy_assets(self, source_file: str):
        """Copy any assets referenced in the source file"""
        source_dir = Path(source_file).parent
        
        # Copy any .kasha files in the same directory
        for file in source_dir.glob('*.kasha'):
            if file.name != Path(source_file).name:
                dest = self.output_dir / file.name
                # Don't copy, just note it
                print(f"  ℹ️  Found related file: {file.name}")


class MobileExporter:
    """Export KashaLang programs to mobile app structure"""
    
    def export_react_native(self, source_file: str, output_dir: str) -> int:
        """Export to React Native structure (future feature)"""
        print("📱 Mobile export is a future feature!")
        print("   For now, use the web export and wrap with Capacitor or Cordova.")
        return 0
    
    def export_flutter(self, source_file: str, output_dir: str) -> int:
        """Export to Flutter structure (future feature)"""
        print("📱 Flutter export is a future feature!")
        return 0

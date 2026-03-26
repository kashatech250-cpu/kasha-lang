"""
KashaLang Project Initializer - Create new projects with templates
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Optional


class ProjectInitializer:
    """Initialize new KashaLang projects"""
    
    TEMPLATES = {
        'basic': {
            'description': 'Basic KashaLang project',
            'files': {
                'main.kasha': '''# Welcome to KashaLang!
# This is your main program file

vuga "Muraho, Afurika!"
vuga "Welcome to your new KashaLang project"

# Declare a variable
shyiramo izina = "Developer"
vuga "Hello,", izina

# Simple function
fata greet(name) {
    subiza "Muraho, " + name + "!"
}

# Call the function
shyiramo ubutumwa = greet("Kasha")
vuga ubutumwa
''',
                'README.md': '''# {project_name}

A KashaLang project created with `kasha init`.

## Getting Started

Run the program:
```bash
kasha run main.kasha
```

## Project Structure

```
{project_name}/
├── main.kasha      # Main program file
├── kasha.json      # Project configuration
└── README.md       # This file
```

## Learn More

- [KashaLang Documentation](https://kashalang.dev/docs)
- [Examples](https://kashalang.dev/examples)
- [Community](https://kashalang.dev/community)

---
Made with 🌍 KashaLang
''',
            }
        },
        'web': {
            'description': 'Web application project',
            'files': {
                'main.kasha': '''# KashaLang Web App
# This will be exported to HTML/CSS/JS

vuga "Web App: {project_name}"

# Define page structure
shyiramo page = {
    "title": "{project_name}",
    "heading": "Welcome to {project_name}",
    "content": "Built with KashaLang"
}

# Output page info
vuga "Title:", page["title"]
vuga "Heading:", page["heading"]
''',
                'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>🌍 {project_name}</h1>
        <p>Built with KashaLang</p>
        <div id="app"></div>
    </div>
    <script src="app.js"></script>
</body>
</html>
''',
                'style.css': '''/* KashaLang Web App Styles */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.container {
    background: white;
    padding: 3rem;
    border-radius: 1rem;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    text-align: center;
    max-width: 500px;
}

h1 {
    color: #333;
    margin-bottom: 1rem;
    font-size: 2.5rem;
}

p {
    color: #666;
    margin-bottom: 2rem;
}

#app {
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 0.5rem;
    min-height: 100px;
}
''',
                'app.js': '''// KashaLang Web App JavaScript

console.log('🌍 {project_name} - Built with KashaLang');

document.addEventListener('DOMContentLoaded', () => {
    const app = document.getElementById('app');
    
    app.innerHTML = `
        <h2>Welcome to KashaLang!</h2>
        <p>This app was generated from KashaLang code.</p>
        <button id="greetBtn">Say Hello</button>
    `;
    
    document.getElementById('greetBtn').addEventListener('click', () => {
        alert('Muraho! Hello from KashaLang! 🌍');
    });
});
''',
                'README.md': '''# {project_name}

A KashaLang web application.

## Getting Started

### Run the KashaLang program:
```bash
kasha run main.kasha
```

### Export to web:
```bash
kasha export web main.kasha --output ./dist
```

### Open in browser:
Open `index.html` in your web browser.

## Project Structure

```
{project_name}/
├── main.kasha      # KashaLang source code
├── index.html      # HTML template
├── style.css       # Styles
├── app.js          # JavaScript
├── kasha.json      # Project configuration
└── README.md       # This file
```

## Customization

1. Edit `main.kasha` to change the app logic
2. Edit `style.css` to change the appearance
3. Edit `app.js` to add interactivity

## Deployment

Upload the files to any static hosting service:
- GitHub Pages
- Netlify
- Vercel
- Firebase Hosting

---
Built with 🌍 KashaLang
''',
            }
        },
        'api': {
            'description': 'API server project',
            'files': {
                'main.kasha': '''# KashaLang API Server
# This simulates an API server

vuga "Starting API Server: {project_name}"
vuga ""

# Define API routes
shyiramo routes = [
    {"path": "/", "method": "GET", "description": "Home"},
    {"path": "/users", "method": "GET", "description": "List users"},
    {"path": "/users/:id", "method": "GET", "description": "Get user"}
]

# Display routes
vuga "Available Routes:"
subiramo route in routes
    vuga route["method"], route["path"], "-", route["description"]

vuga ""
vuga "Server would be running on http://localhost:3000"
''',
                'README.md': '''# {project_name}

A KashaLang API project.

## Getting Started

Run the program:
```bash
kasha run main.kasha
```

## API Endpoints

- `GET /` - Home
- `GET /users` - List all users
- `GET /users/:id` - Get user by ID

## Project Structure

```
{project_name}/
├── main.kasha      # API logic
├── kasha.json      # Project configuration
└── README.md       # This file
```

## Future Features

- Real HTTP server
- Database integration
- Authentication
- Middleware support

---
Built with 🌍 KashaLang
''',
            }
        }
    }
    
    def create_project(self, name: str, template: str = 'basic', init_git: bool = False) -> int:
        """Create a new project with the given template"""
        
        # Validate project name
        if not self._validate_name(name):
            return 1
        
        # Check if directory already exists
        if os.path.exists(name):
            print(f"❌ Directory '{name}' already exists")
            return 1
        
        # Get template
        template_config = self.TEMPLATES.get(template)
        if not template_config:
            print(f"❌ Unknown template: {template}")
            print(f"Available templates: {', '.join(self.TEMPLATES.keys())}")
            return 1
        
        print(f"🌍 Creating new KashaLang project: {name}")
        print(f"📦 Template: {template_config['description']}")
        print()
        
        # Create project directory
        os.makedirs(name)
        
        # Create files from template
        for filename, content in template_config['files'].items():
            filepath = os.path.join(name, filename)
            # Use replace instead of format to avoid issues with curly braces in CSS/JS
            formatted_content = content.replace('{{project_name}}', name).replace('{project_name}', name)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            
            print(f"  ✓ Created {filename}")
        
        # Create kasha.json
        kasha_config = {
            'name': name,
            'version': '1.0.0',
            'description': f'A KashaLang project: {name}',
            'main': 'main.kasha',
            'author': '',
            'license': 'MIT',
            'dependencies': {},
            'devDependencies': {},
            'scripts': {
                'run': 'kasha run main.kasha',
                'test': 'kasha test',
                'build': 'kasha export web main.kasha'
            },
            'keywords': ['kashalang'],
            'template': template
        }
        
        config_path = os.path.join(name, 'kasha.json')
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(kasha_config, f, indent=2)
        print(f"  ✓ Created kasha.json")
        
        # Initialize git repository
        if init_git:
            print()
            print("🔧 Initializing git repository...")
            try:
                os.chdir(name)
                subprocess.run(['git', 'init'], capture_output=True, check=True)
                
                # Create .gitignore
                gitignore_content = '''# KashaLang
*.kashac
build/
dist/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
'''
                with open('.gitignore', 'w', encoding='utf-8') as f:
                    f.write(gitignore_content)
                
                subprocess.run(['git', 'add', '.'], capture_output=True, check=True)
                subprocess.run(['git', 'commit', '-m', 'Initial commit from KashaLang'], 
                             capture_output=True, check=True)
                print("  ✓ Git repository initialized")
                os.chdir('..')
            except subprocess.CalledProcessError as e:
                print(f"  ⚠️  Git initialization failed: {e}")
            except FileNotFoundError:
                print("  ⚠️  Git not found. Please install git.")
        
        # Create .kasha directory for project metadata
        kasha_dir = os.path.join(name, '.kasha')
        os.makedirs(kasha_dir, exist_ok=True)
        
        # Create project metadata
        metadata = {
            'created_with': 'kasha init',
            'template': template,
            'version': '1.0.0'
        }
        
        metadata_path = os.path.join(kasha_dir, 'project.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print()
        print(f"✅ Project '{name}' created successfully!")
        print()
        print("Next steps:")
        print(f"  cd {name}")
        print(f"  kasha run main.kasha")
        print()
        print("Happy coding! 🌍")
        
        return 0
    
    def _validate_name(self, name: str) -> bool:
        """Validate project name"""
        if not name:
            print("❌ Project name cannot be empty")
            return False
        
        if not name[0].isalpha():
            print("❌ Project name must start with a letter")
            return False
        
        if not all(c.isalnum() or c in '-_' for c in name):
            print("❌ Project name can only contain letters, numbers, hyphens, and underscores")
            return False
        
        if len(name) > 50:
            print("❌ Project name is too long (max 50 characters)")
            return False
        
        return True
    
    def list_templates(self):
        """List available templates"""
        print("📦 Available Templates:")
        print()
        for name, config in self.TEMPLATES.items():
            print(f"  {name:10s} - {config['description']}")
        print()
        print("Usage: kasha init <name> --template <template>")

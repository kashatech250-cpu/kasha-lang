"""
KashaLang Package Manager - Install and manage packages
"""

import os
import json
import urllib.request
import urllib.error
import zipfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional


class PackageManager:
    """Manage KashaLang packages"""
    
    # Default package registry (can be extended)
    REGISTRY_URL = "https://registry.kashalang.dev/packages"
    
    # Built-in packages that don't need installation
    BUILT_IN_PACKAGES = {
        'kasha-core': {
            'description': 'Core KashaLang utilities',
            'version': '1.0.0',
            'built_in': True
        },
        'kasha-math': {
            'description': 'Mathematical functions',
            'version': '1.0.0',
            'built_in': True
        },
        'kasha-string': {
            'description': 'String manipulation utilities',
            'version': '1.0.0',
            'built_in': True
        },
        'kasha-list': {
            'description': 'List/array utilities',
            'version': '1.0.0',
            'built_in': True
        },
        'kasha-io': {
            'description': 'Input/output utilities',
            'version': '1.0.0',
            'built_in': True
        },
    }
    
    # Simulated package registry for demo
    DEMO_PACKAGES = {
        'kasha-web': {
            'name': 'kasha-web',
            'version': '1.0.0',
            'description': 'Web framework for KashaLang',
            'author': 'KashaLang Team',
            'dependencies': {},
            'files': {
                'web.kasha': '''# KashaWeb - Web Framework for KashaLang

fata render(template, data)
    # Simple template rendering
    shyiramo result = template
    subiramo key in data
        shyiramo placeholder = "{{" + key + "}}"
        shyiramo value = data[key]
        result = result.replace(placeholder, value)
    subiza result

fata createElement(tag, content)
    subiza "<" + tag + ">" + content + "</" + tag + ">"
'''
            }
        },
        'kasha-http': {
            'name': 'kasha-http',
            'version': '1.0.0',
            'description': 'HTTP client for KashaLang',
            'author': 'KashaLang Team',
            'dependencies': {},
            'files': {
                'http.kasha': '''# KashaHTTP - HTTP Client for KashaLang

fata get(url)
    vuga "GET request to:", url
    subiza {"status": 200, "data": "Mock response"}

fata post(url, data)
    vuga "POST request to:", url
    subiza {"status": 201, "data": "Created"}
'''
            }
        },
        'kasha-json': {
            'name': 'kasha-json',
            'version': '1.0.0',
            'description': 'JSON utilities for KashaLang',
            'author': 'KashaLang Team',
            'dependencies': {},
            'files': {
                'json.kasha': '''# KashaJSON - JSON Utilities for KashaLang

fata parse(jsonString)
    # Mock JSON parsing
    vuga "Parsing JSON..."
    subiza {}

fata stringify(obj)
    # Mock JSON stringification
    subiza "{}"
'''
            }
        },
        'kasha-colors': {
            'name': 'kasha-colors',
            'version': '1.0.0',
            'description': 'Terminal colors for KashaLang',
            'author': 'KashaLang Team',
            'dependencies': {},
            'files': {
                'colors.kasha': '''# KashaColors - Terminal Colors for KashaLang

shyiramo RED = "\\033[91m"
shyiramo GREEN = "\\033[92m"
shyiramo YELLOW = "\\033[93m"
shyiramo BLUE = "\\033[94m"
shyiramo MAGENTA = "\\033[95m"
shyiramo CYAN = "\\033[96m"
shyiramo WHITE = "\\033[97m"
shyiramo RESET = "\\033[0m"

fata color(text, colorCode)
    subiza colorCode + text + RESET
'''
            }
        },
        'kasha-test': {
            'name': 'kasha-test',
            'version': '1.0.0',
            'description': 'Testing framework for KashaLang',
            'author': 'KashaLang Team',
            'dependencies': {},
            'files': {
                'test.kasha': '''# KashaTest - Testing Framework for KashaLang

shyiramo tests = []
shyiramo passed = 0
shyiramo failed = 0

fata describe(name, fn)
    vuga "Test Suite:", name
    fn()
    vuga ""

fata it(description, fn)
    vuga "  -", description
    # Mock test execution
    passed = passed + 1

fata expect(actual)
    subiza {
        "toBe": fata(expected)
            niba actual != expected
                vuga "    ❌ Expected", expected, "but got", actual
                failed = failed + 1
                passed = passed - 1
            nanone
                vuga "    ✓"
    }
'''
            }
        }
    }
    
    def __init__(self):
        self.project_root = self._find_project_root()
        self.packages_dir = self._get_packages_dir()
    
    def _find_project_root(self) -> Optional[Path]:
        """Find the project root directory (where kasha.json is)"""
        current = Path.cwd()
        while current != current.parent:
            if (current / 'kasha.json').exists():
                return current
            current = current.parent
        return None
    
    def _get_packages_dir(self) -> Path:
        """Get the packages directory"""
        if self.project_root:
            return self.project_root / 'kasha_modules'
        return Path.cwd() / 'kasha_modules'
    
    def install(self, package_name: str, save: bool = False, global_install: bool = False) -> int:
        """Install a package"""
        print(f"📦 Installing {package_name}...")
        
        # Check if it's a built-in package
        if package_name in self.BUILT_IN_PACKAGES:
            print(f"  ✓ {package_name} is built-in, no installation needed")
            return 0
        
        # Get package info from registry
        package_info = self._fetch_package_info(package_name)
        
        if not package_info:
            print(f"❌ Package not found: {package_name}")
            print(f"   Run 'kasha search {package_name}' to find similar packages")
            return 1
        
        # Determine install location
        if global_install:
            install_dir = Path.home() / '.kasha' / 'packages'
        else:
            install_dir = self.packages_dir
        
        # Create packages directory
        install_dir.mkdir(parents=True, exist_ok=True)
        
        # Install package
        package_dir = install_dir / package_name
        
        if package_dir.exists():
            print(f"  ⚠️  {package_name} is already installed")
            print(f"     Use 'kasha update {package_name}' to update")
            return 0
        
        try:
            package_dir.mkdir()
            
            # Write package files
            for filename, content in package_info.get('files', {}).items():
                filepath = package_dir / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Write package metadata
            metadata = {
                'name': package_info['name'],
                'version': package_info['version'],
                'description': package_info['description'],
                'author': package_info.get('author', ''),
                'installed_at': str(Path.cwd()),
            }
            
            with open(package_dir / 'package.json', 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"  ✓ Installed {package_name}@{package_info['version']}")
            
            # Save to dependencies if requested
            if save and self.project_root:
                self._add_to_dependencies(package_name, package_info['version'])
            
            # Install dependencies
            for dep_name, dep_version in package_info.get('dependencies', {}).items():
                print(f"  📦 Installing dependency: {dep_name}@{dep_version}")
                self.install(dep_name, save=False, global_install=global_install)
            
            return 0
            
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            # Clean up
            if package_dir.exists():
                shutil.rmtree(package_dir)
            return 1
    
    def install_from_config(self) -> int:
        """Install packages from kasha.json"""
        if not self.project_root:
            print("❌ No kasha.json found in current directory or parents")
            return 1
        
        config_path = self.project_root / 'kasha.json'
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        dependencies = config.get('dependencies', {})
        dev_dependencies = config.get('devDependencies', {})
        
        all_deps = {**dependencies, **dev_dependencies}
        
        if not all_deps:
            print("📦 No dependencies to install")
            return 0
        
        print(f"📦 Installing {len(all_deps)} package(s)...")
        print()
        
        failed = []
        for package_name, version in all_deps.items():
            if self.install(package_name, save=False, global_install=False) != 0:
                failed.append(package_name)
        
        print()
        if failed:
            print(f"❌ Failed to install: {', '.join(failed)}")
            return 1
        else:
            print("✅ All packages installed successfully")
            return 0
    
    def uninstall(self, package_name: str, global_uninstall: bool = False) -> int:
        """Uninstall a package"""
        print(f"🗑️  Uninstalling {package_name}...")
        
        if global_uninstall:
            package_dir = Path.home() / '.kasha' / 'packages' / package_name
        else:
            package_dir = self.packages_dir / package_name
        
        if not package_dir.exists():
            print(f"❌ Package not installed: {package_name}")
            return 1
        
        try:
            shutil.rmtree(package_dir)
            print(f"  ✓ Uninstalled {package_name}")
            
            # Remove from dependencies
            if self.project_root:
                self._remove_from_dependencies(package_name)
            
            return 0
        except Exception as e:
            print(f"❌ Uninstall failed: {e}")
            return 1
    
    def update(self, package_name: str = None) -> int:
        """Update package(s)"""
        if package_name:
            print(f"🔄 Updating {package_name}...")
            # Uninstall and reinstall
            self.uninstall(package_name)
            return self.install(package_name)
        else:
            # Update all packages
            packages = self._list_installed_packages()
            for pkg in packages:
                self.update(pkg)
            return 0
    
    def list_packages(self) -> int:
        """List installed packages"""
        print("📦 Installed Packages:")
        print()
        
        packages = self._list_installed_packages()
        
        if not packages:
            print("  No packages installed")
            print()
            print("Install packages with: kasha install <package>")
            return 0
        
        for pkg_name, pkg_info in packages.items():
            version = pkg_info.get('version', 'unknown')
            description = pkg_info.get('description', '')
            print(f"  {pkg_name}@{version}")
            if description:
                print(f"    {description}")
        
        print()
        print(f"Total: {len(packages)} package(s)")
        return 0
    
    def search(self, query: str) -> int:
        """Search for packages"""
        print(f"🔍 Searching for '{query}'...")
        print()
        
        results = []
        
        # Search built-in packages
        for name, info in self.BUILT_IN_PACKAGES.items():
            if query.lower() in name.lower() or query.lower() in info['description'].lower():
                results.append((name, info, 'built-in'))
        
        # Search demo packages
        for name, info in self.DEMO_PACKAGES.items():
            if query.lower() in name.lower() or query.lower() in info['description'].lower():
                results.append((name, info, 'registry'))
        
        if not results:
            print("  No packages found")
            return 0
        
        print(f"Found {len(results)} package(s):\n")
        
        for name, info, source in results:
            version = info.get('version', '1.0.0')
            description = info.get('description', '')
            
            if source == 'built-in':
                print(f"  📦 {name}@{version} (built-in)")
            else:
                print(f"  📦 {name}@{version}")
            print(f"     {description}")
            print()
        
        print("Install with: kasha install <package>")
        return 0
    
    def _fetch_package_info(self, package_name: str) -> Optional[Dict]:
        """Fetch package information from registry"""
        # First check demo packages
        if package_name in self.DEMO_PACKAGES:
            return self.DEMO_PACKAGES[package_name]
        
        # Try to fetch from registry (in real implementation)
        # For now, return None
        return None
    
    def _add_to_dependencies(self, package_name: str, version: str):
        """Add package to kasha.json dependencies"""
        config_path = self.project_root / 'kasha.json'
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if 'dependencies' not in config:
            config['dependencies'] = {}
        
        config['dependencies'][package_name] = f"^{version}"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        print(f"  ✓ Added to kasha.json dependencies")
    
    def _remove_from_dependencies(self, package_name: str):
        """Remove package from kasha.json dependencies"""
        config_path = self.project_root / 'kasha.json'
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if 'dependencies' in config and package_name in config['dependencies']:
            del config['dependencies'][package_name]
        
        if 'devDependencies' in config and package_name in config['devDependencies']:
            del config['devDependencies'][package_name]
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    
    def _list_installed_packages(self) -> Dict[str, Dict]:
        """List all installed packages"""
        packages = {}
        
        if self.packages_dir.exists():
            for pkg_dir in self.packages_dir.iterdir():
                if pkg_dir.is_dir():
                    metadata_file = pkg_dir / 'package.json'
                    if metadata_file.exists():
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            packages[pkg_dir.name] = json.load(f)
        
        return packages
    
    def info(self, package_name: str) -> int:
        """Show package information"""
        # Check built-in
        if package_name in self.BUILT_IN_PACKAGES:
            info = self.BUILT_IN_PACKAGES[package_name]
            print(f"📦 {package_name} (built-in)")
            print(f"   Version: {info['version']}")
            print(f"   Description: {info['description']}")
            return 0
        
        # Check demo packages
        if package_name in self.DEMO_PACKAGES:
            info = self.DEMO_PACKAGES[package_name]
            print(f"📦 {package_name}")
            print(f"   Version: {info['version']}")
            print(f"   Description: {info['description']}")
            print(f"   Author: {info.get('author', 'Unknown')}")
            return 0
        
        print(f"❌ Package not found: {package_name}")
        return 1

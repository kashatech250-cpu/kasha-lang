"""
KashaLang Setup Script
The African-inspired programming language
"""

from setuptools import setup, find_packages
import os

# Read README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Read version from core module
with open("core/__init__.py", "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break
    else:
        version = "1.0.0"

setup(
    name="kashalang",
    version=version,
    author="KashaLang Team",
    author_email="hello@kashalang.dev",
    description="An African-inspired programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://kashalang.dev",
    project_urls={
        "Bug Reports": "https://github.com/kashalang/kashalang/issues",
        "Source": "https://github.com/kashalang/kashalang",
        "Documentation": "https://kashalang.dev/docs",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Compilers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=5.0.0",
            "black>=22.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "mkdocs>=1.4.0",
            "mkdocs-material>=8.5.0",
        ],
        "build": [
            "build>=0.9.0",
            "pyinstaller>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "kasha=cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.kasha", "*.md", "*.txt", "*.yml", "*.yaml"],
    },
    zip_safe=False,
    keywords=[
        "programming-language",
        "interpreter",
        "african",
        "kinyarwanda",
        "swahili",
        "education",
        "beginner-friendly",
    ],
)

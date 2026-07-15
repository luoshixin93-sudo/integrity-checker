from setuptools import setup, find_packages

setup(
    name="integrity-checker",
    version="0.1.0",
    description="Android SafetyNet & Play Integrity CLI checker",
    author="Android Cloud Tools",
    url="https://github.com/luoshixin93-sudo/integrity-checker",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
        "requests>=2.28.0",
        "pyyaml>=6.0",
        "flask>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "integrity-checker=integrity_checker.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Monitoring",
    ],
)

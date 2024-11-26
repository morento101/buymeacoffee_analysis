from setuptools import setup, find_packages

setup(
    name="bmac-analyzer",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.31.0",
        "pandas>=2.1.0",
        "python-dateutil>=2.8.2",
        "typing-extensions>=4.8.0",
        "click>=8.1.7",
        "rich>=13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "bmac=bmac_analyzer.cli:cli",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Buy Me a Coffee Creator Stats Analyzer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bmac-analyzer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
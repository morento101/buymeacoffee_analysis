# Buy Me a Coffee Creator Stats Analyzer

A command-line tool for analyzing creator statistics from Buy Me a Coffee profiles. Get insights into supporter patterns, coffee contributions, and temporal trends for any Buy Me a Coffee creator.

![CLI Demo](demo.gif)

## Features

- 🖥️ Easy-to-use command-line interface
- 📊 Comprehensive statistics gathering
- 📈 Temporal analysis of support patterns
- 💾 Smart caching system for faster repeated queries
- 🎨 Beautiful terminal output with rich formatting
- 📝 Multiple output formats (table/JSON)
- 🔄 Automatic pagination handling

## Installation

### From Source
```bash
# Clone the repository
git clone https://github.com/yourusername/buymeacoffee-analyzer.git
cd buymeacoffee-analyzer

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install the package
pip install -e .
```

### From PyPI (Coming Soon)
```bash
pip install bmac-analyzer
```

## Usage

### Quick Start
```bash
# Get stats for a creator
bmac stats kqlsearch

# Get JSON output
bmac stats kqlsearch --format json

# Force fresh data fetch
bmac stats kqlsearch --no-cache
```

### Available Commands

#### `bmac stats`
Get statistics for a Buy Me a Coffee creator
```bash
# Basic usage
bmac stats <creator-id>

# Options
--format, -f [table|json]  # Output format (default: table)
--no-cache                 # Bypass cache and fetch fresh data
```

#### `bmac cache`
Manage cache for a specific creator
```bash
# View cache info
bmac cache <creator-id>

# Clear cache for creator
bmac cache <creator-id> --clear
```

#### `bmac clear-all`
Clear all cached data
```bash
bmac clear-all
```

### Example Output

```
📊 Statistics for kqlsearch
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Metric                ┃ Value         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ Total Supporters      │ 42           │
│ Total Coffees         │ 87           │
│ Average Per Supporter │ 2.07         │
│ First Support         │ 2024-01-23   │
│ Last Support          │ 2024-10-20   │
│ Days Active          │ 271          │
└────────────────────────┴───────────────┘
...
```

## Cache System

The tool includes a smart caching system to improve performance and reduce API calls:

- Cache Location: `~/.bmac-cache/`
- Default TTL: 1 hour
- Automatic cache invalidation
- Cache management commands

### Cache Management
```bash
# Check cache status for a creator
bmac cache kqlsearch

# Clear specific creator's cache
bmac cache kqlsearch --clear

# Clear all cached data
bmac clear-all
```

## Data Structure

The tool returns data in the following structure:

```json
{
    "summary": {
        "total_supporters": int,
        "total_coffees": int,
        "average_coffees_per_supporter": float,
        "first_support": "YYYY-MM-DD",
        "last_support": "YYYY-MM-DD",
        "days_active": int
    },
    "support_patterns": {
        "coffee_distribution": {
            "1": int,
            "2": int,
            "3": int
        },
        "supporters_with_messages": int,
        "message_rate": "XX.X%",
        "creator_supporters": int
    },
    "monthly_trends": {
        "best_month": {
            "date": "YYYY-MM",
            "coffees": int
        },
        "worst_month": {
            "date": "YYYY-MM",
            "coffees": int
        },
        "monthly_averages": {
            "supporters": float,
            "coffees": float
        }
    }
}
```

## Configuration

The tool uses these default settings:
- Cache TTL: 3600 seconds (1 hour)
- Cache Location: `~/.bmac-cache/`
- Output Format: table
- Page Size: 10 items

## Development

### Project Structure
```
buymeacoffee_analysis/
├── README.md
├── requirements.txt
├── setup.py
└── bmac_analyzer/
    ├── __init__.py
    ├── analyzer.py
    └── cli.py
```

### Setting Up Development Environment
```bash
# Clone the repository
git clone https://github.com/yourusername/buymeacoffee-analyzer.git
cd buymeacoffee-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .
```

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Areas for Improvement
- Add unit tests
- Implement data visualization features
- Add export functionality
- Enhance error handling
- Add configuration file support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is not officially affiliated with Buy Me a Coffee. It uses their public API for data analysis purposes. Please ensure you comply with Buy Me a Coffee's terms of service when using this tool.

## Support

If you find this tool useful, consider:

- ⭐ Star the repository
- 🐛 Report issues
- 🤝 Contribute to the codebase
- 📢 Share with others

## Credits

Created with ❤️ using:
- [Click](https://click.palletsprojects.com/)
- [Rich](https://rich.readthedocs.io/)
- [Pandas](https://pandas.pydata.org/)
- [Requests](https://requests.readthedocs.io/)

For questions or support, please open an issue in the GitHub repository.
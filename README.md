# Buy Me a Coffee Creator Stats Analyzer

A Python tool for analyzing creator statistics from Buy Me a Coffee profiles. This tool provides comprehensive insights into supporter patterns, coffee contributions, and temporal trends for any Buy Me a Coffee creator.

## Features

- 📊 Comprehensive statistics gathering
- 📈 Temporal analysis of support patterns
- 💬 Message and engagement analysis
- 📅 Monthly trend analysis
- 🔄 Automatic pagination handling

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/buymeacoffee-analyzer.git
cd buymeacoffee-analyzer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from bmac_analyzer import BuyMeACoffeeAnalyzer

# Initialize analyzer with creator ID
analyzer = BuyMeACoffeeAnalyzer("creator-id")

# Get comprehensive stats
stats = analyzer.analyze_stats()

# Access specific metrics
print(f"Total Supporters: {stats['summary']['total_supporters']}")
print(f"Total Coffees: {stats['summary']['total_coffees']}")
```

### Output Example

The analyzer provides statistics in the following categories:

1. Summary Statistics:
   - Total supporters
   - Total coffees received
   - Average coffees per supporter
   - First and last support dates
   - Days active

2. Support Patterns:
   - Distribution of coffee quantities
   - Message engagement rates
   - Creator supporter count

3. Monthly Trends:
   - Best and worst performing months
   - Monthly averages
   - Support frequency patterns

## Data Structure

The tool returns a dictionary with the following structure:

```python
{
    "summary": {
        "total_supporters": int,
        "total_coffees": int,
        "average_coffees_per_supporter": float,
        "first_support": str,
        "last_support": str,
        "days_active": int
    },
    "support_patterns": {
        "coffee_distribution": dict,
        "supporters_with_messages": int,
        "message_rate": str,
        "creator_supporters": int
    },
    "monthly_trends": {
        "best_month": {
            "date": str,
            "coffees": int
        },
        "worst_month": {
            "date": str,
            "coffees": int
        },
        "monthly_averages": {
            "supporters": float,
            "coffees": float
        }
    }
}
```

## Contributing

Contributions are welcome! Here are some ways you can contribute:

1. Report bugs
2. Suggest new features
3. Submit pull requests
4. Improve documentation

## Future Enhancements

- [ ] Sentiment analysis of supporter messages
- [ ] Data visualization capabilities
- [ ] Export functionality (CSV/Excel)
- [ ] Day/time pattern analysis
- [ ] API rate limiting and caching
- [ ] Command-line interface

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is not officially affiliated with Buy Me a Coffee. It uses their public API for data analysis purposes. Please ensure you comply with Buy Me a Coffee's terms of service when using this tool.

## Support

If you find this tool useful, consider:

- Star the repository
- Report issues
- Contribute to the codebase
- Share with others who might find it helpful

For questions or support, please open an issue in the GitHub repository.
import requests
from datetime import datetime
import pandas as pd
from collections import Counter
from typing import Dict, List, Any
import json


class BuyMeACoffeeAnalyzer:
    def __init__(self, creator_id: str):
        self.creator_id = creator_id
        self.base_url = "https://app.buymeacoffee.com/api/creators/slug"
        self.all_supporters = []

    def fetch_data(self, page: int = 1, per_page: int = 10) -> Dict:
        """Fetch data from Buy Me a Coffee API"""
        url = f"{self.base_url}/{self.creator_id}/coffees"
        params = {
            "web": 1,
            "page": page,
            "per_page": per_page
        }
        response = requests.get(url, params=params)
        return response.json()

    def fetch_all_pages(self) -> List[Dict]:
        """Fetch all pages of supporter data"""
        page = 1
        while True:
            data = self.fetch_data(page=page)
            self.all_supporters.extend(data['data'])

            if not data['links']['next']:
                break
            page += 1
        return self.all_supporters

    def analyze_stats(self) -> Dict[str, Any]:
        """Analyze supporter statistics"""
        if not self.all_supporters:
            self.fetch_all_pages()

        # Convert timestamps to datetime objects
        for supporter in self.all_supporters:
            supporter['support_created_on'] = datetime.strptime(
                supporter['support_created_on'].split('.')[0],
                '%Y-%m-%dT%H:%M:%S'
            )

        # Basic stats
        total_supporters = len(self.all_supporters)
        total_coffees = sum(s['support_coffees'] for s in self.all_supporters)

        # Time-based analysis
        support_dates = [s['support_created_on'] for s in self.all_supporters]
        first_support = min(support_dates)
        last_support = max(support_dates)

        # Support distribution
        coffee_counts = Counter(s['support_coffees'] for s in self.all_supporters)

        # Message analysis
        messages_with_notes = [s for s in self.all_supporters if s.get('support_note')]

        # Supporter types
        creator_supporters = [s for s in self.all_supporters if s.get('supporter_role_is_creator')]

        # Monthly trends
        df = pd.DataFrame(self.all_supporters)
        monthly_stats = (
            df.groupby(df['support_created_on'].dt.strftime('%Y-%m'))
            .agg({
                'id': 'count',
                'support_coffees': 'sum'
            })
            .rename(columns={'id': 'supporters', 'support_coffees': 'coffees'})
        )

        best_month = monthly_stats['coffees'].idxmax()
        worst_month = monthly_stats['coffees'].idxmin()

        return {
            "summary": {
                "total_supporters": total_supporters,
                "total_coffees": total_coffees,
                "average_coffees_per_supporter": round(total_coffees / total_supporters, 2),
                "first_support": first_support.strftime('%Y-%m-%d'),
                "last_support": last_support.strftime('%Y-%m-%d'),
                "days_active": (last_support - first_support).days
            },
            "support_patterns": {
                "coffee_distribution": dict(coffee_counts),
                "supporters_with_messages": len(messages_with_notes),
                "message_rate": f"{(len(messages_with_notes) / total_supporters) * 100:.1f}%",
                "creator_supporters": len(creator_supporters)
            },
            "monthly_trends": {
                "best_month": {
                    "date": best_month,
                    "coffees": monthly_stats.loc[best_month, 'coffees']
                },
                "worst_month": {
                    "date": worst_month,
                    "coffees": monthly_stats.loc[worst_month, 'coffees']
                },
                "monthly_averages": {
                    "supporters": monthly_stats['supporters'].mean(),
                    "coffees": monthly_stats['coffees'].mean()
                }
            }
        }


def main():
    # Example usage
    creator_id = "kqlsearch"

    analyzer = BuyMeACoffeeAnalyzer(creator_id)
    stats = analyzer.analyze_stats()

    # Pretty print the results
    print(f"\n📊 Buy Me a Coffee Stats for creator: {creator_id}")
    print("\n🎯 Summary:")
    for key, value in stats['summary'].items():
        print(f"  - {key.replace('_', ' ').title()}: {value}")

    print("\n👥 Support Patterns:")
    for key, value in stats['support_patterns'].items():
        print(f"  - {key.replace('_', ' ').title()}: {value}")

    print("\n📈 Monthly Trends:")
    trends = stats['monthly_trends']
    print(f"  - Best Month: {trends['best_month']['date']} ({trends['best_month']['coffees']} coffees)")
    print(f"  - Worst Month: {trends['worst_month']['date']} ({trends['worst_month']['coffees']} coffees)")
    print(f"  - Average Monthly Supporters: {trends['monthly_averages']['supporters']:.1f}")
    print(f"  - Average Monthly Coffees: {trends['monthly_averages']['coffees']:.1f}")


if __name__ == "__main__":
    main()
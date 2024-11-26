import requests
from datetime import datetime
import pandas as pd
from collections import Counter
from typing import Dict, List, Any, Optional
import json
from pathlib import Path
import time


class BuyMeACoffeeAnalyzer:
    def __init__(self, creator_id: str, use_cache: bool = True, cache_ttl: int = 3600):
        self.creator_id = creator_id
        self.base_url = "https://app.buymeacoffee.com/api/creators/slug"
        self.all_supporters = []
        self.use_cache = use_cache
        self.cache_ttl = cache_ttl  # Cache TTL in seconds
        self.cache_dir = Path.home() / ".bmac-cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self) -> Path:
        """Get the cache file path for the current creator"""
        return self.cache_dir / f"{self.creator_id}.json"

    def _save_to_cache(self, data: List[Dict]) -> None:
        """Save data to cache with timestamp"""
        cache_data = {
            "timestamp": time.time(),
            "data": data
        }
        with open(self._get_cache_path(), 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

    def _load_from_cache(self) -> Optional[List[Dict]]:
        """Load data from cache if it exists and is not expired"""
        cache_path = self._get_cache_path()
        if not cache_path.exists():
            return None

        with open(cache_path, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)

        # Check if cache is expired
        if time.time() - cache_data["timestamp"] > self.cache_ttl:
            return None

        return cache_data["data"]

    def fetch_data(self, page: int = 1, per_page: int = 10) -> Dict:
        """Fetch data from Buy Me a Coffee API"""
        url = f"{self.base_url}/{self.creator_id}/coffees"
        params = {
            "web": 1,
            "page": page,
            "per_page": per_page
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch data: {str(e)}")

    def fetch_all_pages(self) -> List[Dict]:
        """Fetch all pages of supporter data with caching"""
        # Try to load from cache first
        if self.use_cache:
            cached_data = self._load_from_cache()
            if cached_data is not None:
                self.all_supporters = cached_data
                return self.all_supporters

        # Fetch fresh data if cache is disabled or expired
        page = 1
        self.all_supporters = []

        while True:
            data = self.fetch_data(page=page)
            self.all_supporters.extend(data['data'])

            if not data['links']['next']:
                break
            page += 1

        # Save to cache if enabled
        if self.use_cache:
            self._save_to_cache(self.all_supporters)

        return self.all_supporters

    def analyze_stats(self) -> Dict[str, Any]:
        """Analyze supporter statistics"""
        if not self.all_supporters:
            self.fetch_all_pages()

        try:
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
        except Exception as e:
            raise Exception(f"Failed to analyze stats: {str(e)}")
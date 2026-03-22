import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

channels = ['Email', 'Paid Social', 'Organic Social', 'Paid Search', 'Display Ads']
campaign_types = ['Brand Awareness', 'Lead Generation', 'Retargeting', 'Seasonal Promo', 'Product Launch']
regions = ['West', 'East', 'South', 'Midwest', 'International']

rows = []
start_date = datetime(2024, 1, 1)

for i in range(5000):
    channel = random.choice(channels)
    campaign_type = random.choice(campaign_types)
    region = random.choice(regions)
    date = start_date + timedelta(days=random.randint(0, 364))

    spend_ranges = {
        'Email': (50, 500),
        'Paid Social': (200, 3000),
        'Organic Social': (0, 100),
        'Paid Search': (300, 5000),
        'Display Ads': (100, 2000)
    }
    spend = round(random.uniform(*spend_ranges[channel]), 2)

    impressions = random.randint(1000, 500000)
    clicks = int(impressions * random.uniform(0.005, 0.08))
    conversions = int(clicks * random.uniform(0.02, 0.15))
    revenue = round(conversions * random.uniform(20, 200), 2)

    ctr = round(clicks / impressions * 100, 4) if impressions > 0 else 0
    conversion_rate = round(conversions / clicks * 100, 4) if clicks > 0 else 0

    cpa = round(spend / conversions, 2)
    roas = round(revenue / spend, 2)

    rows.append({
        'campaign_id': i + 1,
        'date': date.strftime('%Y-%m-%d'),
        'channel': channel,
        'campaign_type': campaign_type,
        'region': region,
        'impressions': impressions,
        'clicks': clicks,
        'conversions': conversions,
        'spend': spend,
        'revenue': revenue,
        'ctr': ctr,
        'conversion_rate': conversion_rate,
        'cpa': cpa,
        'roas': roas
    })

df = pd.DataFrame(rows)

df.to_csv('data/marketing_data.csv', index=False, sep=';')
print(f"Dataset created: {len(df)} rows")
print(df.head())
print(f"\nTotal spend: ${df['spend'].sum():,.2f}")
print(f"Total revenue: ${df['revenue'].sum():,.2f}")
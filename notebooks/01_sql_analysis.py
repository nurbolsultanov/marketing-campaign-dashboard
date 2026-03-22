import pandas as pd
import sqlite3

# Load data
df = pd.read_csv('data/marketing_data.csv')
conn = sqlite3.connect(':memory:')
df.to_sql('campaigns', conn, index=False)

print("=== 1. OVERALL PERFORMANCE ===")
print(pd.read_sql("""
    SELECT
        COUNT(*) AS total_campaigns,
        ROUND(SUM(spend), 2) AS total_spend,
        ROUND(SUM(revenue), 2) AS total_revenue,
        ROUND(SUM(revenue) / SUM(spend), 2) AS overall_roas,
        ROUND(AVG(ctr), 4) AS avg_ctr,
        ROUND(AVG(conversion_rate), 4) AS avg_conversion_rate,
        SUM(impressions) AS total_impressions,
        SUM(clicks) AS total_clicks,
        SUM(conversions) AS total_conversions
    FROM campaigns
""", conn))

print("\n=== 2. PERFORMANCE BY CHANNEL ===")
print(pd.read_sql("""
    SELECT
        channel,
        COUNT(*) AS campaigns,
        ROUND(SUM(spend), 2) AS total_spend,
        ROUND(SUM(revenue), 2) AS total_revenue,
        ROUND(SUM(revenue) / SUM(spend), 2) AS roas,
        ROUND(AVG(ctr), 4) AS avg_ctr,
        ROUND(AVG(conversion_rate), 4) AS avg_conversion_rate,
        ROUND(AVG(cpa), 2) AS avg_cpa
    FROM campaigns
    GROUP BY channel
    ORDER BY roas DESC
""", conn))

print("\n=== 3. PERFORMANCE BY CAMPAIGN TYPE ===")
print(pd.read_sql("""
    SELECT
        campaign_type,
        COUNT(*) AS campaigns,
        ROUND(SUM(spend), 2) AS total_spend,
        ROUND(SUM(revenue), 2) AS total_revenue,
        ROUND(SUM(revenue) / SUM(spend), 2) AS roas,
        ROUND(AVG(conversion_rate), 4) AS avg_conversion_rate
    FROM campaigns
    GROUP BY campaign_type
    ORDER BY roas DESC
""", conn))

print("\n=== 4. PERFORMANCE BY REGION ===")
print(pd.read_sql("""
    SELECT
        region,
        COUNT(*) AS campaigns,
        ROUND(SUM(spend), 2) AS total_spend,
        ROUND(SUM(revenue), 2) AS total_revenue,
        ROUND(SUM(revenue) / SUM(spend), 2) AS roas
    FROM campaigns
    GROUP BY region
    ORDER BY total_revenue DESC
""", conn))

print("\n=== 5. MONTHLY TREND ===")
print(pd.read_sql("""
    SELECT
        SUBSTR(date, 1, 7) AS month,
        COUNT(*) AS campaigns,
        ROUND(SUM(spend), 2) AS total_spend,
        ROUND(SUM(revenue), 2) AS total_revenue,
        ROUND(SUM(revenue) / SUM(spend), 2) AS roas
    FROM campaigns
    GROUP BY SUBSTR(date, 1, 7)
    ORDER BY month
""", conn))

print("\n=== 6. TOP 10 CAMPAIGNS BY ROAS ===")
print(pd.read_sql("""
    SELECT
        campaign_id,
        date,
        channel,
        campaign_type,
        region,
        ROUND(spend, 2) AS spend,
        ROUND(revenue, 2) AS revenue,
        ROUND(roas, 2) AS roas
    FROM campaigns
    ORDER BY roas DESC
    LIMIT 10
""", conn))

print("\n=== 7. BEST CHANNEL + CAMPAIGN TYPE COMBO ===")
print(pd.read_sql("""
    SELECT
        channel,
        campaign_type,
        COUNT(*) AS campaigns,
        ROUND(AVG(roas), 2) AS avg_roas,
        ROUND(SUM(revenue), 2) AS total_revenue
    FROM campaigns
    GROUP BY channel, campaign_type
    ORDER BY avg_roas DESC
    LIMIT 10
""", conn))

conn.close()
print("\nSQL analysis complete.")
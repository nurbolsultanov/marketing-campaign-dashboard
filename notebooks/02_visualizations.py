import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Load data
df = pd.read_csv('data/marketing_data.csv')
conn = sqlite3.connect(':memory:')
df.to_sql('campaigns', conn, index=False)

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Marketing Campaign Performance Dashboard', fontsize=16, fontweight='bold')

# Plot 1 - ROAS by Channel
channel_roas = pd.read_sql("""
    SELECT channel, ROUND(SUM(revenue)/SUM(spend), 2) AS roas
    FROM campaigns GROUP BY channel ORDER BY roas DESC
""", conn)
axes[0,0].bar(channel_roas['channel'], channel_roas['roas'], color='steelblue')
axes[0,0].set_title('ROAS by Channel')
axes[0,0].set_xlabel('Channel')
axes[0,0].set_ylabel('ROAS')
axes[0,0].tick_params(axis='x', rotation=30)
for i, v in enumerate(channel_roas['roas']):
    axes[0,0].text(i, v + 10, f'{v:.0f}x', ha='center', fontsize=9)

# Plot 2 - Revenue by Campaign Type
camp_rev = pd.read_sql("""
    SELECT campaign_type, ROUND(SUM(revenue)/1000000, 2) AS revenue_m
    FROM campaigns GROUP BY campaign_type ORDER BY revenue_m DESC
""", conn)
axes[0,1].bar(camp_rev['campaign_type'], camp_rev['revenue_m'], color='darkorange')
axes[0,1].set_title('Total Revenue by Campaign Type ($M)')
axes[0,1].set_xlabel('Campaign Type')
axes[0,1].set_ylabel('Revenue ($M)')
axes[0,1].tick_params(axis='x', rotation=30)
for i, v in enumerate(camp_rev['revenue_m']):
    axes[0,1].text(i, v + 0.2, f'${v:.1f}M', ha='center', fontsize=9)

# Plot 3 - Monthly Revenue Trend
monthly = pd.read_sql("""
    SELECT SUBSTR(date,1,7) AS month,
    ROUND(SUM(revenue)/1000000, 2) AS revenue_m,
    ROUND(SUM(spend)/1000, 2) AS spend_k
    FROM campaigns GROUP BY SUBSTR(date,1,7) ORDER BY month
""", conn)
axes[0,2].plot(monthly['month'], monthly['revenue_m'], marker='o', color='seagreen', linewidth=2)
axes[0,2].set_title('Monthly Revenue Trend ($M)')
axes[0,2].set_xlabel('Month')
axes[0,2].set_ylabel('Revenue ($M)')
axes[0,2].tick_params(axis='x', rotation=45)

# Plot 4 - CTR by Channel
channel_ctr = pd.read_sql("""
    SELECT channel, ROUND(AVG(ctr), 4) AS avg_ctr
    FROM campaigns GROUP BY channel ORDER BY avg_ctr DESC
""", conn)
axes[1,0].bar(channel_ctr['channel'], channel_ctr['avg_ctr'], color='mediumpurple')
axes[1,0].set_title('Avg CTR by Channel (%)')
axes[1,0].set_xlabel('Channel')
axes[1,0].set_ylabel('CTR (%)')
axes[1,0].tick_params(axis='x', rotation=30)
for i, v in enumerate(channel_ctr['avg_ctr']):
    axes[1,0].text(i, v + 0.02, f'{v:.2f}%', ha='center', fontsize=9)

# Plot 5 - Spend vs Revenue by Region
region_data = pd.read_sql("""
    SELECT region,
    ROUND(SUM(spend)/1000, 2) AS spend_k,
    ROUND(SUM(revenue)/1000000, 2) AS revenue_m
    FROM campaigns GROUP BY region ORDER BY revenue_m DESC
""", conn)
x = range(len(region_data))
width = 0.35
axes[1,1].bar([i - width/2 for i in x], region_data['spend_k'], width, label='Spend ($K)', color='tomato')
axes[1,1].bar([i + width/2 for i in x], region_data['revenue_m']*100, width, label='Revenue ($100K)', color='steelblue')
axes[1,1].set_title('Spend vs Revenue by Region')
axes[1,1].set_xticks(list(x))
axes[1,1].set_xticklabels(region_data['region'], rotation=30)
axes[1,1].legend()

# Plot 6 - Conversion Rate by Campaign Type
conv_rate = pd.read_sql("""
    SELECT campaign_type, ROUND(AVG(conversion_rate), 4) AS avg_conv_rate
    FROM campaigns GROUP BY campaign_type ORDER BY avg_conv_rate DESC
""", conn)
axes[1,2].bar(conv_rate['campaign_type'], conv_rate['avg_conv_rate'], color='dodgerblue')
axes[1,2].set_title('Avg Conversion Rate by Campaign Type (%)')
axes[1,2].set_xlabel('Campaign Type')
axes[1,2].set_ylabel('Conversion Rate (%)')
axes[1,2].tick_params(axis='x', rotation=30)
for i, v in enumerate(conv_rate['avg_conv_rate']):
    axes[1,2].text(i, v + 0.02, f'{v:.2f}%', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('data/campaign_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved to data/campaign_analysis.png")
conn.close()
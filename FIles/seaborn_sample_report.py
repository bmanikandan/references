import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import matplotlib.image as mpimg
from urllib.request import urlretrieve
import os

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Generate sample data
np.random.seed(42)
n_samples = 1000

# Sales data
data = {
    'month': np.random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], n_samples),
    'product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], n_samples),
    'region': np.random.choice(['North', 'South', 'East', 'West'], n_samples),
    'sales': np.random.normal(1000, 300, n_samples),
    'profit_margin': np.random.uniform(0.1, 0.4, n_samples),
    'customer_satisfaction': np.random.normal(4.2, 0.8, n_samples)
}

df = pd.DataFrame(data)
df['sales'] = np.abs(df['sales'])  # Ensure positive sales values
df['customer_satisfaction'] = np.clip(df['customer_satisfaction'], 1, 5)  # Clip to 1-5 range

print("Sample Sales Report - Data Analysis with Seaborn")
print("=" * 50)
print(f"Dataset Overview:")
print(f"Total records: {len(df)}")
print(f"Date range: {df['month'].nunique()} months")
print(f"Products: {df['product'].nunique()}")
print(f"Regions: {df['region'].nunique()}")
print()

# Function to create PNC-style logo placeholder
def create_pnc_logo_placeholder():
    """Create a simple PNC logo placeholder"""
    fig_logo = plt.figure(figsize=(2, 0.8))
    ax = fig_logo.add_subplot(111)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    
    # PNC colors: Blue (#004977) and Gold (#F5A623)
    # Create stylized "PNC" text
    ax.text(5, 2, 'PNC', fontsize=24, fontweight='bold', 
           ha='center', va='center', color='#004977')
    
    # Add a gold underline
    ax.plot([2, 8], [1, 1], color='#F5A623', linewidth=4)
    
    ax.axis('off')
    fig_logo.patch.set_facecolor('white')
    
    # Save as temporary image
    logo_path = 'temp_pnc_logo.png'
    fig_logo.savefig(logo_path, bbox_inches='tight', dpi=150, 
                    facecolor='white', edgecolor='none')
    plt.close(fig_logo)
    return logo_path

# Create PNC logo
logo_path = create_pnc_logo_placeholder()

# Create PDF filename with timestamp
pdf_filename = f"PNC_sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

# Create a comprehensive report with multiple visualizations
with PdfPages(pdf_filename) as pdf:
    fig = plt.figure(figsize=(16, 20))

    # 1. Sales Distribution by Product
    plt.subplot(4, 2, 1)
    sns.boxplot(data=df, x='product', y='sales', hue='product', palette='Set2', legend=False)
    plt.title('Sales Distribution by Product', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)

    # 2. Monthly Sales Trend
    plt.subplot(4, 2, 2)
    monthly_sales = df.groupby('month')['sales'].mean().reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])
    sns.barplot(x=monthly_sales.index, y=monthly_sales.values, hue=monthly_sales.index, palette='viridis', legend=False)
    plt.title('Average Sales by Month', fontsize=14, fontweight='bold')
    plt.ylabel('Average Sales')

    # 3. Regional Performance Heatmap
    plt.subplot(4, 2, 3)
    regional_data = df.pivot_table(values='sales', index='region', columns='product', aggfunc='mean')
    sns.heatmap(regional_data, annot=True, fmt='.0f', cmap='YlOrRd')
    plt.title('Average Sales by Region and Product', fontsize=14, fontweight='bold')

    # 4. Profit Margin vs Sales Scatter Plot
    plt.subplot(4, 2, 4)
    sns.scatterplot(data=df, x='sales', y='profit_margin', hue='region', alpha=0.6)
    plt.title('Sales vs Profit Margin by Region', fontsize=14, fontweight='bold')
    plt.xlabel('Sales')
    plt.ylabel('Profit Margin')

    # 5. Customer Satisfaction Distribution
    plt.subplot(4, 2, 5)
    sns.histplot(data=df, x='customer_satisfaction', bins=20, kde=True, color='skyblue')
    plt.title('Customer Satisfaction Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Customer Satisfaction (1-5)')
    plt.ylabel('Frequency')

    # 6. Product Performance Comparison
    plt.subplot(4, 2, 6)
    product_metrics = df.groupby('product').agg({
        'sales': 'mean',
        'profit_margin': 'mean',
        'customer_satisfaction': 'mean'
    }).reset_index()

    x_pos = np.arange(len(product_metrics))
    width = 0.25

    plt.bar(x_pos - width, product_metrics['sales']/100, width, label='Sales (÷100)', alpha=0.8)
    plt.bar(x_pos, product_metrics['profit_margin']*10, width, label='Profit Margin (×10)', alpha=0.8)
    plt.bar(x_pos + width, product_metrics['customer_satisfaction'], width, label='Customer Satisfaction', alpha=0.8)

    plt.xlabel('Products')
    plt.ylabel('Normalized Values')
    plt.title('Product Performance Comparison', fontsize=14, fontweight='bold')
    plt.xticks(x_pos, product_metrics['product'], rotation=45)
    plt.legend()

    # 7. Correlation Matrix
    plt.subplot(4, 2, 7)
    numeric_cols = ['sales', 'profit_margin', 'customer_satisfaction']
    correlation_matrix = df[numeric_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, square=True)
    plt.title('Correlation Matrix', fontsize=14, fontweight='bold')

    # 8. Sales by Region and Month
    plt.subplot(4, 2, 8)
    region_month_sales = df.groupby(['region', 'month'])['sales'].mean().reset_index()
    sns.lineplot(data=region_month_sales, x='month', y='sales', hue='region', marker='o')
    plt.title('Sales Trends by Region and Month', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)

    plt.tight_layout(pad=3.0)
    plt.suptitle('Comprehensive Sales Analysis Report', fontsize=18, fontweight='bold', y=0.995)
    
    # Add PNC logo to the top right corner of the chart page
    if os.path.exists(logo_path):
        try:
            logo_img = mpimg.imread(logo_path)
            # Create an inset axes for the logo
            logo_ax = fig.add_axes([0.85, 0.96, 0.12, 0.04])  # [x, y, width, height]
            logo_ax.imshow(logo_img)
            logo_ax.axis('off')
        except Exception as e:
            print(f"Could not load logo: {e}")
    
    # Save to PDF
    pdf.savefig(fig, bbox_inches='tight')
    
    # Create a summary page
    fig_summary = plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    
    # Add PNC logo to the summary page header
    if os.path.exists(logo_path):
        try:
            logo_img = mpimg.imread(logo_path)
            # Create an inset axes for the logo at the top left
            logo_ax_summary = fig_summary.add_axes([0.05, 0.95, 0.2, 0.05])
            logo_ax_summary.imshow(logo_img)
            logo_ax_summary.axis('off')
        except Exception as e:
            print(f"Could not load logo for summary: {e}")
    
    # Report title and metadata
    plt.text(0.5, 0.95, 'Sales Analysis Report', ha='center', va='top', 
             fontsize=20, fontweight='bold', color='#004977', transform=fig_summary.transFigure)
    
    plt.text(0.5, 0.90, f'Generated on: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}', 
             ha='center', va='top', fontsize=12, transform=fig_summary.transFigure)
    
    # Dataset overview
    overview_text = f"""
Dataset Overview:
• Total Records: {len(df):,}
• Time Period: {df['month'].nunique()} months
• Products Analyzed: {df['product'].nunique()}
• Regions Covered: {df['region'].nunique()}
"""
    
    plt.text(0.1, 0.80, overview_text, ha='left', va='top', fontsize=12,
             transform=fig_summary.transFigure, bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue"))
    
    # Key insights
    insights_text = f"""
Key Business Insights:
• Top Performing Product: {df.groupby('product')['sales'].mean().idxmax()}
• Best Performing Region: {df.groupby('region')['sales'].mean().idxmax()}
• Average Customer Satisfaction: {df['customer_satisfaction'].mean():.2f}/5.0
• Peak Profit Margin: {df['profit_margin'].max():.2%}
• Total Sales Volume: ${df['sales'].sum():,.2f}
• Average Sales per Transaction: ${df['sales'].mean():.2f}
"""
    
    plt.text(0.1, 0.60, insights_text, ha='left', va='top', fontsize=12,
             transform=fig_summary.transFigure, bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen"))
    
    # Recommendations
    recommendations_text = """
Recommendations:
• Focus marketing efforts on top-performing products
• Investigate success factors in best-performing regions
• Address customer satisfaction in underperforming areas
• Optimize pricing strategies for better profit margins
• Consider seasonal trends in sales planning
"""
    
    plt.text(0.1, 0.35, recommendations_text, ha='left', va='top', fontsize=12,
             transform=fig_summary.transFigure, bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"))
    
    # Footer
    plt.text(0.5, 0.05, 'Generated with Python, Pandas, Seaborn, and Matplotlib', 
             ha='center', va='bottom', fontsize=10, style='italic',
             transform=fig_summary.transFigure)
    
    pdf.savefig(fig_summary, bbox_inches='tight')
    
    plt.show()
    plt.close('all')

# Summary Statistics
print("\nKey Insights:")
print("-" * 30)
print(f"Top performing product: {df.groupby('product')['sales'].mean().idxmax()}")
print(f"Best region: {df.groupby('region')['sales'].mean().idxmax()}")
print(f"Average customer satisfaction: {df['customer_satisfaction'].mean():.2f}/5.0")
print(f"Highest profit margin: {df['profit_margin'].max():.2%}")
print(f"Total sales volume: ${df['sales'].sum():,.2f}")

# Clean up temporary logo file
if os.path.exists(logo_path):
    os.remove(logo_path)

# Save the report data for future reference
df.to_csv('sales_report_data.csv', index=False)
print(f"\nData saved to: sales_report_data.csv")
print(f"PDF report saved to: {pdf_filename}")
print("Report generated successfully!")
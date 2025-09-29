import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page configuration - MUST be first
st.set_page_config(
    page_title="Zomato Analytics Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_excel('cleaned_zomato.xlsx')

df = load_data()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #E23744;
    }
    .powerbi-container {
        border: 2px solid #E23744;
        border-radius: 10px;
        padding: 10px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🍽️ Zomato Analytics Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Dashboard Navigation")
page = st.sidebar.selectbox("Select Analysis", [
    "Overview", 
    "Top 10", 
    "Restaurant Analytics", 
    "Customer Insights",
    "Performance Metrics"
])

if page == "Overview":
    st.header("📈 Executive Summary")
    
    # Key metrics from actual data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Restaurants", f"{df['name'].nunique():,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_rating = df['rate'].mean() if 'rate' in df.columns else 0
        st.metric("Avg Rating", f"{avg_rating:.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_cities = df['location'].nunique() if 'location' in df.columns else 0
        st.metric("Locations", f"{total_cities}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_cost = df['approx_cost(for two people)'].mean() if 'approx_cost(for two people)' in df.columns else 0
        st.metric("Avg Cost (2 people)", f"₹{avg_cost:.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Power BI Dashboard Integration
    st.markdown('<div class="powerbi-container">', unsafe_allow_html=True)
    
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiZDAxN2VjOTUtZTI1Yy00ZjU1LWJjNDItZDgzNjVlMDdlYmYyIiwidCI6ImFlODc0N2EyLThhM2UtNGIyMi1iM2MyLTdlZjlhNDk0ZGZhMyJ9&pageName=4b4382c4a5eb392e094c"
    
    st.components.v1.iframe(
        src=powerbi_url,
        width=680,
        height=400,
        scrolling=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info("💡 **Tip**: Use the filters and interactive elements in the Power BI dashboard above to explore different aspects of the Zomato business data.")
    
    # Business Insights
    st.markdown("### 📊 Key Business Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📈 KPI Insights:**
        - **Total Restaurants**: Measures market penetration and platform scale
        - **Average Rating**: Indicates overall customer satisfaction and service quality
        - **Total Votes**: Shows customer engagement and platform activity levels
        - **Average Cost**: Helps position pricing strategy and target market segments
        """)
        
        st.markdown("""
        **🔄 Digital Adoption:**
        - **Online Orders %**: Critical for revenue growth and delivery expansion
        - **Table Booking %**: Indicates dine-in market capture and reservation system adoption
        """)
    
    with col2:
        st.markdown("""
        **🎯 Strategic Applications:**
        - **Market Expansion**: Use restaurant density data to identify underserved areas
        - **Partner Onboarding**: Target high-rating locations for premium partnerships
        - **Revenue Optimization**: Focus on increasing online order adoption rates
        - **Customer Experience**: Monitor rating trends to maintain service standards
        """)
        
        st.markdown("""
        **📍 Geographic & Cuisine Intelligence:**
        - **Top Locations**: Prioritize marketing spend in high-density restaurant areas
        - **Popular Cuisines**: Align promotional campaigns with customer preferences
        - **Cost Analysis**: Optimize commission structures based on price segments
        """)
    
    st.markdown("---")
    
    st.markdown("""
    **🚀 Actionable Business Outcomes:**
    
    1. **Revenue Growth**: Increase online order penetration from current % to 80%+ target
    2. **Market Leadership**: Maintain average rating above 4.0 across all restaurant categories
    3. **Expansion Strategy**: Focus on cities with high restaurant density but low Zomato presence
    4. **Partner Success**: Support restaurants in premium segments to drive higher order values
    5. **Customer Retention**: Use rating distribution insights to improve low-performing restaurant partnerships
    """)

elif page == "Top 10":
    st.header("📊 Top 10 Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Cuisines")
        if 'cuisines' in df.columns:
            cuisine_counts = df['cuisines'].value_counts().head(10)
            fig = px.bar(x=cuisine_counts.values, y=cuisine_counts.index, 
                        orientation='h', title="Top 10 Cuisines",
                        color_discrete_sequence=["#E23744"])
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Restaurant Distribution")
        if 'location' in df.columns:
            location_counts = df['location'].value_counts().head(10)
            fig = px.pie(values=location_counts.values, names=location_counts.index, 
                        title="Top 10 Locations",
                        color_discrete_sequence=px.colors.sequential.Reds_r)
            st.plotly_chart(fig, use_container_width=True)

elif page == "Restaurant Analytics":
    st.header("🏪 Restaurant Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⭐ Rating Distribution")
        if 'rate' in df.columns:
            fig = px.histogram(df, x='rate', nbins=20, 
                             title="Restaurant Rating Distribution",
                             color_discrete_sequence=["#FFFFFF"])
            fig.update_traces(marker_line_color='black', marker_line_width=1)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Cost Analysis")
        if 'approx_cost(for two people)' in df.columns:
            fig = px.box(df, y='approx_cost(for two people)', 
                        title="Cost Distribution (for 2 people)")
            st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🏆 Top Rated Restaurants")
    if 'name' in df.columns and 'rate' in df.columns:
        top_rated = df.nlargest(10, 'rate')[['name', 'rate', 'location', 'cuisines']]
        st.dataframe(top_rated, use_container_width=True)

elif page == "Customer Insights":
    st.header("👥 Customer Behavior Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🍽️ Restaurant Types")
        if 'rest_type' in df.columns:
            rest_type_counts = df['rest_type'].value_counts().head(8)
            fig = px.bar(x=rest_type_counts.values, y=rest_type_counts.index,
                        orientation='h', title="Restaurant Types",
                        color_discrete_sequence=["#E23744"])
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Cost vs Rating")
        if 'approx_cost(for two people)' in df.columns and 'rate' in df.columns:
            fig = px.scatter(df.sample(500), x='approx_cost(for two people)', y='rate',
                           title="Cost vs Rating Relationship",
                           color_discrete_sequence=["#E23744"])
            st.plotly_chart(fig, use_container_width=True)
    
    if 'online_order' in df.columns:
        st.subheader("📱 Order & Booking Analysis")
        online_stats = df['online_order'].value_counts()
        col1, col2 = st.columns(2)
        
        with col1:
            color_map = {'Yes': 'white', 'No': '#E23744'}
            fig = px.pie(values=online_stats.values, names=online_stats.index,
                        title="Online Order Distribution",
                        color=online_stats.index,
                        color_discrete_map=color_map)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'book_table' in df.columns:
                booking_stats = df['book_table'].value_counts()
                fig = px.pie(values=booking_stats.values, names=booking_stats.index,
                            title="Table Booking Distribution",
                            color=booking_stats.index,
                            color_discrete_map=color_map)
                st.plotly_chart(fig, use_container_width=True)

elif page == "Performance Metrics":
    st.header("📊 Data Insights & Analytics")
    
    st.subheader("📍 Location Performance")
    if 'location' in df.columns and 'rate' in df.columns:
        location_stats = df.groupby('location').agg({
            'rate': 'mean',
            'approx_cost(for two people)': 'mean',
            'name': 'count'
        }).round(2).sort_values('rate', ascending=False).head(10)
        location_stats.columns = ['Avg Rating', 'Avg Cost', 'Restaurant Count']
        st.dataframe(location_stats, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Cuisine Performance")
        if 'cuisines' in df.columns and 'rate' in df.columns:
            cuisine_ratings = df.groupby('cuisines')['rate'].mean().sort_values(ascending=False).head(10)
            fig = px.bar(x=cuisine_ratings.values, y=cuisine_ratings.index,
                        orientation='h', title="Top Cuisines by Rating",
                        color_discrete_sequence=["#E23744"])
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💸 Premium vs Budget")
        if 'approx_cost(for two people)' in df.columns:
            df_cost = df.copy()
            df_cost['cost_category'] = pd.cut(df_cost['approx_cost(for two people)'], 
                                            bins=[0, 500, 1000, 2000, float('inf')],
                                            labels=['Budget', 'Mid-range', 'Premium', 'Luxury'])
            cost_dist = df_cost['cost_category'].value_counts()
            fig = px.pie(values=cost_dist.values, names=cost_dist.index,
                        title="Restaurant Categories by Cost",
                        color_discrete_sequence=px.colors.sequential.Reds)
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🍽️ Zomato Analytics Dashboard | Built with Streamlit | Last Updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)
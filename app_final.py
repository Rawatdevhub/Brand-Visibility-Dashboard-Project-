import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Brand Visibility Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #172554;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    color: #64748b;
    margin-bottom: 30px;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    color: #172554;
    margin-top: 25px;
    margin-bottom: 15px;
}

div[data-testid="stMetric"] {
    background: white;
    border-radius: 15px;
    padding: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0px 8px 25px rgba(0,0,0,0.10);
}

.sidebar-title {
    font-size: 22px;
    font-weight: 700;
}

.insight-box {
    padding: 18px;
    border-radius: 12px;
    background-color: white;
    border-left: 5px solid #2563eb;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.06);
    margin-bottom: 15px;
}

.footer {
    text-align: center;
    padding: 30px;
    color: #64748b;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    data = pd.read_csv("brand_clean_dataset.csv")

    numeric_columns = [
        "price",
        "rating",
        "reviews",
        "delivery_days"
    ]

    for column in numeric_columns:

        if column in data.columns:

            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

    return data


df = load_data()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📊 Brand Visibility Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive marketplace intelligence platform for analyzing '
    'product visibility, pricing, ratings, reviews, delivery and performance.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    '<div class="sidebar-title">🎛️ Dashboard Filters</div>',
    unsafe_allow_html=True
)

st.sidebar.write(
    "Use the filters below to explore marketplace performance."
)


# Platform Filter

platforms = ["All"]

if "platform" in df.columns:

    platforms += sorted(
        df["platform"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


selected_platform = st.sidebar.selectbox(
    "Select Platform",
    platforms,
    index=0,
    key="platform_filter"
)


# Keyword Filter

keywords = ["All"]

if "keyword" in df.columns:

    keywords += sorted(
        df["keyword"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


selected_keyword = st.sidebar.selectbox(
    "Select Keyword",
    keywords,
    index=0,
    key="keyword_filter"
)


# Reset Information

st.sidebar.markdown("---")

st.sidebar.info(
    "💡 Change the filters to dynamically update "
    "all KPIs and charts."
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if selected_platform != "All":

    filtered_df = filtered_df[
        filtered_df["platform"] == selected_platform
    ]


if selected_keyword != "All":

    filtered_df = filtered_df[
        filtered_df["keyword"] == selected_keyword
    ]


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_products = len(filtered_df)

avg_price = filtered_df["price"].mean()

avg_rating = filtered_df["rating"].mean()

total_reviews = filtered_df["reviews"].sum()


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📦 Total Products",
        f"{total_products:,}"
    )


with col2:

    st.metric(
        "💰 Average Price",
        f"₹{avg_price:,.0f}"
        if pd.notna(avg_price)
        else "N/A"
    )


with col3:

    st.metric(
        "⭐ Average Rating",
        f"{avg_rating:.2f}"
        if pd.notna(avg_rating)
        else "N/A"
    )


with col4:

    st.metric(
        "💬 Total Reviews",
        f"{total_reviews:,.0f}"
        if pd.notna(total_reviews)
        else "N/A"
    )


# =========================================================
# NO DATA CHECK
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No products match the selected filters."
    )

    st.stop()


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "🏠 Executive Summary",
        "📊 Marketplace Overview",
        "🏆 Product Performance",
        "🏷️ Brand Analysis",
        "💰 Pricing Analysis",
        "🚚 Delivery Analysis",
        "📥 Reports & Data"
    ]
)


# =========================================================
# TAB 1 — EXECUTIVE SUMMARY
# =========================================================

with tab1:

    st.markdown(
        '<div class="section-title">🎯 Executive Summary</div>',
        unsafe_allow_html=True
    )

    st.write(
        "A high-level overview of marketplace visibility, "
        "customer engagement, pricing and product performance."
    )

    # =====================================================
    # EXECUTIVE SUMMARY KPIs
    # =====================================================

    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

    # Market Leader
    platform_counts = (
        filtered_df["platform"]
        .value_counts()
    )

    market_leader = (
        platform_counts.idxmax()
        if not platform_counts.empty
        else "N/A"
    )

    market_leader_count = (
        platform_counts.max()
        if not platform_counts.empty
        else 0
    )

    # Best Rated Platform
    rating_by_platform = (
        filtered_df
        .groupby("platform")["rating"]
        .mean()
        .dropna()
    )

    best_rated_platform = (
        rating_by_platform.idxmax()
        if not rating_by_platform.empty
        else "N/A"
    )

    best_rating = (
        rating_by_platform.max()
        if not rating_by_platform.empty
        else 0
    )

    # Most Visible Keyword
    keyword_counts = (
        filtered_df["keyword"]
        .value_counts()
    )

    top_keyword = (
        keyword_counts.idxmax()
        if not keyword_counts.empty
        else "N/A"
    )

    top_keyword_count = (
        keyword_counts.max()
        if not keyword_counts.empty
        else 0
    )

    # Most Reviewed Product
    review_df = filtered_df.dropna(
        subset=["reviews"]
    )

    if not review_df.empty:

        most_reviewed_product = review_df.loc[
            review_df["reviews"].idxmax(),
            "title"
        ]

        most_reviewed_count = review_df["reviews"].max()

    else:

        most_reviewed_product = "N/A"
        most_reviewed_count = 0


    # KPI 1
    with summary_col1:

        st.metric(
            "🏆 Market Leader",
            market_leader,
            f"{market_leader_count:,} products"
        )


    # KPI 2
    with summary_col2:

        st.metric(
            "⭐ Best Rated Platform",
            best_rated_platform,
            f"{best_rating:.2f} ⭐"
        )


    # KPI 3
    with summary_col3:

        st.metric(
            "🔎 Top Search Keyword",
            top_keyword,
            f"{top_keyword_count:,} products"
        )


    # KPI 4
    with summary_col4:

        st.metric(
            "💬 Most Reviewed Product",
            f"{most_reviewed_count:,.0f}",
            "Reviews"
        )


    # =====================================================
    # PLATFORM VISIBILITY CHART
    # =====================================================

    st.markdown(
        '<div class="section-title">📊 Platform Visibility</div>',
        unsafe_allow_html=True
    )

    platform_counts_df = (
        platform_counts
        .reset_index()
    )

    platform_counts_df.columns = [
        "Platform",
        "Product Count"
    ]


    fig_platform = px.bar(
        platform_counts_df,
        x="Platform",
        y="Product Count",
        color="Platform",
        text="Product Count",
        hover_data={
            "Platform": True,
            "Product Count": ":,"
        },
        title="📊 Product Visibility Across Marketplaces"
    )


    fig_platform.update_traces(
        hovertemplate=
        "<b>%{x}</b><br>"
        "Products: %{y:,}<extra></extra>"
    )


    fig_platform.update_layout(
        template="plotly_white",
        title_x=0.5,
        height=450,
        showlegend=False
    )


    st.plotly_chart(
        fig_platform,
        use_container_width=True,
        key="summary_platform_chart_v2"
    )


    # =====================================================
    # BUSINESS INSIGHTS
    # =====================================================

    st.markdown(
        '<div class="section-title">💡 Key Management Takeaways</div>',
        unsafe_allow_html=True
    )


    insight_col1, insight_col2 = st.columns(2)


    # Insight 1
    with insight_col1:

        st.info(
            f"""
            🏆 **Marketplace Leadership**

            **{market_leader}** currently has the highest product
            visibility in the filtered dataset with **{market_leader_count:,}
            products**.

            This indicates stronger marketplace presence and product
            availability compared with other platforms.
            """
        )


    # Insight 2
    with insight_col2:

        st.success(
            f"""
            ⭐ **Customer Satisfaction**

            **{best_rated_platform}** has the highest average rating
            of **{best_rating:.2f} ⭐**.

            This suggests that products listed on this platform are
            receiving stronger customer satisfaction signals.
            """
        )


    # Insight 3
    with insight_col1:

        st.warning(
            f"""
            🔎 **Search Visibility**

            The keyword **"{top_keyword}"** generates the highest product
            visibility with **{top_keyword_count:,} products**.

            Brands targeting this keyword may have greater marketplace
            exposure but could also face stronger competition.
            """
        )


  # Insight 4
with insight_col2:

    st.error(
        f"""
💬 **Customer Engagement**

The most reviewed product has received approximately
**{most_reviewed_count:,.0f} reviews**.

High review volume can indicate stronger customer engagement,
product popularity and marketplace traction.
"""
    )
    

    # =====================================================
    # STRATEGIC RECOMMENDATION
    # =====================================================

    st.markdown(
        '<div class="section-title">🚀 Strategic Recommendation</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="insight-box">

        <b>📌 Recommended Business Strategy</b>

        <br><br>

        Focus on increasing product visibility on <b>{market_leader}</b>,
        while using the strong customer satisfaction performance of
        <b>{best_rated_platform}</b> as a benchmark.

        <br><br>

        For search optimization, prioritize the keyword
        <b>"{top_keyword}"</b> while monitoring competition and product
        positioning.

        <br><br>

        The combination of <b>visibility + customer ratings + review volume</b>
        should be used to identify high-potential products and marketplace
        opportunities.

        </div>
        """,
        unsafe_allow_html=True
    )

    # Platform Performance

    platform_counts = (
        filtered_df["platform"]
        .value_counts()
        .reset_index()
    )

    platform_counts.columns = [
        "Platform",
        "Product Count"
    ]


    fig_platform = px.bar(
        platform_counts,
        x="Platform",
        y="Product Count",
        text="Product Count",
        title="📊 Product Visibility by Platform"
    )

    fig_platform.update_layout(
        template="plotly_white",
        title_x=0.5
    )


    st.plotly_chart(
        fig_platform,
        use_container_width=True,
        key="summary_platform_chart"
    )


    # Insights

    st.markdown(
        '<div class="section-title">💡 Business Insights</div>',
        unsafe_allow_html=True
    )


    price_by_platform = (
        filtered_df
        .groupby("platform")["price"]
        .mean()
        .dropna()
    )


    if not price_by_platform.empty:

        highest_price_platform = price_by_platform.idxmax()

        highest_price = price_by_platform.max()

        st.info(
            f"💰 **Pricing Insight:** "
            f"{highest_price_platform} has the highest average "
            f"product price at **₹{highest_price:,.0f}**."
        )


    keyword_counts = (
        filtered_df["keyword"]
        .value_counts()
    )


    if not keyword_counts.empty:

        top_keyword = keyword_counts.idxmax()

        top_keyword_count = keyword_counts.max()

        st.success(
            f"🔎 **Visibility Insight:** "
            f"**{top_keyword}** is the most visible search keyword "
            f"with **{top_keyword_count:,} products**."
        )


if filtered_df["reviews"].notna().any():

    most_reviewed = filtered_df.loc[
        filtered_df["reviews"].idxmax()
    ]

    st.warning(
        f"💬 **Customer Engagement:** "
        f"**{most_reviewed['title']}** has the highest review volume "
        f"with **{most_reviewed['reviews']:,.0f} reviews**."
    )

    st.metric(
        "💬 Most Reviewed Product",
        f"{most_reviewed['reviews']:,.0f}",
        "Reviews"
    )

# =========================================================
# TAB 2 — MARKETPLACE OVERVIEW
# =========================================================

with tab2:

    st.markdown(
        '<div class="section-title">📊 Marketplace Overview</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Compare marketplace performance across product visibility, "
        "pricing, customer ratings and review engagement."
    )


    # =====================================================
    # PLATFORM PERFORMANCE DATA
    # =====================================================

    platform_comparison = (
        filtered_df
        .groupby("platform")
        .agg(
            Average_Price=("price", "mean"),
            Average_Rating=("rating", "mean"),
            Total_Reviews=("reviews", "sum"),
            Product_Count=("title", "count")
        )
        .reset_index()
    )


    # =====================================================
    # PLATFORM SCORECARD
    # =====================================================

    st.markdown(
        '<div class="section-title">🏆 Platform Performance Scorecard</div>',
        unsafe_allow_html=True
    )


    score_col1, score_col2, score_col3, score_col4 = st.columns(4)


    # Best visibility platform

    visibility_platform = (
        platform_comparison
        .sort_values(
            "Product_Count",
            ascending=False
        )
        .iloc[0]
    )


    # Best rated platform

    rating_platform = (
        platform_comparison
        .sort_values(
            "Average_Rating",
            ascending=False
        )
        .iloc[0]
    )


    # Most reviewed platform

    reviews_platform = (
        platform_comparison
        .sort_values(
            "Total_Reviews",
            ascending=False
        )
        .iloc[0]
    )


    # Lowest average price

    price_platform = (
        platform_comparison
        .sort_values(
            "Average_Price",
            ascending=True
        )
        .iloc[0]
    )


    # =====================================================
    # SCORECARD 1
    # =====================================================

    with score_col1:

        st.metric(
            "📦 Highest Visibility",
            visibility_platform["platform"],
            f"{visibility_platform['Product_Count']:,.0f} products"
        )


    # =====================================================
    # SCORECARD 2
    # =====================================================

    with score_col2:

        st.metric(
            "⭐ Best Rated",
            rating_platform["platform"],
            f"{rating_platform['Average_Rating']:.2f} ⭐"
        )


    # =====================================================
    # SCORECARD 3
    # =====================================================

    with score_col3:

        st.metric(
            "💬 Most Reviews",
            reviews_platform["platform"],
            f"{reviews_platform['Total_Reviews']:,.0f} reviews"
        )


    # =====================================================
    # SCORECARD 4
    # =====================================================

    with score_col4:

        st.metric(
            "💰 Lowest Avg. Price",
            price_platform["platform"],
            f"₹{price_platform['Average_Price']:,.0f}"
        )


    # =====================================================
    # PLATFORM DATA TABLE
    # =====================================================

    st.markdown(
        '<div class="section-title">📋 Detailed Platform Comparison</div>',
        unsafe_allow_html=True
    )


    display_platform = platform_comparison.copy()


    display_platform["Average_Price"] = (
        display_platform["Average_Price"]
        .round(0)
    )


    display_platform["Average_Rating"] = (
        display_platform["Average_Rating"]
        .round(2)
    )


    display_platform["Total_Reviews"] = (
        display_platform["Total_Reviews"]
        .round(0)
    )


    display_platform.columns = [
        "Platform",
        "Average Price (₹)",
        "Average Rating",
        "Total Reviews",
        "Product Count"
    ]


    st.dataframe(
        display_platform,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # CHART 1 — PRODUCT VISIBILITY
    # =====================================================

    st.markdown(
        '<div class="section-title">📦 Product Visibility by Platform</div>',
        unsafe_allow_html=True
    )


    fig_visibility_overview = px.bar(
        platform_comparison,
        x="platform",
        y="Product_Count",
        color="platform",
        text="Product_Count",
        hover_data={
            "platform": True,
            "Product_Count": ":,"
        },
        title="📦 Number of Products Listed on Each Platform"
    )


    fig_visibility_overview.update_traces(
        hovertemplate=
        "<b>%{x}</b><br>"
        "Products: %{y:,}<extra></extra>"
    )


    fig_visibility_overview.update_layout(
        template="plotly_white",
        title_x=0.5,
        height=450,
        showlegend=False
    )


    st.plotly_chart(
        fig_visibility_overview,
        use_container_width=True,
        key="overview_visibility_v3"
    )


    # =====================================================
    # CHART 2 — RATING VS PRICE
    # =====================================================

    chart_col1, chart_col2 = st.columns(2)


    with chart_col1:

        fig_rating_overview = px.bar(
            platform_comparison,
            x="platform",
            y="Average_Rating",
            color="platform",
            text="Average_Rating",
            title="⭐ Average Customer Rating"
        )


        fig_rating_overview.update_traces(
            texttemplate="%{text:.2f} ⭐",
            textposition="outside"
        )


        fig_rating_overview.update_layout(
            template="plotly_white",
            title_x=0.5,
            yaxis_range=[0, 5.5],
            showlegend=False
        )


        st.plotly_chart(
            fig_rating_overview,
            use_container_width=True,
            key="overview_rating_v3"
        )


    with chart_col2:

        fig_price_overview = px.bar(
            platform_comparison,
            x="platform",
            y="Average_Price",
            color="platform",
            text="Average_Price",
            title="💰 Average Product Price"
        )


        fig_price_overview.update_traces(
            texttemplate="₹%{text:,.0f}",
            textposition="outside"
        )


        fig_price_overview.update_layout(
            template="plotly_white",
            title_x=0.5,
            showlegend=False
        )


        st.plotly_chart(
            fig_price_overview,
            use_container_width=True,
            key="overview_price_v3"
        )


    # =====================================================
    # CHART 3 — REVIEW ENGAGEMENT
    # =====================================================

    st.markdown(
        '<div class="section-title">💬 Customer Engagement</div>',
        unsafe_allow_html=True
    )


    fig_reviews_overview = px.bar(
        platform_comparison,
        x="platform",
        y="Total_Reviews",
        color="platform",
        text="Total_Reviews",
        title="💬 Total Customer Reviews by Platform"
    )


    fig_reviews_overview.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )


    fig_reviews_overview.update_layout(
        template="plotly_white",
        title_x=0.5,
        showlegend=False,
        height=450
    )


    st.plotly_chart(
        fig_reviews_overview,
        use_container_width=True,
        key="overview_reviews_v3"
    )


    # =====================================================
    # MANAGEMENT RECOMMENDATION
    # =====================================================

    st.markdown(
        '<div class="section-title">💡 Management Recommendation</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="insight-box">

        🏆 <b>Visibility:</b>
        <b>{visibility_platform['platform']}</b> leads in product visibility
        with <b>{visibility_platform['Product_Count']:,.0f}</b> products.

        <br><br>

        ⭐ <b>Customer Satisfaction:</b>
        <b>{rating_platform['platform']}</b> has the strongest average rating
        at <b>{rating_platform['Average_Rating']:.2f} ⭐</b>.

        <br><br>

        💬 <b>Customer Engagement:</b>
        <b>{reviews_platform['platform']}</b> generates the highest review
        volume with <b>{reviews_platform['Total_Reviews']:,.0f}</b> reviews.

        <br><br>

        💰 <b>Pricing Opportunity:</b>
        <b>{price_platform['platform']}</b> has the lowest average product
        price at approximately <b>₹{price_platform['Average_Price']:,.0f}</b>.

        </div>
        """,
        unsafe_allow_html=True
    )
# =========================================================
# TAB 3 — PRODUCT PERFORMANCE
# =========================================================

with tab3:

    st.markdown(
        '<div class="section-title">🏆 Product Performance</div>',
        unsafe_allow_html=True
    )


    product_df = filtered_df.dropna(
        subset=["title", "rating", "reviews"]
    ).copy()


    # Top by Reviews

    top_reviews = (
        product_df
        .sort_values(
            "reviews",
            ascending=False
        )
        .head(10)
    )


    fig_top_reviews = px.bar(
        top_reviews,
        x="reviews",
        y="title",
        color="platform",
        orientation="h",
        title="💬 Top 10 Products by Review Volume"
    )


    fig_top_reviews.update_layout(
        template="plotly_white",
        title_x=0.5,
        yaxis={
            "categoryorder": "total ascending"
        }
    )


    st.plotly_chart(
        fig_top_reviews,
        use_container_width=True,
        key="products_top_reviews_chart"
    )


    # Top Rated Products

    top_rating = (
        product_df
        .sort_values(
            ["rating", "reviews"],
            ascending=[False, False]
        )
        .head(10)
    )


    fig_top_rating = px.bar(
        top_rating,
        x="rating",
        y="title",
        color="platform",
        orientation="h",
        title="⭐ Top 10 Highest Rated Products"
    )


    fig_top_rating.update_layout(
        template="plotly_white",
        title_x=0.5,
        xaxis_range=[0, 5],
        yaxis={
            "categoryorder": "total ascending"
        }
    )


    st.plotly_chart(
        fig_top_rating,
        use_container_width=True,
        key="products_top_rating_chart"
    )


    # Price vs Rating

    scatter_df = filtered_df.dropna(
        subset=["price", "rating"]
    )


    fig_scatter = px.scatter(
        scatter_df,
        x="price",
        y="rating",
        color="platform",
        size="reviews",
        hover_data=[
            "keyword",
            "title"
        ],
        title="💰 Price vs ⭐ Rating"
    )


    fig_scatter.update_layout(
        template="plotly_white",
        title_x=0.5
    )


    st.plotly_chart(
        fig_scatter,
        use_container_width=True,
        key="products_price_rating_chart"
    )


# =========================================================
# TAB 4 — BRAND / KEYWORD ANALYSIS
# =========================================================

with tab4:

    st.markdown(
        '<div class="section-title">🏷️ Brand & Keyword Analysis</div>',
        unsafe_allow_html=True
    )


    # Keyword Visibility

    keyword_visibility = (
        filtered_df["keyword"]
        .value_counts()
        .reset_index()
    )


    keyword_visibility.columns = [
        "Keyword",
        "Product Count"
    ]


    fig_keyword = px.bar(
        keyword_visibility,
        x="Keyword",
        y="Product Count",
        color="Product Count",
        text="Product Count",
        title="🔎 Product Visibility by Search Keyword"
    )


    fig_keyword.update_layout(
        template="plotly_white",
        title_x=0.5,
        xaxis_tickangle=-45
    )


    st.plotly_chart(
        fig_keyword,
        use_container_width=True,
        key="brand_keyword_visibility_chart"
    )


    # Keyword Table

    st.subheader("🔍 Keyword Performance")


    st.dataframe(
        keyword_visibility,
        use_container_width=True,
        hide_index=True
    )


    # Platform Keyword Matrix

    keyword_platform = pd.crosstab(
        filtered_df["keyword"],
        filtered_df["platform"]
    )


    fig_heatmap = px.imshow(
        keyword_platform,
        text_auto=True,
        aspect="auto",
        title="🔥 Keyword Visibility Across Platforms"
    )


    fig_heatmap.update_layout(
        template="plotly_white",
        title_x=0.5
    )


    st.plotly_chart(
        fig_heatmap,
        use_container_width=True,
        key="brand_keyword_heatmap"
    )


# =========================================================
# TAB 5 — PRICING ANALYSIS
# =========================================================

with tab5:

    st.markdown(
        '<div class="section-title">💰 Pricing Analysis</div>',
        unsafe_allow_html=True
    )


    # Price Distribution

    fig_price_distribution = px.histogram(
        filtered_df,
        x="price",
        nbins=30,
        title="💰 Product Price Distribution",
        labels={
            "price": "Price (₹)"
        }
    )


    fig_price_distribution.update_layout(
        template="plotly_white",
        title_x=0.5
    )


    st.plotly_chart(
        fig_price_distribution,
        use_container_width=True,
        key="pricing_distribution_chart"
    )


    # Platform Price Comparison

    price_platform = (
        filtered_df
        .groupby("platform")["price"]
        .mean()
        .reset_index()
    )


    fig_price_compare = px.bar(
        price_platform,
        x="platform",
        y="price",
        color="platform",
        text_auto=".0f",
        title="🏪 Average Price Comparison"
    )


    fig_price_compare.update_layout(
        template="plotly_white",
        title_x=0.5
    )


    st.plotly_chart(
        fig_price_compare,
        use_container_width=True,
        key="pricing_platform_chart"
    )


    # Price Statistics

    price_col1, price_col2, price_col3 = st.columns(3)


    with price_col1:

        st.metric(
            "Lowest Price",
            f"₹{filtered_df['price'].min():,.0f}"
        )


    with price_col2:

        st.metric(
            "Average Price",
            f"₹{filtered_df['price'].mean():,.0f}"
        )


    with price_col3:

        st.metric(
            "Highest Price",
            f"₹{filtered_df['price'].max():,.0f}"
        )


# =========================================================
# TAB 6 — DELIVERY ANALYSIS
# =========================================================

with tab6:

    st.markdown(
        '<div class="section-title">🚚 Delivery Performance</div>',
        unsafe_allow_html=True
    )


    if "delivery_days" in filtered_df.columns:

        delivery_df = (
            filtered_df
            .groupby("delivery_days")
            .size()
            .reset_index(
                name="Product Count"
            )
        )


        fig_delivery = px.bar(
            delivery_df,
            x="delivery_days",
            y="Product Count",
            text="Product Count",
            title="🚚 Products by Delivery Time"
        )


        fig_delivery.update_layout(
            template="plotly_white",
            title_x=0.5
        )


        st.plotly_chart(
            fig_delivery,
            use_container_width=True,
            key="delivery_days_chart"
        )


        # Delivery by Platform

        delivery_platform = (
            filtered_df
            .groupby("platform")["delivery_days"]
            .mean()
            .reset_index()
        )


        fig_delivery_platform = px.bar(
            delivery_platform,
            x="platform",
            y="delivery_days",
            color="platform",
            text_auto=".1f",
            title="🏪 Average Delivery Days by Platform"
        )


        fig_delivery_platform.update_layout(
            template="plotly_white",
            title_x=0.5
        )


        st.plotly_chart(
            fig_delivery_platform,
            use_container_width=True,
            key="delivery_platform_chart"
        )


        delivery_col1, delivery_col2 = st.columns(2)


        with delivery_col1:

            st.metric(
                "Average Delivery",
                f"{filtered_df['delivery_days'].mean():.1f} Days"
            )


        with delivery_col2:

            st.metric(
                "Fastest Delivery",
                f"{filtered_df['delivery_days'].min():.0f} Days"
            )


    else:

        st.warning(
            "Delivery data is not available in the dataset."
        )


# =========================================================
# TAB 7 — REPORTS & DATA
# =========================================================

with tab7:

    st.markdown(
        '<div class="section-title">📥 Reports & Data</div>',
        unsafe_allow_html=True
    )


    # Platform Summary

    st.subheader("📊 Platform Performance Summary")


    display_platform = platform_comparison.copy()


    if "Average_Price" in display_platform.columns:

        display_platform["Average_Price"] = (
            display_platform["Average_Price"]
            .round(2)
        )


    if "Average_Rating" in display_platform.columns:

        display_platform["Average_Rating"] = (
            display_platform["Average_Rating"]
            .round(2)
        )


    st.dataframe(
        display_platform,
        use_container_width=True,
        hide_index=True
    )


    # Product Preview

    st.subheader("🛍️ Product Data Preview")


    preview_columns = [
        "keyword",
        "title",
        "price",
        "rating",
        "reviews",
        "platform",
        "delivery"
    ]


    available_columns = [
        column
        for column in preview_columns
        if column in filtered_df.columns
    ]


    st.dataframe(
        filtered_df[
            available_columns
        ].head(30),
        use_container_width=True,
        hide_index=True
    )


    # Download Filtered Data

    filtered_csv = (
        filtered_df
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        label="📥 Download Filtered Dataset",
        data=filtered_csv,
        file_name="filtered_brand_visibility_data.csv",
        mime="text/csv",
        key="download_filtered_data"
    )


    # Download Platform Summary

    platform_csv = (
        platform_comparison
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        label="📊 Download Platform Summary",
        data=platform_csv,
        file_name="platform_performance_summary.csv",
        mime="text/csv",
        key="download_platform_summary"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        📊 Brand Visibility Dashboard
        <br>
        Built with Python • Pandas • Plotly • Streamlit
        <br>
        Interactive Marketplace Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True
)
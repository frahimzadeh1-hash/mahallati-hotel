import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def guest_segmentation(guests_df):
    """تقسیم‌بندی مهمانان بر اساس امتیاز وفاداری"""
    if guests_df.empty:
        return px.pie(title='داده‌ای برای نمایش وجود ندارد')
    
    # تعریف دسته‌بندی
    bins = [0, 30, 50, 70, 100]
    labels = ['کم‌وفادار', 'متوسط', 'وفادار', 'بسیار وفادار']
    guests_df_copy = guests_df.copy()
    guests_df_copy['loyalty_tier'] = pd.cut(guests_df_copy['loyalty_score'], bins=bins, labels=labels, right=True)
    
    # محاسبه تعداد هر دسته
    tier_counts = guests_df_copy['loyalty_tier'].value_counts().reset_index()
    tier_counts.columns = ['level', 'count']
    
    # نمودار دایره‌ای
    fig = px.pie(
        tier_counts, 
        values='count',
        names='level',
        title='توزیع مهمانان بر اساس سطح وفاداری',
        hole=0.4,
        color_discrete_sequence=['#FF6B6B', '#FECA57', '#48DBFB', '#0ABDE3']
    )
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def guest_geography(guests_df):
    """نمودار توزیع جغرافیایی مهمانان"""
    if guests_df.empty:
        return px.bar(title='داده‌ای برای نمایش وجود ندارد')
    
    city_counts = guests_df['city'].value_counts().reset_index()
    city_counts.columns = ['city', 'count']
    
    # مرتب‌سازی بر اساس تعداد
    city_counts = city_counts.sort_values('count', ascending=True)
    
    fig = px.bar(
        city_counts, 
        x='count',
        y='city',
        title='توزیع مهمانان بر اساس شهر',
        color='count',
        color_continuous_scale='Viridis',
        text='count',
        orientation='h'
    )
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>تعداد: %{x}'
    )
    fig.update_layout(
        xaxis_title='تعداد مهمان',
        yaxis_title='شهر',
        height=400,
        yaxis=dict(categoryorder='total ascending')
    )
    return fig

def guest_preferences(guests_df):
    """تحلیل علایق مهمانان"""
    if guests_df.empty:
        return px.bar(title='داده‌ای برای نمایش وجود ندارد')
    
    pref_counts = guests_df['preferences'].value_counts().reset_index()
    pref_counts.columns = ['preference', 'count']
    
    fig = px.bar(
        pref_counts,
        x='preference',
        y='count',
        title='علایق مهمانان',
        color='count',
        color_continuous_scale='Plasma',
        text='count'
    )
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>تعداد: %{y}'
    )
    fig.update_layout(
        xaxis_title='علاقه',
        yaxis_title='تعداد مهمان',
        height=400
    )
    return fig

def top_guests(guests_df, n=10):
    """نمایش وفادارترین مهمانان"""
    if guests_df.empty:
        return pd.DataFrame()
    return guests_df.nlargest(n, 'loyalty_score')[['first_name', 'last_name', 'city', 'loyalty_score', 'preferences']]

def guest_growth_trend(guests_df):
    """نمودار روند رشد مهمانان در طول زمان"""
    if guests_df.empty:
        return px.line(title='داده‌ای برای نمایش وجود ندارد')
    
    guests_df_copy = guests_df.copy()
    guests_df_copy['first_visit'] = pd.to_datetime(guests_df_copy['first_visit'])
    monthly_new = guests_df_copy.groupby(guests_df_copy['first_visit'].dt.to_period('M')).size().reset_index()
    monthly_new.columns = ['month', 'new_guests']
    monthly_new['month'] = monthly_new['month'].astype(str)
    
    fig = px.line(
        monthly_new,
        x='month',
        y='new_guests',
        title='روند جذب مهمانان جدید',
        markers=True,
        line_shape='spline'
    )
    fig.update_traces(
        line=dict(width=3, color='#FF6B6B'),
        marker=dict(size=8, color='#FF6B6B')
    )
    fig.update_layout(
        xaxis_title='ماه',
        yaxis_title='تعداد مهمانان جدید',
        height=350
    )
    return fig

def guest_retention_rate(guests_df):
    """محاسبه نرخ بازگشت مشتریان"""
    if guests_df.empty:
        return 0
    
    returning = len(guests_df[guests_df['total_visits'] > 1])
    total = len(guests_df)
    return (returning / total * 100) if total > 0 else 0import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def guest_segmentation(guests_df):
    """تقسیم‌بندی مهمانان بر اساس امتیاز وفاداری"""
    if guests_df.empty:
        return px.pie(title='داده‌ای برای نمایش وجود ندارد')
    
    # تعریف دسته‌بندی
    bins = [0, 30, 50, 70, 100]
    labels = ['کم‌وفادار', 'متوسط', 'وفادار', 'بسیار وفادار']
    guests_df_copy = guests_df.copy()
    guests_df_copy['loyalty_tier'] = pd.cut(guests_df_copy['loyalty_score'], bins=bins, labels=labels, right=True)
    
    # محاسبه تعداد هر دسته
    tier_counts = guests_df_copy['loyalty_tier'].value_counts().reset_index()
    tier_counts.columns = ['level', 'count']
    
    # نمودار دایره‌ای
    fig = px.pie(
        tier_counts, 
        values='count',
        names='level',
        title='توزیع مهمانان بر اساس سطح وفاداری',
        hole=0.4,
        color_discrete_sequence=['#FF6B6B', '#FECA57', '#48DBFB', '#0ABDE3']
    )
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def guest_geography(guests_df):
    """نمودار توزیع جغرافیایی مهمانان"""
    if guests_df.empty:
        return px.bar(title='داده‌ای برای نمایش وجود ندارد')
    
    city_counts = guests_df['city'].value_counts().reset_index()
    city_counts.columns = ['city', 'count']
    
    # مرتب‌سازی بر اساس تعداد
    city_counts = city_counts.sort_values('count', ascending=True)
    
    fig = px.bar(
        city_counts, 
        x='count',
        y='city',
        title='توزیع مهمانان بر اساس شهر',
        color='count',
        color_continuous_scale='Viridis',
        text='count',
        orientation='h'
    )
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>تعداد: %{x}'
    )
    fig.update_layout(
        xaxis_title='تعداد مهمان',
        yaxis_title='شهر',
        height=400,
        yaxis=dict(categoryorder='total ascending')
    )
    return fig

def guest_preferences(guests_df):
    """تحلیل علایق مهمانان"""
    if guests_df.empty:
        return px.bar(title='داده‌ای برای نمایش وجود ندارد')
    
    pref_counts = guests_df['preferences'].value_counts().reset_index()
    pref_counts.columns = ['preference', 'count']
    
    fig = px.bar(
        pref_counts,
        x='preference',
        y='count',
        title='علایق مهمانان',
        color='count',
        color_continuous_scale='Plasma',
        text='count'
    )
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>تعداد: %{y}'
    )
    fig.update_layout(
        xaxis_title='علاقه',
        yaxis_title='تعداد مهمان',
        height=400
    )
    return fig

def top_guests(guests_df, n=10):
    """نمایش وفادارترین مهمانان"""
    if guests_df.empty:
        return pd.DataFrame()
    return guests_df.nlargest(n, 'loyalty_score')[['first_name', 'last_name', 'city', 'loyalty_score', 'preferences']]

def guest_growth_trend(guests_df):
    """نمودار روند رشد مهمانان در طول زمان"""
    if guests_df.empty:
        return px.line(title='داده‌ای برای نمایش وجود ندارد')
    
    guests_df_copy = guests_df.copy()
    guests_df_copy['first_visit'] = pd.to_datetime(guests_df_copy['first_visit'])
    monthly_new = guests_df_copy.groupby(guests_df_copy['first_visit'].dt.to_period('M')).size().reset_index()
    monthly_new.columns = ['month', 'new_guests']
    monthly_new['month'] = monthly_new['month'].astype(str)
    
    fig = px.line(
        monthly_new,
        x='month',
        y='new_guests',
        title='روند جذب مهمانان جدید',
        markers=True,
        line_shape='spline'
    )
    fig.update_traces(
        line=dict(width=3, color='#FF6B6B'),
        marker=dict(size=8, color='#FF6B6B')
    )
    fig.update_layout(
        xaxis_title='ماه',
        yaxis_title='تعداد مهمانان جدید',
        height=350
    )
    return fig

def guest_retention_rate(guests_df):
    """محاسبه نرخ بازگشت مشتریان"""
    if guests_df.empty:
        return 0
    
    returning = len(guests_df[guests_df['total_visits'] > 1])
    total = len(guests_df)
    return (returning / total * 100) if total > 0 else 0

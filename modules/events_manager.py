import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def events_dashboard(events_df):
    """داشبورد وضعیت ایونت‌ها - دو نمودار"""
    if events_df.empty:
        empty_fig = px.bar(title='داده‌ای برای نمایش وجود ندارد')
        return empty_fig, empty_fig
    
    events_df_copy = events_df.copy()
    events_df_copy['fill_rate'] = (events_df_copy['registered'] / events_df_copy['capacity']) * 100
    events_df_copy = events_df_copy.sort_values('date')
    
    # نمودار ۱: مقایسه ظرفیت و ثبت‌نام
    fig1 = px.bar(
        events_df_copy,
        x='event_name',
        y=['capacity', 'registered'],
        title='وضعیت ثبت‌نام ایونت‌ها',
        barmode='group',
        text_auto=True,
        color_discrete_sequence=['#74B9FF', '#FF7675']
    )
    fig1.update_traces(
        texttemplate='%{y}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>%{data.name}: %{y}'
    )
    fig1.update_layout(
        xaxis_title='نام ایونت',
        yaxis_title='تعداد',
        legend_title='نوع',
        height=350
    )
    
    # نمودار ۲: درصد پر شدن ظرفیت
    fig2 = px.bar(
        events_df_copy,
        x='event_name',
        y='fill_rate',
        title='درصد پر شدن ظرفیت ایونت‌ها',
        color='fill_rate',
        color_continuous_scale=[[0, 'red'], [0.5, 'yellow'], [1, 'green']],
        text='fill_rate',
        range_color=[0, 100]
    )
    fig2.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>پر شدن: %{y:.1f}%'
    )
    fig2.update_layout(
        xaxis_title='نام ایونت',
        yaxis_title='درصد پر شدن',
        height=350,
        yaxis=dict(range=[0, 110])
    )
    
    return fig1, fig2

def event_revenue_analysis(events_df, reservations_df):
    """تحلیل درآمد حاصل از ایونت‌ها"""
    if events_df.empty or reservations_df.empty:
        return px.bar(title='داده‌ای برای نمایش وجود ندارد')
    
    # بررسی رزروهایی که با ایونت همراه بوده‌اند
    event_reservations = reservations_df[reservations_df['has_event'] == True]
    
    if event_reservations.empty:
        return px.bar(title='هیچ رزروی با ایونت همراه نبوده است')
    
    # محاسبه درآمد هر ایونت
    revenue_by_event = event_reservations.groupby('event_name').agg({
        'price_per_night': 'sum',
        'reservation_id': 'count'
    }).reset_index()
    revenue_by_event.columns = ['event', 'total_revenue', 'reservation_count']
    revenue_by_event = revenue_by_event.sort_values('total_revenue', ascending=True)
    
    # تبدیل به میلیون تومان
    revenue_by_event['total_revenue_m'] = revenue_by_event['total_revenue'] / 1000000
    
    fig = px.bar(
        revenue_by_event,
        x='total_revenue_m',
        y='event',
        title='درآمد ایجاد شده توسط هر ایونت (میلیون تومان)',
        color='reservation_count',
        color_continuous_scale='Blues',
        text='total_revenue_m',
        orientation='h'
    )
    fig.update_traces(
        texttemplate='%{text:.1f} میلیون تومان',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>درآمد: %{x:.1f} میلیون تومان<br>تعداد رزرو: %{marker.color}'
    )
    fig.update_layout(
        xaxis_title='درآمد (میلیون تومان)',
        yaxis_title='ایونت',
        height=400,
        yaxis=dict(categoryorder='total ascending')
    )
    return fig

def events_timeline(events_df):
    """نمودار زمانی ایونت‌ها"""
    if events_df.empty:
        return px.scatter(title='داده‌ای برای نمایش وجود ندارد')
    
    events_df_copy = events_df.copy()
    events_df_copy['fill_rate'] = (events_df_copy['registered'] / events_df_copy['capacity']) * 100
    
    fig = px.scatter(
        events_df_copy,
        x='date',
        y='event_name',
        size='registered',
        color='fill_rate',
        title='تقویم ایونت‌ها بر اساس تاریخ',
        color_continuous_scale='RdYlGn',
        range_color=[0, 100],
        hover_data={'capacity': True, 'registered': True}
    )
    fig.update_traces(
        marker=dict(sizemode='area', sizeref=2.*max(events_df_copy['registered'])/(40.**2)),
        hovertemplate='<b>%{y}</b><br>تاریخ: %{x}<br>ثبت‌نام: %{marker.size}'
    )
    fig.update_layout(
        xaxis_title='تاریخ',
        yaxis_title='ایونت',
        height=400
    )
    return fig

def event_category_analysis(events_df):
    """تحلیل ایونت‌ها بر اساس دسته‌بندی"""
    if events_df.empty:
        return px.pie(title='داده‌ای برای نمایش وجود ندارد')
    
    category_stats = events_df.groupby('category').agg({
        'registered': 'sum',
        'capacity': 'sum',
        'event_id': 'count'
    }).reset_index()
    category_stats.columns = ['category', 'total_registered', 'total_capacity', 'event_count']
    category_stats['fill_rate'] = (category_stats['total_registered'] / category_stats['total_capacity']) * 100
    
    fig = px.bar(
        category_stats,
        x='category',
        y='fill_rate',
        title='نرخ پر شدن ظرفیت بر اساس دسته‌بندی ایونت',
        color='event_count',
        text='fill_rate',
        color_continuous_scale='Aggrnyl'
    )
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )
    return figimport pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def events_dashboard(events_df):
    """داشبورد وضعیت ایونت‌ها - دو نمودار"""
    if events_df.empty:
        empty_fig = px.bar(title='داده‌ای برای نمایش وجود ندارد')
        return empty_fig, empty_fig
    
    events_df_copy = events_df.copy()
    events_df_copy['fill_rate'] = (events_df_copy['registered'] / events_df_copy['capacity']) * 100
    events_df_copy = events_df_copy.sort_values('date')
    
    # نمودار ۱: مقایسه ظرفیت و ثبت‌نام
    fig1 = px.bar(
        events_df_copy,
        x='event_name',
        y=['capacity', 'registered'],
        title='وضعیت ثبت‌نام ایونت‌ها',
        barmode='group',
        text_auto=True,
        color_discrete_sequence=['#74B9FF', '#FF7675']
    )
    fig1.update_traces(
        texttemplate='%{y}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>%{data.name}: %{y}'
    )
    fig1.update_layout(
        xaxis_title='نام ایونت',
        yaxis_title='تعداد',
        legend_title='نوع',
        height=350
    )
    
    # نمودار ۲: درصد پر شدن ظرفیت
    fig2 = px.bar(
        events_df_copy,
        x='event_name',
        y='fill_rate',
        title='درصد پر شدن ظرفیت ایونت‌ها',
        color='fill_rate',
        color_continuous_scale=[[0, 'red'], [0.5, 'yellow'], [1, 'green']],
        text='fill_rate',
        range_color=[0, 100]
    )
    fig2.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>پر شدن: %{y:.1f}%'
    )
    fig2.update_layout(
        xaxis_title='نام ایونت',
        yaxis_title='درصد پر شدن',
        height=350,
        yaxis=dict(range=[0, 110])
    )
    
    return fig1, fig2

def event_revenue_analysis(events_df, reservations_df):
    """تحلیل درآمد حاصل از ایونت‌ها"""
    if events_df.empty or reservations_df.empty:
        return px.bar(title='داده‌ای برای نمایش وجود ندارد')
    
    # بررسی رزروهایی که با ایونت همراه بوده‌اند
    event_reservations = reservations_df[reservations_df['has_event'] == True]
    
    if event_reservations.empty:
        return px.bar(title='هیچ رزروی با ایونت همراه نبوده است')
    
    # محاسبه درآمد هر ایونت
    revenue_by_event = event_reservations.groupby('event_name').agg({
        'price_per_night': 'sum',
        'reservation_id': 'count'
    }).reset_index()
    revenue_by_event.columns = ['event', 'total_revenue', 'reservation_count']
    revenue_by_event = revenue_by_event.sort_values('total_revenue', ascending=True)
    
    # تبدیل به میلیون تومان
    revenue_by_event['total_revenue_m'] = revenue_by_event['total_revenue'] / 1000000
    
    fig = px.bar(
        revenue_by_event,
        x='total_revenue_m',
        y='event',
        title='درآمد ایجاد شده توسط هر ایونت (میلیون تومان)',
        color='reservation_count',
        color_continuous_scale='Blues',
        text='total_revenue_m',
        orientation='h'
    )
    fig.update_traces(
        texttemplate='%{text:.1f} میلیون تومان',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>درآمد: %{x:.1f} میلیون تومان<br>تعداد رزرو: %{marker.color}'
    )
    fig.update_layout(
        xaxis_title='درآمد (میلیون تومان)',
        yaxis_title='ایونت',
        height=400,
        yaxis=dict(categoryorder='total ascending')
    )
    return fig

def events_timeline(events_df):
    """نمودار زمانی ایونت‌ها"""
    if events_df.empty:
        return px.scatter(title='داده‌ای برای نمایش وجود ندارد')
    
    events_df_copy = events_df.copy()
    events_df_copy['fill_rate'] = (events_df_copy['registered'] / events_df_copy['capacity']) * 100
    
    fig = px.scatter(
        events_df_copy,
        x='date',
        y='event_name',
        size='registered',
        color='fill_rate',
        title='تقویم ایونت‌ها بر اساس تاریخ',
        color_continuous_scale='RdYlGn',
        range_color=[0, 100],
        hover_data={'capacity': True, 'registered': True}
    )
    fig.update_traces(
        marker=dict(sizemode='area', sizeref=2.*max(events_df_copy['registered'])/(40.**2)),
        hovertemplate='<b>%{y}</b><br>تاریخ: %{x}<br>ثبت‌نام: %{marker.size}'
    )
    fig.update_layout(
        xaxis_title='تاریخ',
        yaxis_title='ایونت',
        height=400
    )
    return fig

def event_category_analysis(events_df):
    """تحلیل ایونت‌ها بر اساس دسته‌بندی"""
    if events_df.empty:
        return px.pie(title='داده‌ای برای نمایش وجود ندارد')
    
    category_stats = events_df.groupby('category').agg({
        'registered': 'sum',
        'capacity': 'sum',
        'event_id': 'count'
    }).reset_index()
    category_stats.columns = ['category', 'total_registered', 'total_capacity', 'event_count']
    category_stats['fill_rate'] = (category_stats['total_registered'] / category_stats['total_capacity']) * 100
    
    fig = px.bar(
        category_stats,
        x='category',
        y='fill_rate',
        title='نرخ پر شدن ظرفیت بر اساس دسته‌بندی ایونت',
        color='event_count',
        text='fill_rate',
        color_continuous_scale='Aggrnyl'
    )
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )
    return fig

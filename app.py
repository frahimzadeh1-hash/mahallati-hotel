import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import numpy as np
import os

# ============================================
# تنظیمات صفحه
# ============================================
st.set_page_config(
    page_title="🏨 بوتیک هتل محلاتی - داشبورد مدیریت",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# تابع تولید داده‌های نمونه
# ============================================
def generate_sample_data():
    """تولید داده‌های نمونه برای ۶ ماه گذشته"""
    
    if not os.path.exists('data'):
        os.makedirs('data')
    
    first_names = ['احمد', 'سارا', 'محمد', 'زهرا', 'علی', 'مریم', 'رضا', 'فاطمه', 
                   'حسین', 'نگار', 'کیان', 'نازنین', 'امیر', 'سپیده', 'مهدی', 'الهه']
    
    last_names = ['محلاتی', 'کریمی', 'حسینی', 'رضوی', 'نوری', 'یزدی', 'شیرازی', 
                  'کاشانی', 'اصفهانی', 'تبریزی', 'فردوسی', 'سهرابی']
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # تولید مهمانان
    guests = []
    for i in range(200):
        guest = {
            'guest_id': f'G{1000+i}',
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'email': f'guest{i}@example.com',
            'phone': f'0912{random.randint(1000000, 9999999)}',
            'city': random.choice(['تهران', 'شیراز', 'اصفهان', 'مشهد', 'تبریز', 'یزد', 'کاشان']),
            'first_visit': random.choice(date_range).strftime('%Y-%m-%d'),
            'total_visits': random.randint(1, 12),
            'preferences': random.choice(['موسیقی', 'شعر', 'فیلم', 'هنر', 'تاریخ', 'غذا']),
            'loyalty_score': round(random.uniform(0, 100), 1)
        }
        guests.append(guest)
    
    guests_df = pd.DataFrame(guests)
    guests_df.to_csv('data/guests.csv', index=False, encoding='utf-8-sig')
    
    # تولید رزروها
    reservations = []
    room_types = ['اتاق سنتی', 'اتاق مدرن', 'سوئیت', 'اتاق خانوادگی']
    event_names = ['شب شعر', 'کنسرت موسیقی', 'تحلیل فیلم', 'کارگاه خوشنویسی', 'شب داستان‌گویی']
    channels = ['Website', 'Booking.com', 'Instagram', 'Phone', 'Walk-in']
    
    for i in range(500):
        check_in = random.choice(date_range)
        stay_days = random.randint(1, 5)
        check_out = check_in + timedelta(days=stay_days)
        
        has_event = random.random() < 0.3
        
        reservation = {
            'reservation_id': f'R{10000+i}',
            'guest_id': f'G{random.randint(1000, 1199)}',
            'check_in': check_in.strftime('%Y-%m-%d'),
            'check_out': check_out.strftime('%Y-%m-%d'),
            'room_type': random.choice(room_types),
            'price_per_night': random.randint(150, 500) * 10000,
            'has_event': has_event,
            'event_name': random.choice(event_names) if has_event else None,
            'channel': random.choice(channels),
            'status': random.choices(['completed', 'cancelled', 'no-show'], weights=[0.7, 0.2, 0.1])[0]
        }
        reservations.append(reservation)
    
    reservations_df = pd.DataFrame(reservations)
    reservations_df.to_csv('data/reservations.csv', index=False, encoding='utf-8-sig')
    
    # تولید ایونت‌ها
    events = []
    event_types = ['شب شعر بهار', 'کنسرت نی', 'تحلیل فیلم سینمایی', 'کارگاه شعر معاصر', 
                   'شب موسیقی سنتی', 'نمایشگاه عکس', 'جشنواره فیلم کوتاه']
    categories = ['موسیقی', 'شعر', 'فیلم', 'هنر']
    
    for i in range(30):
        event_date = random.choice(date_range)
        event = {
            'event_id': f'E{2000+i}',
            'event_name': random.choice(event_types),
            'date': event_date.strftime('%Y-%m-%d'),
            'capacity': random.randint(20, 50),
            'registered': random.randint(10, 45),
            'price': random.randint(50, 200) * 10000,
            'is_paid': random.choice([True, False]),
            'category': random.choice(categories)
        }
        events.append(event)
    
    events_df = pd.DataFrame(events)
    events_df.to_csv('data/events.csv', index=False, encoding='utf-8-sig')
    
    return guests_df, reservations_df, events_df

# ============================================
# توابع بارگذاری داده
# ============================================
def check_data_exists():
    """بررسی وجود فایل‌های داده"""
    required_files = ['guests.csv', 'reservations.csv', 'events.csv']
    data_dir = 'data'
    
    if not os.path.exists(data_dir):
        return False
    
    for file in required_files:
        if not os.path.exists(os.path.join(data_dir, file)):
            return False
    return True

def load_all_data():
    """بارگذاری همه داده‌ها"""
    try:
        guests = pd.read_csv('data/guests.csv', encoding='utf-8-sig')
        reservations = pd.read_csv('data/reservations.csv', encoding='utf-8-sig')
        events = pd.read_csv('data/events.csv', encoding='utf-8-sig')
        
        reservations['check_in'] = pd.to_datetime(reservations['check_in'])
        reservations['check_out'] = pd.to_datetime(reservations['check_out'])
        events['date'] = pd.to_datetime(events['date'])
        
        return guests, reservations, events
    except Exception as e:
        st.error(f"❌ خطا در خواندن داده‌ها: {str(e)}")
        return None, None, None

def calculate_kpis(reservations_df):
    """محاسبه شاخص‌های کلیدی"""
    if reservations_df.empty:
        return {
            'total_reservations': 0,
            'completion_rate': 0,
            'cancellation_rate': 0,
            'adr': 0,
            'revenue': 0,
            'revpar': 0,
            'total_nights': 0,
            'no_show_rate': 0
        }
    
    total_reservations = len(reservations_df)
    completed = reservations_df[reservations_df['status'] == 'completed']
    cancelled = reservations_df[reservations_df['status'] == 'cancelled']
    no_show = reservations_df[reservations_df['status'] == 'no-show']
    
    completed['nights'] = (completed['check_out'] - completed['check_in']).dt.days
    total_nights = completed['nights'].sum() if not completed.empty else 0
    
    adr = completed['price_per_night'].mean() if not completed.empty else 0
    
    if not completed.empty:
        completed['total_price'] = completed['price_per_night'] * completed['nights']
        revenue = completed['total_price'].sum()
    else:
        revenue = 0
    
    total_rooms = 20
    days_in_period = 30
    revpar = revenue / total_rooms / days_in_period if total_rooms > 0 else 0
    
    return {
        'total_reservations': total_reservations,
        'completion_rate': (len(completed) / total_reservations * 100) if total_reservations > 0 else 0,
        'cancellation_rate': (len(cancelled) / total_reservations * 100) if total_reservations > 0 else 0,
        'no_show_rate': (len(no_show) / total_reservations * 100) if total_reservations > 0 else 0,
        'adr': adr,
        'revenue': revenue,
        'revpar': revpar,
        'total_nights': total_nights
    }

# ============================================
# توابع نمودارهای تحلیل مهمانان
# ============================================
def guest_segmentation(guests_df):
    """تقسیم‌بندی مهمانان بر اساس وفاداری"""
    if guests_df.empty:
        return px.pie(title='داده‌ای برای نمایش وجود ندارد')
    
    bins = [0, 30, 50, 70, 100]
    labels = ['کم‌وفادار', 'متوسط', 'وفادار', 'بسیار وفادار']
    guests_df_copy = guests_df.copy()
    guests_df_copy['loyalty_tier'] = pd.cut(guests_df_copy['loyalty_score'], bins=bins, labels=labels, right=True)
    
    tier_counts = guests_df_copy['loyalty_tier'].value_counts().reset_index()
    tier_counts.columns = ['level', 'count']
    
    fig = px.pie(
        tier_counts, 
        values='count',
        names='level',
        title='توزیع مهمانان بر اساس سطح وفاداری',
        hole=0.4,
        color_discrete_sequence=['#FF6B6B', '#FECA57', '#48DBFB', '#0ABDE3']
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def guest_geography(guests_df):
    """نمودار توزیع جغرافیایی"""
    if guests_df.empty:
        return px.bar(title='داده‌ای برای نمایش وجود ندارد')
    
    city_counts = guests_df['city'].value_counts().reset_index()
    city_counts.columns = ['city', 'count']
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
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(xaxis_title='تعداد مهمان', yaxis_title='شهر', height=400)
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
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(xaxis_title='علاقه', yaxis_title='تعداد مهمان', height=400)
    return fig

def top_guests(guests_df, n=10):
    """نمایش وفادارترین مهمانان"""
    if guests_df.empty:
        return pd.DataFrame()
    return guests_df.nlargest(n, 'loyalty_score')[['first_name', 'last_name', 'city', 'loyalty_score', 'preferences']]

def guest_growth_trend(guests_df):
    """نمودار روند رشد مهمانان"""
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
    fig.update_traces(line=dict(width=3, color='#FF6B6B'), marker=dict(size=8))
    fig.update_layout(xaxis_title='ماه', yaxis_title='تعداد مهمانان جدید', height=350)
    return fig

def guest_retention_rate(guests_df):
    """محاسبه نرخ بازگشت مشتریان"""
    if guests_df.empty:
        return 0
    returning = len(guests_df[guests_df['total_visits'] > 1])
    total = len(guests_df)
    return (returning / total * 100) if total > 0 else 0

# ============================================
# توابع نمودارهای مدیریت ایونت‌ها
# ============================================
def events_dashboard(events_df):
    """داشبورد وضعیت ایونت‌ها"""
    if events_df.empty:
        empty_fig = px.bar(title='داده‌ای برای نمایش وجود ندارد')
        return empty_fig, empty_fig
    
    events_df_copy = events_df.copy()
    events_df_copy['fill_rate'] = (events_df_copy['registered'] / events_df_copy['capacity']) * 100
    events_df_copy = events_df_copy.sort_values('date')
    
    fig1 = px.bar(
        events_df_copy,
        x='event_name',
        y=['capacity', 'registered'],
        title='وضعیت ثبت‌نام ایونت‌ها',
        barmode='group',
        text_auto=True,
        color_discrete_sequence=['#74B9FF', '#FF7675']
    )
    fig1.update_layout(xaxis_title='نام ایونت', yaxis_title='تعداد', height=350)
    
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
    fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig2.update_layout(xaxis_title='نام ایونت', yaxis_title='درصد پر شدن', height=350, yaxis=dict(range=[0, 110]))
    
    return fig1, fig2

def event_revenue_analysis(events_df, reservations_df):
    """تحلیل درآمد حاصل از ایونت‌ها"""
    if events_df.empty or reservations_df.empty:
        return px.bar(title='داده‌ای برای نمایش وجود ندارد')
    
    event_reservations = reservations_df[reservations_df['has_event'] == True]
    
    if event_reservations.empty:
        return px.bar(title='هیچ رزروی با ایونت همراه نبوده است')
    
    revenue_by_event = event_reservations.groupby('event_name').agg({
        'price_per_night': 'sum',
        'reservation_id': 'count'
    }).reset_index()
    revenue_by_event.columns = ['event', 'total_revenue', 'reservation_count']
    revenue_by_event = revenue_by_event.sort_values('total_revenue', ascending=True)
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
    fig.update_traces(texttemplate='%{text:.1f} میلیون تومان', textposition='outside')
    fig.update_layout(xaxis_title='درآمد (میلیون تومان)', yaxis_title='ایونت', height=400)
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
        range_color=[0, 100]
    )
    fig.update_layout(xaxis_title='تاریخ', yaxis_title='ایونت', height=400)
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
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    return fig

# ============================================
# توابع کمکی
# ============================================
def format_currency(amount):
    """تبدیل عدد به فرمت تومان"""
    if amount >= 1000000:
        return f"{amount/1000000:,.1f} میلیون تومان"
    elif amount >= 1000:
        return f"{amount/1000:,.0f} هزار تومان"
    else:
        return f"{amount:,.0f} تومان"

# ============================================
# تولید داده در صورت نیاز
# ============================================
if not check_data_exists():
    with st.spinner("⏳ در حال تولید داده‌های نمونه..."):
        generate_sample_data()
        st.success("✅ داده‌ها با موفقیت ساخته شدند!")

# ============================================
# بارگذاری داده‌ها
# ============================================
guests_df, reservations_df, events_df = load_all_data()

if guests_df is None:
    st.error("❌ خطا در بارگذاری داده‌ها")
    st.stop()

# ============================================
# سایدبار
# ============================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 15px 0; background: linear-gradient(135deg, #8B4513, #D2691E); 
                border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: #FFFFFF; margin: 0; font-size: 24px;">🏨 بوتیک هتل</h2>
        <h3 style="color: #FFD700; margin: 0; font-size: 20px;">محلاتی</h3>
        <p style="color: #F5DEB3; font-size: 12px; margin: 5px 0 0 0;">✨ خانه تاریخی بازسازی شده</p>
        <p style="color: #F5DEB3; font-size: 11px; margin: 0;">شیراز - خیابان محلاتی</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("📅 بازه زمانی")
    default_start = datetime.now() - timedelta(days=90)
    default_end = datetime.now()
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("از تاریخ", default_start)
    with col2:
        end_date = st.date_input("تا تاریخ", default_end)
    
    st.subheader("🔍 فیلترهای پیشرفته")
    channels = ['همه', 'Website', 'Booking.com', 'Instagram', 'Phone', 'Walk-in', 'Google Hotels']
    selected_channels = st.multiselect("کانال رزرو", channels, default=['همه'])
    
    room_types = ['همه', 'اتاق سنتی', 'اتاق مدرن', 'سوئیت', 'اتاق خانوادگی']
    selected_rooms = st.selectbox("نوع اتاق", room_types)
    
    st.subheader("⚙️ تنظیمات")
    show_detailed_stats = st.checkbox("نمایش آمار دقیق", value=True)
    
    st.markdown("---")
    st.caption("**نسخه:** ۱.۰ | **توسعه‌دهنده:** تیم مدیریت")

# ============================================
# عنوان اصلی
# ============================================
st.title("📊 داشبورد مدیریت بوتیک هتل محلاتی")
st.caption(f"🕒 آخرین بروزرسانی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================
# اعمال فیلترها
# ============================================
reservations_filtered = reservations_df[
    (reservations_df['check_in'] >= pd.to_datetime(start_date)) & 
    (reservations_df['check_in'] <= pd.to_datetime(end_date))
]

if 'همه' not in selected_channels:
    reservations_filtered = reservations_filtered[
        reservations_filtered['channel'].isin(selected_channels)
    ]

if selected_rooms != 'همه':
    reservations_filtered = reservations_filtered[
        reservations_filtered['room_type'] == selected_rooms
    ]

kpis = calculate_kpis(reservations_filtered)

# ============================================
# ردیف اول: شاخص‌های کلیدی (KPI)
# ============================================
st.markdown("---")
st.subheader("📈 شاخص‌های کلیدی عملکرد")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📋 کل رزروها",
        value=f"{kpis['total_reservations']:,}",
        delta=f"{kpis['completion_rate']:.1f}% تکمیل شده"
    )

with col2:
    st.metric(
        label="💰 میانگین قیمت هر شب (ADR)",
        value=format_currency(kpis['adr']),
        delta=f"{kpis['revenue']/1000000:,.1f} میلیون درآمد کل"
    )

with col3:
    st.metric(
        label="📈 درآمد هر اتاق (RevPAR)",
        value=format_currency(kpis['revpar']),
        delta="ماهانه"
    )

with col4:
    st.metric(
        label="❌ نرخ لغو",
        value=f"{kpis['cancellation_rate']:.1f}%",
        delta=f"{kpis['no_show_rate']:.1f}% عدم حضور",
        delta_color="inverse"
    )

if show_detailed_stats:
    with st.expander("📊 آمار دقیق رزروها"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("تعداد شب‌های اقامت", f"{kpis['total_nights']:,}")
        with col2:
            st.metric("میانگین مدت اقامت", 
                     f"{kpis['total_nights']/kpis['total_reservations']:.1f} شب" if kpis['total_reservations'] > 0 else "۰")
        with col3:
            st.metric("نرخ تکمیل", f"{kpis['completion_rate']:.1f}%")

# ============================================
# ردیف دوم: تحلیل مهمانان
# ============================================
st.markdown("---")
st.subheader("👥 تحلیل و شناخت مهمانان")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(guest_segmentation(guests_df), use_container_width=True)

with col2:
    st.plotly_chart(guest_geography(guests_df), use_container_width=True)

# ============================================
# ردیف سوم: روند رشد و علایق
# ============================================
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(guest_growth_trend(guests_df), use_container_width=True)

with col2:
    st.plotly_chart(guest_preferences(guests_df), use_container_width=True)

# ============================================
# ردیف چهارم: وفادارترین مهمانان
# ============================================
st.subheader("🏆 وفادارترین مهمانان")

top_guests_df = top_guests(guests_df, 5)
if not top_guests_df.empty:
    cols = st.columns(5)
    for idx, (_, row) in enumerate(top_guests_df.iterrows()):
        with cols[idx]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f5f5f5, #e8e8e8); 
                        padding: 15px; border-radius: 10px; 
                        border-right: 4px solid #FFD700;
                        text-align: center;
                        min-height: 130px;">
                <h4 style="margin: 0; color: #333;">{row['first_name']} {row['last_name']}</h4>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">🏙 {row['city']}</p>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">🎯 {row['preferences']}</p>
                <p style="margin: 5px 0; font-size: 18px; color: #FFD700;">
                    ⭐ {row['loyalty_score']:.1f}
                </p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("هیچ مهمانی برای نمایش وجود ندارد.")

# ============================================
# ردیف پنجم: مدیریت ایونت‌ها
# ============================================
st.markdown("---")
st.subheader("🎭 مدیریت ایونت‌ها")

col1, col2 = st.columns(2)

with col1:
    fig1, fig2 = events_dashboard(events_df)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# ردیف ششم: تحلیل پیشرفته ایونت‌ها
# ============================================
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(events_timeline(events_df), use_container_width=True)

with col2:
    st.plotly_chart(event_category_analysis(events_df), use_container_width=True)

# ============================================
# ردیف هفتم: درآمد ایونت‌ها
# ============================================
st.subheader("💰 تحلیل درآمد ایونت‌ها")

fig_revenue = event_revenue_analysis(events_df, reservations_filtered)
st.plotly_chart(fig_revenue, use_container_width=True)

if not events_df.empty:
    total_events = len(events_df)
    total_registered = events_df['registered'].sum()
    total_capacity = events_df['capacity'].sum()
    avg_fill_rate = (total_registered / total_capacity * 100) if total_capacity > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎭 تعداد ایونت‌ها", total_events)
    with col2:
        st.metric("🎟️ کل ثبت‌نام‌ها", f"{total_registered:,}")
    with col3:
        st.metric("🪑 ظرفیت کل", f"{total_capacity:,}")
    with col4:
        st.metric("📊 میانگین پر شدن", f"{avg_fill_rate:.1f}%")

# ============================================
# ردیف هشتم: آمار کلی و جمع‌بندی
# ============================================
st.markdown("---")
st.subheader("📊 خلاصه آمار هتل")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 کل مهمانان", f"{len(guests_df):,}")

with col2:
    retention = guest_retention_rate(guests_df)
    st.metric("📊 نرخ بازگشت مشتریان", f"{retention:.1f}%")

with col3:
    avg_loyalty = guests_df['loyalty_score'].mean() if not guests_df.empty else 0
    st.metric("⭐ میانگین وفاداری", f"{avg_loyalty:.1f}")

with col4:
    loyal_count = len(guests_df[guests_df['loyalty_score'] > 70]) if not guests_df.empty else 0
    st.metric("🌟 مهمانان وفادار", f"{loyal_count}")

# ============================================
# بخش: بینش‌ها و توصیه‌ها
# ============================================
st.markdown("---")
st.subheader("💡 بینش‌ها و توصیه‌های مدیریتی")

insights = []

if kpis['completion_rate'] < 60:
    insights.append("🔴 **نرخ اشغال پایین است** (کمتر از ۶۰٪). پیشنهاد: اجرای کمپین تخفیفی یا تبلیغات هدفمند.")

if kpis['cancellation_rate'] > 20:
    insights.append("⚠️ **نرخ لغو بالا** (بیشتر از ۲۰٪). پیشنهاد: بررسی سیاست‌های لغو و بهبود ارتباط با مشتری.")

if not events_df.empty:
    best_event = events_df.loc[events_df['registered'].idxmax()]
    if best_event['registered'] > 0:
        insights.append(f"🎯 **ایونت پرفروش:** '{best_event['event_name']}' با {best_event['registered']} ثبت‌نام.")

if not guests_df.empty and guests_df['loyalty_score'].mean() < 50:
    insights.append("💎 **میانگین وفاداری پایین است**. پیشنهاد: ایجاد برنامه پاداش برای مهمانان تکراری.")

if not guests_df.empty:
    top_city = guests_df['city'].mode()[0]
    insights.append(f"📍 **بیشترین مهمانان از {top_city}** هستند.")

if insights:
    for insight in insights:
        st.info(insight)
else:
    st.success("🎉 همه چیز در وضعیت مطلوب است! به کار خود ادامه دهید.")

# ============================================
# فوتر (Footer)
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px 0; color: #666;">
    <p style="font-size: 14px;">
        🚀 <b>بوتیک هتل محلاتی</b> - داشبورد هوشمند مدیریت
    </p>
    <p style="font-size: 12px;">
        توسعه‌یافته با ❤️ با استفاده از Streamlit | © ۱۴۰۴
    </p>
</div>
""", unsafe_allow_html=True)

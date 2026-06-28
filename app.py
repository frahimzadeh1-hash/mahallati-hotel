import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import os
import json

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
# توابع تولید و بارگذاری داده
# ============================================

def generate_sample_data():
    """تولید داده‌های نمونه"""
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
    channels = ['Website', 'Booking.com', 'Instagram', 'Phone', 'Walk-in']
    
    for i in range(500):
        check_in = random.choice(date_range)
        stay_days = random.randint(1, 5)
        check_out = check_in + timedelta(days=stay_days)
        
        reservation = {
            'reservation_id': f'R{10000+i}',
            'guest_id': f'G{random.randint(1000, 1199)}',
            'check_in': check_in.strftime('%Y-%m-%d'),
            'check_out': check_out.strftime('%Y-%m-%d'),
            'room_type': random.choice(room_types),
            'price_per_night': random.randint(150, 500) * 10000,
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
            'category': random.choice(categories)
        }
        events.append(event)
    
    events_df = pd.DataFrame(events)
    events_df.to_csv('data/events.csv', index=False, encoding='utf-8-sig')
    
    return guests_df, reservations_df, events_df

def load_data():
    """بارگذاری داده‌ها"""
    try:
        guests = pd.read_csv('data/guests.csv', encoding='utf-8-sig')
        reservations = pd.read_csv('data/reservations.csv', encoding='utf-8-sig')
        events = pd.read_csv('data/events.csv', encoding='utf-8-sig')
        
        reservations['check_in'] = pd.to_datetime(reservations['check_in'])
        reservations['check_out'] = pd.to_datetime(reservations['check_out'])
        events['date'] = pd.to_datetime(events['date'])
        
        return guests, reservations, events
    except:
        return None, None, None

def save_data(guests_df, reservations_df, events_df):
    """ذخیره داده‌ها"""
    guests_df.to_csv('data/guests.csv', index=False, encoding='utf-8-sig')
    reservations_df.to_csv('data/reservations.csv', index=False, encoding='utf-8-sig')
    events_df.to_csv('data/events.csv', index=False, encoding='utf-8-sig')

# ============================================
# توابع محاسباتی و تحلیلی
# ============================================

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
    
    total = len(reservations_df)
    completed = reservations_df[reservations_df['status'] == 'completed']
    cancelled = reservations_df[reservations_df['status'] == 'cancelled']
    no_show = reservations_df[reservations_df['status'] == 'no-show']
    
    completed['nights'] = (completed['check_out'] - completed['check_in']).dt.days
    total_nights = completed['nights'].sum() if not completed.empty else 0
    adr = completed['price_per_night'].mean() if not completed.empty else 0
    revenue = (completed['price_per_night'] * completed['nights']).sum() if not completed.empty else 0
    revpar = revenue / 20 / 30 if revenue > 0 else 0
    
    return {
        'total_reservations': total,
        'completion_rate': (len(completed) / total * 100) if total > 0 else 0,
        'cancellation_rate': (len(cancelled) / total * 100) if total > 0 else 0,
        'no_show_rate': (len(no_show) / total * 100) if total > 0 else 0,
        'adr': adr,
        'revenue': revenue,
        'revpar': revpar,
        'total_nights': total_nights
    }

# ============================================
# توابع نمودارها
# ============================================

def guest_segmentation(guests_df):
    if guests_df.empty:
        return px.pie(title='داده‌ای وجود ندارد')
    bins = [0, 30, 50, 70, 100]
    labels = ['کم‌وفادار', 'متوسط', 'وفادار', 'بسیار وفادار']
    guests_df_copy = guests_df.copy()
    guests_df_copy['loyalty_tier'] = pd.cut(guests_df_copy['loyalty_score'], bins=bins, labels=labels, right=True)
    tier_counts = guests_df_copy['loyalty_tier'].value_counts().reset_index()
    tier_counts.columns = ['level', 'count']
    fig = px.pie(tier_counts, values='count', names='level', title='تقسیم‌بندی وفاداری', hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def guest_geography(guests_df):
    if guests_df.empty:
        return px.bar(title='داده‌ای وجود ندارد')
    city_counts = guests_df['city'].value_counts().reset_index()
    city_counts.columns = ['city', 'count']
    city_counts = city_counts.sort_values('count', ascending=True)
    fig = px.bar(city_counts, x='count', y='city', title='توزیع جغرافیایی', color='count', orientation='h')
    fig.update_layout(height=400)
    return fig

def guest_preferences(guests_df):
    if guests_df.empty:
        return px.bar(title='داده‌ای وجود ندارد')
    pref_counts = guests_df['preferences'].value_counts().reset_index()
    pref_counts.columns = ['preference', 'count']
    fig = px.bar(pref_counts, x='preference', y='count', title='علایق مهمانان', color='count')
    return fig

def guest_growth(guests_df):
    if guests_df.empty:
        return px.line(title='داده‌ای وجود ندارد')
    guests_df_copy = guests_df.copy()
    guests_df_copy['first_visit'] = pd.to_datetime(guests_df_copy['first_visit'])
    monthly = guests_df_copy.groupby(guests_df_copy['first_visit'].dt.to_period('M')).size().reset_index()
    monthly.columns = ['month', 'new_guests']
    monthly['month'] = monthly['month'].astype(str)
    fig = px.line(monthly, x='month', y='new_guests', title='روند جذب مهمانان', markers=True)
    return fig

def events_dashboard(events_df):
    if events_df.empty:
        return px.bar(title='داده‌ای وجود ندارد'), px.bar(title='داده‌ای وجود ندارد')
    events_df_copy = events_df.copy()
    events_df_copy['fill_rate'] = (events_df_copy['registered'] / events_df_copy['capacity']) * 100
    events_df_copy = events_df_copy.sort_values('date')
    
    fig1 = px.bar(events_df_copy, x='event_name', y=['capacity', 'registered'], 
                  title='ظرفیت و ثبت‌نام', barmode='group')
    fig2 = px.bar(events_df_copy, x='event_name', y='fill_rate', 
                  title='درصد پر شدن ظرفیت', color='fill_rate',
                  color_continuous_scale=[[0, 'red'], [0.5, 'yellow'], [1, 'green']])
    fig2.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    return fig1, fig2

def event_revenue(events_df, reservations_df):
    if events_df.empty or reservations_df.empty:
        return px.bar(title='داده‌ای وجود ندارد')
    event_res = reservations_df[reservations_df['has_event'] == True] if 'has_event' in reservations_df.columns else pd.DataFrame()
    if event_res.empty:
        return px.bar(title='هیچ رزروی با ایونت همراه نیست')
    revenue_by_event = event_res.groupby('event_name').agg({'price_per_night': 'sum', 'reservation_id': 'count'}).reset_index()
    revenue_by_event.columns = ['event', 'total_revenue', 'count']
    revenue_by_event['total_revenue_m'] = revenue_by_event['total_revenue'] / 1000000
    fig = px.bar(revenue_by_event, x='total_revenue_m', y='event', 
                 title='درآمد ایونت‌ها (میلیون تومان)', color='count', orientation='h')
    return fig

# ============================================
# بخش مدیریت اطلاعات
# ============================================

def management_section(guests_df, reservations_df, events_df):
    """پنل مدیریت اطلاعات"""
    st.header("📝 پنل مدیریت اطلاعات")
    st.markdown("---")
    
    # ===== تب‌های مدیریت =====
    tab1, tab2, tab3, tab4 = st.tabs(["👤 مهمانان", "🏠 رزروها", "🎭 ایونت‌ها", "📊 ثبت‌نام ایونت"])
    
    # ===== تب ۱: مدیریت مهمانان =====
    with tab1:
        st.subheader("👤 مدیریت مهمانان")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # نمایش لیست مهمانان
            st.dataframe(
                guests_df[['guest_id', 'first_name', 'last_name', 'phone', 'city', 'preferences', 'loyalty_score']],
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.subheader("➕ افزودن مهمان جدید")
            
            with st.form("add_guest_form"):
                first_name = st.text_input("نام")
                last_name = st.text_input("نام خانوادگی")
                phone = st.text_input("شماره تماس")
                city = st.selectbox("شهر", ['تهران', 'شیراز', 'اصفهان', 'مشهد', 'تبریز', 'یزد', 'کاشان'])
                preferences = st.selectbox("علاقه‌مندی", ['موسیقی', 'شعر', 'فیلم', 'هنر', 'تاریخ', 'غذا'])
                
                submitted = st.form_submit_button("➕ افزودن مهمان")
                
                if submitted:
                    if first_name and last_name and phone:
                        new_id = f"G{len(guests_df) + 1000}"
                        new_guest = pd.DataFrame([{
                            'guest_id': new_id,
                            'first_name': first_name,
                            'last_name': last_name,
                            'phone': phone,
                            'city': city,
                            'first_visit': datetime.now().strftime('%Y-%m-%d'),
                            'total_visits': 1,
                            'preferences': preferences,
                            'loyalty_score': 50.0
                        }])
                        guests_df_updated = pd.concat([guests_df, new_guest], ignore_index=True)
                        guests_df_updated.to_csv('data/guests.csv', index=False, encoding='utf-8-sig')
                        st.success(f"✅ مهمان {first_name} {last_name} با موفقیت افزوده شد!")
                        st.rerun()
                    else:
                        st.error("❌ لطفاً نام و شماره تماس را وارد کنید!")
    
    # ===== تب ۲: مدیریت رزروها =====
    with tab2:
        st.subheader("🏠 مدیریت رزروها")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.dataframe(
                reservations_df[['reservation_id', 'guest_id', 'check_in', 'check_out', 'room_type', 'price_per_night', 'status']],
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.subheader("➕ افزودن رزرو جدید")
            
            with st.form("add_reservation_form"):
                guest_id = st.selectbox("شناسه مهمان", guests_df['guest_id'].tolist())
                check_in = st.date_input("تاریخ ورود")
                check_out = st.date_input("تاریخ خروج")
                room_type = st.selectbox("نوع اتاق", ['اتاق سنتی', 'اتاق مدرن', 'سوئیت', 'اتاق خانوادگی'])
                price = st.number_input("قیمت هر شب (تومان)", min_value=100000, step=100000, value=2000000)
                channel = st.selectbox("کانال رزرو", ['Website', 'Booking.com', 'Instagram', 'Phone', 'Walk-in'])
                
                submitted = st.form_submit_button("➕ افزودن رزرو")
                
                if submitted:
                    if guest_id and check_in and check_out:
                        new_id = f"R{len(reservations_df) + 10000}"
                        new_reservation = pd.DataFrame([{
                            'reservation_id': new_id,
                            'guest_id': guest_id,
                            'check_in': check_in.strftime('%Y-%m-%d'),
                            'check_out': check_out.strftime('%Y-%m-%d'),
                            'room_type': room_type,
                            'price_per_night': price,
                            'channel': channel,
                            'status': 'completed'
                        }])
                        reservations_df_updated = pd.concat([reservations_df, new_reservation], ignore_index=True)
                        reservations_df_updated.to_csv('data/reservations.csv', index=False, encoding='utf-8-sig')
                        st.success(f"✅ رزرو {new_id} با موفقیت افزوده شد!")
                        st.rerun()
                    else:
                        st.error("❌ لطفاً همه فیلدها را پر کنید!")
    
    # ===== تب ۳: مدیریت ایونت‌ها =====
    with tab3:
        st.subheader("🎭 مدیریت ایونت‌ها")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.dataframe(
                events_df[['event_id', 'event_name', 'date', 'capacity', 'registered', 'price', 'category']],
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.subheader("➕ افزودن ایونت جدید")
            
            with st.form("add_event_form"):
                event_name = st.text_input("نام ایونت")
                event_date = st.date_input("تاریخ برگزاری")
                capacity = st.number_input("ظرفیت", min_value=1, value=30)
                price = st.number_input("قیمت (تومان)", min_value=0, step=100000, value=1000000)
                category = st.selectbox("دسته‌بندی", ['موسیقی', 'شعر', 'فیلم', 'هنر'])
                
                submitted = st.form_submit_button("➕ افزودن ایونت")
                
                if submitted:
                    if event_name and event_date:
                        new_id = f"E{len(events_df) + 2000}"
                        new_event = pd.DataFrame([{
                            'event_id': new_id,
                            'event_name': event_name,
                            'date': event_date.strftime('%Y-%m-%d'),
                            'capacity': capacity,
                            'registered': 0,
                            'price': price,
                            'category': category
                        }])
                        events_df_updated = pd.concat([events_df, new_event], ignore_index=True)
                        events_df_updated.to_csv('data/events.csv', index=False, encoding='utf-8-sig')
                        st.success(f"✅ ایونت {event_name} با موفقیت افزوده شد!")
                        st.rerun()
                    else:
                        st.error("❌ لطفاً نام و تاریخ ایونت را وارد کنید!")
    
    # ===== تب ۴: ثبت‌نام در ایونت =====
    with tab4:
        st.subheader("📊 ثبت‌نام مهمانان در ایونت‌ها")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 انتخاب ایونت")
            selected_event = st.selectbox("ایونت مورد نظر", events_df['event_name'].tolist())
            
            event_data = events_df[events_df['event_name'] == selected_event]
            if not event_data.empty:
                st.info(f"""
                **📋 اطلاعات ایونت:**
                - تاریخ: {event_data['date'].iloc[0]}
                - ظرفیت: {event_data['capacity'].iloc[0]}
                - ثبت‌نام فعلی: {event_data['registered'].iloc[0]}
                - جای خالی: {event_data['capacity'].iloc[0] - event_data['registered'].iloc[0]}
                """)
        
        with col2:
            st.subheader("👤 انتخاب مهمان")
            guest_list = guests_df[['guest_id', 'first_name', 'last_name']].copy()
            guest_list['full_name'] = guest_list['first_name'] + ' ' + guest_list['last_name'] + ' (' + guest_list['guest_id'] + ')'
            selected_guest = st.selectbox("مهمان", guest_list['full_name'].tolist())
            
            if st.button("✅ ثبت‌نام در ایونت", use_container_width=True):
                # بروزرسانی تعداد ثبت‌نام‌ها
                event_index = events_df[events_df['event_name'] == selected_event].index[0]
                events_df.loc[event_index, 'registered'] += 1
                events_df.to_csv('data/events.csv', index=False, encoding='utf-8-sig')
                st.success(f"✅ {selected_guest} با موفقیت در ایونت {selected_event} ثبت‌نام شد!")
                st.balloons()
                st.rerun()
    
    return guests_df, reservations_df, events_df

# ============================================
# بخش تحلیل‌ها و گزارش‌ها
# ============================================

def analytics_section(guests_df, reservations_df, events_df):
    """بخش تحلیل و گزارش"""
    
    st.header("📊 داشبورد تحلیلی")
    
    # ===== فیلترها =====
    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input("از تاریخ", datetime.now() - timedelta(days=90))
    with col2:
        end_date = st.date_input("تا تاریخ", datetime.now())
    with col3:
        channel_filter = st.multiselect("کانال رزرو", 
                                       ['Website', 'Booking.com', 'Instagram', 'Phone', 'Walk-in'],
                                       default=['Website', 'Booking.com', 'Instagram'])
    
    # فیلتر کردن رزروها
    reservations_filtered = reservations_df[
        (reservations_df['check_in'] >= pd.to_datetime(start_date)) & 
        (reservations_df['check_in'] <= pd.to_datetime(end_date))
    ]
    if channel_filter:
        reservations_filtered = reservations_filtered[reservations_filtered['channel'].isin(channel_filter)]
    
    # ===== KPIها =====
    kpis = calculate_kpis(reservations_filtered)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📋 کل رزروها", f"{kpis['total_reservations']:,}")
    with col2:
        st.metric("💰 درآمد کل", f"{kpis['revenue']/1000000:,.1f} میلیون تومان")
    with col3:
        st.metric("📈 نرخ تکمیل", f"{kpis['completion_rate']:.1f}%")
    with col4:
        st.metric("❌ نرخ لغو", f"{kpis['cancellation_rate']:.1f}%")
    
    st.markdown("---")
    
    # ===== ردیف اول: تحلیل مهمانان =====
    st.subheader("👥 تحلیل مهمانان")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(guest_segmentation(guests_df), use_container_width=True)
    with col2:
        st.plotly_chart(guest_geography(guests_df), use_container_width=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(guest_growth(guests_df), use_container_width=True)
    with col2:
        st.plotly_chart(guest_preferences(guests_df), use_container_width=True)
    
    # ===== ردیف دوم: ایونت‌ها =====
    st.markdown("---")
    st.subheader("🎭 تحلیل ایونت‌ها")
    
    col1, col2 = st.columns(2)
    with col1:
        fig1, fig2 = events_dashboard(events_df)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    
    st.plotly_chart(event_revenue(events_df, reservations_filtered), use_container_width=True)

# ============================================
# بخش راهنما
# ============================================

def help_section():
    """بخش راهنما"""
    st.header("📚 راهنمای استفاده از داشبورد")
    
    st.markdown("""
    ### 🎯 این داشبورد چه قابلیت‌هایی دارد؟
    
    ۱. **مدیریت مهمانان** 👤
    - مشاهده لیست تمام مهمانان
    - افزودن مهمان جدید با اطلاعات کامل
    - نمایش امتیاز وفاداری و علایق
    
    ۲. **مدیریت رزروها** 🏠
    - مشاهده تمام رزروها
    - افزودن رزرو جدید
    - فیلتر بر اساس تاریخ و کانال
    
    ۳. **مدیریت ایونت‌ها** 🎭
    - مشاهده تمام ایونت‌ها
    - افزودن ایونت جدید
    - ثبت‌نام مهمانان در ایونت‌ها
    
    ۴. **تحلیل‌های پیشرفته** 📊
    - تقسیم‌بندی وفاداری مهمانان
    - توزیع جغرافیایی
    - علایق مهمانان
    - تحلیل عملکرد ایونت‌ها
    - درآمدزایی ایونت‌ها
    
    ### 📝 نحوه استفاده
    
    - از **تب‌های مدیریت** برای افزودن اطلاعات استفاده کنید
    - از **بخش تحلیل** برای مشاهده نمودارها استفاده کنید
    - داده‌ها به‌طور خودکار در پوشه `data` ذخیره می‌شوند
    
    ### 💡 نکات مهم
    
    - برای افزودن مهمان جدید، به تب "مهمانان" بروید
    - برای ثبت‌نام در ایونت، به تب "ثبت‌نام ایونت" بروید
    - همه تغییرات به‌طور خودکار ذخیره می‌شوند
    """)

# ============================================
# تابع اصلی
# ============================================

def main():
    """تابع اصلی برنامه"""
    
    # ایجاد داده در صورت نیاز
    if not os.path.exists('data'):
        generate_sample_data()
    
    # بارگذاری داده
    guests_df, reservations_df, events_df = load_data()
    
    if guests_df is None:
        st.error("❌ خطا در بارگذاری داده‌ها")
        st.info("در حال تولید داده‌های جدید...")
        generate_sample_data()
        guests_df, reservations_df, events_df = load_data()
    
    # ===== سایدبار =====
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 15px 0; background: linear-gradient(135deg, #8B4513, #D2691E); 
                    border-radius: 10px; margin-bottom: 20px;">
            <h2 style="color: #FFFFFF; margin: 0;">🏨 بوتیک هتل</h2>
            <h3 style="color: #FFD700; margin: 0;">محلاتی</h3>
            <p style="color: #F5DEB3; font-size: 12px;">شیراز - خیابان محلاتی</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # منوی اصلی
        menu = st.radio(
            "📋 منوی اصلی",
            ["📝 مدیریت اطلاعات", "📊 تحلیل و گزارش", "📚 راهنما"],
            index=0
        )
        
        st.markdown("---")
        st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # آمار سریع
        st.caption(f"👥 {len(guests_df)} مهمان")
        st.caption(f"🏠 {len(reservations_df)} رزرو")
        st.caption(f"🎭 {len(events_df)} ایونت")
    
    # ===== نمایش بخش‌های مختلف =====
    if menu == "📝 مدیریت اطلاعات":
        guests_df, reservations_df, events_df = management_section(guests_df, reservations_df, events_df)
    
    elif menu == "📊 تحلیل و گزارش":
        analytics_section(guests_df, reservations_df, events_df)
    
    elif menu == "📚 راهنما":
        help_section()
    
    # ===== فوتر =====
    st.markdown("---")
    st.caption("🚀 بوتیک هتل محلاتی - داشبورد هوشمند مدیریت | توسعه‌یافته با Streamlit")

if __name__ == "__main__":
    main()

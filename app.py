import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
import sys

# ============================================
# تنظیمات صفحه - حتماً اولین خط بعد از importها
# ============================================
st.set_page_config(
    page_title="🏨 بوتیک هتل محلاتی - داشبورد مدیریت",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# تنظیم مسیر برای پیدا کردن ماژول‌ها
# ============================================
# اطمینان از اینکه پوشه modules و utils در مسیر هستند
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# ============================================
# ایمپورت ماژول‌های اختصاصی
# ============================================
try:
    from modules.data_loader import load_all_data, calculate_kpis
    from modules.guest_analytics import (
        guest_segmentation, guest_geography, guest_preferences, 
        top_guests, guest_growth_trend, guest_retention_rate
    )
    from modules.events_manager import (
        events_dashboard, event_revenue_analysis, 
        events_timeline, event_category_analysis
    )
    from utils.helpers import generate_sample_data
except ModuleNotFoundError as e:
    st.error(f"❌ ماژول مورد نظر پیدا نشد: {e}")
    st.info("""
    **راه‌حل:** 
    1. مطمئن شوید فایل‌های زیر در پوشه‌های correct وجود دارند:
       - modules/data_loader.py
       - modules/guest_analytics.py
       - modules/events_manager.py
       - utils/helpers.py
    2. از پوشه اصلی (hotel_dashboard) برنامه را اجرا کنید
    """)
    st.stop()

# ============================================
# توابع کمکی
# ============================================
def check_data_exists():
    """بررسی وجود فایل‌های داده"""
    required_files = ['guests.csv', 'reservations.csv', 'events.csv']
    data_dir = os.path.join(current_dir, 'data')
    
    if not os.path.exists(data_dir):
        return False
    
    for file in required_files:
        if not os.path.exists(os.path.join(data_dir, file)):
            return False
    return True

def create_empty_plot(title="داده‌ای برای نمایش وجود ندارد"):
    """ایجاد یک نمودار خالی برای مواقعی که داده نداریم"""
    fig = px.scatter(title=title)
    fig.update_layout(
        annotations=[{
            'text': title,
            'x': 0.5,
            'y': 0.5,
            'font': {'size': 20},
            'showarrow': False
        }]
    )
    return fig

def format_currency(amount):
    """تبدیل عدد به فرمت تومان"""
    if amount >= 1000000:
        return f"{amount/1000000:,.1f} میلیون تومان"
    elif amount >= 1000:
        return f"{amount/1000:,.0f} هزار تومان"
    else:
        return f"{amount:,.0f} تومان"

# ============================================
# سایدبار
# ============================================
with st.sidebar:
    # هدر هتل با استایل سفارشی
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
    
    # ===== بخش تولید داده =====
    if not check_data_exists():
        st.warning("⚠️ داده‌ای وجود ندارد!")
        st.info("""
        برای شروع کار، باید داده‌های نمونه تولید شوند.
        این داده‌ها شامل اطلاعات مهمانان، رزروها و ایونت‌ها هستند.
        """)
        
        if st.button("🔄 تولید داده‌های نمونه", type="primary", use_container_width=True):
            with st.spinner("⏳ در حال تولید داده‌های نمونه..."):
                try:
                    generate_sample_data()
                    st.success("✅ داده‌ها با موفقیت ساخته شدند!")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ خطا در تولید داده‌ها: {str(e)}")
    else:
        st.success("✅ داده‌ها بارگذاری شدند!")
    
    st.markdown("---")
    
    # ===== فیلترهای تاریخ =====
    st.subheader("📅 بازه زمانی")
    
    # تنظیم تاریخ پیش‌فرض
    default_start = datetime.now() - timedelta(days=90)
    default_end = datetime.now()
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("از تاریخ", default_start)
    with col2:
        end_date = st.date_input("تا تاریخ", default_end)
    
    # ===== فیلترهای پیشرفته =====
    st.subheader("🔍 فیلترهای پیشرفته")
    
    # فیلتر کانال رزرو
    channels = ['همه', 'Website', 'Booking.com', 'Instagram', 'Phone', 'Walk-in', 'Google Hotels']
    selected_channels = st.multiselect(
        "کانال رزرو",
        channels,
        default=['همه']
    )
    
    # فیلتر نوع اتاق
    room_types = ['همه', 'اتاق سنتی', 'اتاق مدرن', 'سوئیت', 'اتاق خانوادگی']
    selected_rooms = st.selectbox("نوع اتاق", room_types)
    
    # ===== تنظیمات نمایش =====
    st.subheader("⚙️ تنظیمات")
    show_detailed_stats = st.checkbox("نمایش آمار دقیق", value=True)
    
    st.markdown("---")
    
    # ===== اطلاعات اضافی =====
    st.caption("""
    **نسخه:** ۱.۰  
    **توسعه‌دهنده:** تیم مدیریت  
    **آخرین بروزرسانی:** آبان ۱۴۰۴
    """)

# ============================================
# بخش اصلی: بارگذاری و نمایش داده
# ============================================

# عنوان اصلی
st.title("📊 داشبورد مدیریت بوتیک هتل محلاتی")
st.caption(f"🕒 آخرین بروزرسانی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ===== بررسی وجود داده =====
if not check_data_exists():
    st.warning("""
    ## 🚀 خوش آمدید به داشبورد مدیریت بوتیک هتل محلاتی!
    
    برای شروع کار، لطفاً:
    1. در **سایدبار سمت چپ** روی دکمه **"تولید داده‌های نمونه"** کلیک کنید
    2. منتظر بمانید تا داده‌ها ساخته شوند
    3. صفحه به‌طور خودکار بروزرسانی می‌شود
    
    💡 **نکته:** این داده‌ها کاملاً نمونه هستند و برای تست طراحی شده‌اند.
    بعداً می‌توانید آنها را با داده‌های واقعی هتل جایگزین کنید.
    """)
    st.stop()

# ===== بارگذاری داده‌ها =====
with st.spinner("⏳ در حال بارگذاری داده‌ها..."):
    guests_df, reservations_df, events_df = load_all_data()

if guests_df is None or reservations_df is None or events_df is None:
    st.error("❌ خطا در بارگذاری داده‌ها. لطفاً دوباره تلاش کنید.")
    st.info("""
    **راه‌حل‌ها:**
    1. دکمه "تولید داده‌های نمونه" را در سایدبار بزنید
    2. اگر مشکل ادامه داشت، پوشه data را پاک کنید و دوباره امتحان کنید
    3. مطمئن شوید فایل‌های CSV در پوشه data با encoding UTF-8 هستند
    """)
    st.stop()

# ===== اعمال فیلترها =====
# فیلتر تاریخ
reservations_filtered = reservations_df[
    (reservations_df['check_in'] >= pd.to_datetime(start_date)) & 
    (reservations_df['check_in'] <= pd.to_datetime(end_date))
]

# فیلتر کانال
if 'همه' not in selected_channels:
    reservations_filtered = reservations_filtered[
        reservations_filtered['channel'].isin(selected_channels)
    ]

# فیلتر نوع اتاق
if selected_rooms != 'همه':
    reservations_filtered = reservations_filtered[
        reservations_filtered['room_type'] == selected_rooms
    ]

# ===== محاسبه KPIها =====
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
        delta=f"{kpis['completion_rate']:.1f}% تکمیل شده",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="💰 میانگین قیمت هر شب (ADR)",
        value=format_currency(kpis['adr']),
        delta=f"{kpis['revenue']/1000000:,.1f} میلیون درآمد کل",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="📈 درآمد هر اتاق (RevPAR)",
        value=format_currency(kpis['revpar']),
        delta="ماهانه",
        delta_color="off"
    )

with col4:
    st.metric(
        label="❌ نرخ لغو",
        value=f"{kpis['cancellation_rate']:.1f}%",
        delta=f"{kpis['no_show_rate']:.1f}% عدم حضور",
        delta_color="inverse"
    )

# نمایش آمار دقیق (اختیاری)
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
            # کارت اطلاعات مهمان
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
    # نمودار وضعیت ایونت‌ها
    fig1, fig2 = events_dashboard(events_df)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # نمودار پر شدن ظرفیت
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

# نمایش جزئیات درآمد
fig_revenue = event_revenue_analysis(events_df, reservations_filtered)
st.plotly_chart(fig_revenue, use_container_width=True)

# آمار تکمیلی ایونت‌ها
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
    # تعداد مهمانان وفادار (امتیاز > 70)
    loyal_count = len(guests_df[guests_df['loyalty_score'] > 70]) if not guests_df.empty else 0
    st.metric("🌟 مهمانان وفادار", f"{loyal_count}")

# ============================================
# بخش: بینش‌ها و توصیه‌ها
# ============================================
st.markdown("---")
st.subheader("💡 بینش‌ها و توصیه‌های مدیریتی")

# ایجاد بینش‌های خودکار بر اساس داده‌ها
insights = []

# بررسی نرخ اشغال
if kpis['completion_rate'] < 60:
    insights.append("🔴 **نرخ اشغال پایین است** (کمتر از ۶۰٪). پیشنهاد: اجرای کمپین تخفیفی یا تبلیغات هدفمند.")

# بررسی نرخ لغو
if kpis['cancellation_rate'] > 20:
    insights.append("⚠️ **نرخ لغو بالا** (بیشتر از ۲۰٪). پیشنهاد: بررسی سیاست‌های لغو و بهبود ارتباط با مشتری.")

# بررسی ایونت‌های پرفروش
if not events_df.empty:
    best_event = events_df.loc[events_df['registered'].idxmax()]
    if best_event['registered'] > 0:
        insights.append(f"🎯 **ایونت پرفروش:** '{best_event['event_name']}' با {best_event['registered']} ثبت‌نام. پیشنهاد: برگزاری دوره‌های مشابه.")

# بررسی وفاداری
if not guests_df.empty and guests_df['loyalty_score'].mean() < 50:
    insights.append("💎 **میانگین وفاداری پایین است**. پیشنهاد: ایجاد برنامه پاداش و تخفیف برای مهمانان تکراری.")

# بررسی تنوع شهری
if not guests_df.empty:
    top_city = guests_df['city'].mode()[0]
    insights.append(f"📍 **بیشترین مهمانان از {top_city}** هستند. پیشنهاد: هدف‌گیری کمپین‌های بازاریابی در این شهر.")

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
    <p style="font-size: 11px; color: #999;">
        داده‌ها به‌صورت لحظه‌ای بروزرسانی می‌شوند | نسخه ۱.۰
    </p>
</div>
""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
import sys

# ============================================
# تنظیمات صفحه - حتماً اولین خط بعد از importها
# ============================================
st.set_page_config(
    page_title="🏨 بوتیک هتل محلاتی - داشبورد مدیریت",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# تنظیم مسیر برای پیدا کردن ماژول‌ها
# ============================================
# اطمینان از اینکه پوشه modules و utils در مسیر هستند
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# ============================================
# ایمپورت ماژول‌های اختصاصی
# ============================================
try:
    from modules.data_loader import load_all_data, calculate_kpis
    from modules.guest_analytics import (
        guest_segmentation, guest_geography, guest_preferences, 
        top_guests, guest_growth_trend, guest_retention_rate
    )
    from modules.events_manager import (
        events_dashboard, event_revenue_analysis, 
        events_timeline, event_category_analysis
    )
    from utils.helpers import generate_sample_data
except ModuleNotFoundError as e:
    st.error(f"❌ ماژول مورد نظر پیدا نشد: {e}")
    st.info("""
    **راه‌حل:** 
    1. مطمئن شوید فایل‌های زیر در پوشه‌های correct وجود دارند:
       - modules/data_loader.py
       - modules/guest_analytics.py
       - modules/events_manager.py
       - utils/helpers.py
    2. از پوشه اصلی (hotel_dashboard) برنامه را اجرا کنید
    """)
    st.stop()

# ============================================
# توابع کمکی
# ============================================
def check_data_exists():
    """بررسی وجود فایل‌های داده"""
    required_files = ['guests.csv', 'reservations.csv', 'events.csv']
    data_dir = os.path.join(current_dir, 'data')
    
    if not os.path.exists(data_dir):
        return False
    
    for file in required_files:
        if not os.path.exists(os.path.join(data_dir, file)):
            return False
    return True

def create_empty_plot(title="داده‌ای برای نمایش وجود ندارد"):
    """ایجاد یک نمودار خالی برای مواقعی که داده نداریم"""
    fig = px.scatter(title=title)
    fig.update_layout(
        annotations=[{
            'text': title,
            'x': 0.5,
            'y': 0.5,
            'font': {'size': 20},
            'showarrow': False
        }]
    )
    return fig

def format_currency(amount):
    """تبدیل عدد به فرمت تومان"""
    if amount >= 1000000:
        return f"{amount/1000000:,.1f} میلیون تومان"
    elif amount >= 1000:
        return f"{amount/1000:,.0f} هزار تومان"
    else:
        return f"{amount:,.0f} تومان"

# ============================================
# سایدبار
# ============================================
with st.sidebar:
    # هدر هتل با استایل سفارشی
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
    
    # ===== بخش تولید داده =====
    if not check_data_exists():
        st.warning("⚠️ داده‌ای وجود ندارد!")
        st.info("""
        برای شروع کار، باید داده‌های نمونه تولید شوند.
        این داده‌ها شامل اطلاعات مهمانان، رزروها و ایونت‌ها هستند.
        """)
        
        if st.button("🔄 تولید داده‌های نمونه", type="primary", use_container_width=True):
            with st.spinner("⏳ در حال تولید داده‌های نمونه..."):
                try:
                    generate_sample_data()
                    st.success("✅ داده‌ها با موفقیت ساخته شدند!")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ خطا در تولید داده‌ها: {str(e)}")
    else:
        st.success("✅ داده‌ها بارگذاری شدند!")
    
    st.markdown("---")
    
    # ===== فیلترهای تاریخ =====
    st.subheader("📅 بازه زمانی")
    
    # تنظیم تاریخ پیش‌فرض
    default_start = datetime.now() - timedelta(days=90)
    default_end = datetime.now()
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("از تاریخ", default_start)
    with col2:
        end_date = st.date_input("تا تاریخ", default_end)
    
    # ===== فیلترهای پیشرفته =====
    st.subheader("🔍 فیلترهای پیشرفته")
    
    # فیلتر کانال رزرو
    channels = ['همه', 'Website', 'Booking.com', 'Instagram', 'Phone', 'Walk-in', 'Google Hotels']
    selected_channels = st.multiselect(
        "کانال رزرو",
        channels,
        default=['همه']
    )
    
    # فیلتر نوع اتاق
    room_types = ['همه', 'اتاق سنتی', 'اتاق مدرن', 'سوئیت', 'اتاق خانوادگی']
    selected_rooms = st.selectbox("نوع اتاق", room_types)
    
    # ===== تنظیمات نمایش =====
    st.subheader("⚙️ تنظیمات")
    show_detailed_stats = st.checkbox("نمایش آمار دقیق", value=True)
    
    st.markdown("---")
    
    # ===== اطلاعات اضافی =====
    st.caption("""
    **نسخه:** ۱.۰  
    **توسعه‌دهنده:** تیم مدیریت  
    **آخرین بروزرسانی:** آبان ۱۴۰۴
    """)

# ============================================
# بخش اصلی: بارگذاری و نمایش داده
# ============================================

# عنوان اصلی
st.title("📊 داشبورد مدیریت بوتیک هتل محلاتی")
st.caption(f"🕒 آخرین بروزرسانی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ===== بررسی وجود داده =====
if not check_data_exists():
    st.warning("""
    ## 🚀 خوش آمدید به داشبورد مدیریت بوتیک هتل محلاتی!
    
    برای شروع کار، لطفاً:
    1. در **سایدبار سمت چپ** روی دکمه **"تولید داده‌های نمونه"** کلیک کنید
    2. منتظر بمانید تا داده‌ها ساخته شوند
    3. صفحه به‌طور خودکار بروزرسانی می‌شود
    
    💡 **نکته:** این داده‌ها کاملاً نمونه هستند و برای تست طراحی شده‌اند.
    بعداً می‌توانید آنها را با داده‌های واقعی هتل جایگزین کنید.
    """)
    st.stop()

# ===== بارگذاری داده‌ها =====
with st.spinner("⏳ در حال بارگذاری داده‌ها..."):
    guests_df, reservations_df, events_df = load_all_data()

if guests_df is None or reservations_df is None or events_df is None:
    st.error("❌ خطا در بارگذاری داده‌ها. لطفاً دوباره تلاش کنید.")
    st.info("""
    **راه‌حل‌ها:**
    1. دکمه "تولید داده‌های نمونه" را در سایدبار بزنید
    2. اگر مشکل ادامه داشت، پوشه data را پاک کنید و دوباره امتحان کنید
    3. مطمئن شوید فایل‌های CSV در پوشه data با encoding UTF-8 هستند
    """)
    st.stop()

# ===== اعمال فیلترها =====
# فیلتر تاریخ
reservations_filtered = reservations_df[
    (reservations_df['check_in'] >= pd.to_datetime(start_date)) & 
    (reservations_df['check_in'] <= pd.to_datetime(end_date))
]

# فیلتر کانال
if 'همه' not in selected_channels:
    reservations_filtered = reservations_filtered[
        reservations_filtered['channel'].isin(selected_channels)
    ]

# فیلتر نوع اتاق
if selected_rooms != 'همه':
    reservations_filtered = reservations_filtered[
        reservations_filtered['room_type'] == selected_rooms
    ]

# ===== محاسبه KPIها =====
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
        delta=f"{kpis['completion_rate']:.1f}% تکمیل شده",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="💰 میانگین قیمت هر شب (ADR)",
        value=format_currency(kpis['adr']),
        delta=f"{kpis['revenue']/1000000:,.1f} میلیون درآمد کل",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="📈 درآمد هر اتاق (RevPAR)",
        value=format_currency(kpis['revpar']),
        delta="ماهانه",
        delta_color="off"
    )

with col4:
    st.metric(
        label="❌ نرخ لغو",
        value=f"{kpis['cancellation_rate']:.1f}%",
        delta=f"{kpis['no_show_rate']:.1f}% عدم حضور",
        delta_color="inverse"
    )

# نمایش آمار دقیق (اختیاری)
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
            # کارت اطلاعات مهمان
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
    # نمودار وضعیت ایونت‌ها
    fig1, fig2 = events_dashboard(events_df)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # نمودار پر شدن ظرفیت
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

# نمایش جزئیات درآمد
fig_revenue = event_revenue_analysis(events_df, reservations_filtered)
st.plotly_chart(fig_revenue, use_container_width=True)

# آمار تکمیلی ایونت‌ها
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
    # تعداد مهمانان وفادار (امتیاز > 70)
    loyal_count = len(guests_df[guests_df['loyalty_score'] > 70]) if not guests_df.empty else 0
    st.metric("🌟 مهمانان وفادار", f"{loyal_count}")

# ============================================
# بخش: بینش‌ها و توصیه‌ها
# ============================================
st.markdown("---")
st.subheader("💡 بینش‌ها و توصیه‌های مدیریتی")

# ایجاد بینش‌های خودکار بر اساس داده‌ها
insights = []

# بررسی نرخ اشغال
if kpis['completion_rate'] < 60:
    insights.append("🔴 **نرخ اشغال پایین است** (کمتر از ۶۰٪). پیشنهاد: اجرای کمپین تخفیفی یا تبلیغات هدفمند.")

# بررسی نرخ لغو
if kpis['cancellation_rate'] > 20:
    insights.append("⚠️ **نرخ لغو بالا** (بیشتر از ۲۰٪). پیشنهاد: بررسی سیاست‌های لغو و بهبود ارتباط با مشتری.")

# بررسی ایونت‌های پرفروش
if not events_df.empty:
    best_event = events_df.loc[events_df['registered'].idxmax()]
    if best_event['registered'] > 0:
        insights.append(f"🎯 **ایونت پرفروش:** '{best_event['event_name']}' با {best_event['registered']} ثبت‌نام. پیشنهاد: برگزاری دوره‌های مشابه.")

# بررسی وفاداری
if not guests_df.empty and guests_df['loyalty_score'].mean() < 50:
    insights.append("💎 **میانگین وفاداری پایین است**. پیشنهاد: ایجاد برنامه پاداش و تخفیف برای مهمانان تکراری.")

# بررسی تنوع شهری
if not guests_df.empty:
    top_city = guests_df['city'].mode()[0]
    insights.append(f"📍 **بیشترین مهمانان از {top_city}** هستند. پیشنهاد: هدف‌گیری کمپین‌های بازاریابی در این شهر.")

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
    <p style="font-size: 11px; color: #999;">
        داده‌ها به‌صورت لحظه‌ای بروزرسانی می‌شوند | نسخه ۱.۰
    </p>
</div>
""", unsafe_allow_html=True)
</div>
""", unsafe_allow_html=True)mahallati-hotel

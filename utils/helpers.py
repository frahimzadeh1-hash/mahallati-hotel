import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_sample_data():
    """تولید داده‌های نمونه برای ۶ ماه گذشته"""
    
    # اطمینان از وجود پوشه data
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # لیست اسامی مهمانان
    first_names = ['احمد', 'سارا', 'محمد', 'زهرا', 'علی', 'مریم', 'رضا', 'فاطمه', 'حسین', 'نگار',
                   'کیان', 'نازنین', 'امیر', 'سپیده', 'مهدی', 'الهه', 'پویا', 'شیرین', 'بابک', 'گلناز']
    
    last_names = ['محلاتی', 'کریمی', 'حسینی', 'رضوی', 'نوری', 'یزدی', 'شیرازی', 'کاشانی', 
                  'اصفهانی', 'تبریزی', 'فردوسی', 'سهرابی', 'مهرآور', 'فرخزاد', 'شمسی']
    
    # تاریخ‌های ۶ ماه گذشته
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    print("🔄 در حال تولید داده‌های مهمانان...")
    
    # --- تولید داده‌های مهمانان ---
    guests = []
    for i in range(200):
        guest = {
            'guest_id': f'G{1000+i}',
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'email': f'guest{i}@example.com',
            'phone': f'0912{random.randint(1000000, 9999999)}',
            'city': random.choice(['تهران', 'شیراز', 'اصفهان', 'مشهد', 'تبریز', 'یزد', 'کاشان', 'کرمان']),
            'first_visit': random.choice(date_range).strftime('%Y-%m-%d'),
            'total_visits': random.randint(1, 12),
            'preferences': random.choice(['موسیقی', 'شعر', 'فیلم', 'هنر', 'تاریخ', 'غذا', 'معماری']),
            'loyalty_score': round(random.uniform(0, 100), 1)
        }
        guests.append(guest)
    
    guests_df = pd.DataFrame(guests)
    guests_df.to_csv('data/guests.csv', index=False, encoding='utf-8-sig')
    print(f"✅ {len(guests_df)} مهمان ساخته شد!")
    
    # --- تولید داده‌های رزرو ---
    print("🔄 در حال تولید داده‌های رزرو...")
    reservations = []
    room_types = ['اتاق سنتی', 'اتاق مدرن', 'سوئیت', 'اتاق خانوادگی']
    event_names = ['شب شعر', 'کنسرت موسیقی', 'تحلیل فیلم', 'کارگاه خوشنویسی', 'شب داستان‌گویی', 
                   'نمایشگاه نقاشی', 'شب موسیقی سنتی']
    channels = ['Website', 'Booking.com', 'Instagram', 'Phone', 'Walk-in', 'Google Hotels']
    
    for i in range(500):
        check_in = random.choice(date_range)
        stay_days = random.randint(1, 5)
        check_out = check_in + timedelta(days=stay_days)
        
        # ۳۰٪ رزروها با ایونت همراه هستند
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
    print(f"✅ {len(reservations_df)} رزرو ساخته شد!")
    
    # --- تولید داده‌های ایونت‌ها ---
    print("🔄 در حال تولید داده‌های ایونت‌ها...")
    events = []
    event_types = ['شب شعر بهار', 'کنسرت نی', 'تحلیل فیلم سینمایی', 'کارگاه شعر معاصر', 
                   'شب موسیقی سنتی', 'نمایشگاه عکس', 'جشنواره فیلم کوتاه']
    
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
            'category': random.choice(['موسیقی', 'شعر', 'فیلم', 'هنر'])
        }
        events.append(event)
    
    events_df = pd.DataFrame(events)
    events_df.to_csv('data/events.csv', index=False, encoding='utf-8-sig')
    print(f"✅ {len(events_df)} ایونت ساخته شد!")
    
    print("\n🎉 همه داده‌ها با موفقیت در پوشه 'data' ذخیره شدند!")
    return guests_df, reservations_df, events_df

# اگر فایل مستقیم اجرا شود
if __name__ == "__main__":
    generate_sample_data()import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_sample_data():
    """تولید داده‌های نمونه برای ۶ ماه گذشته"""
    
    # اطمینان از وجود پوشه data
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # لیست اسامی مهمانان
    first_names = ['احمد', 'سارا', 'محمد', 'زهرا', 'علی', 'مریم', 'رضا', 'فاطمه', 'حسین', 'نگار',
                   'کیان', 'نازنین', 'امیر', 'سپیده', 'مهدی', 'الهه', 'پویا', 'شیرین', 'بابک', 'گلناز']
    
    last_names = ['محلاتی', 'کریمی', 'حسینی', 'رضوی', 'نوری', 'یزدی', 'شیرازی', 'کاشانی', 
                  'اصفهانی', 'تبریزی', 'فردوسی', 'سهرابی', 'مهرآور', 'فرخزاد', 'شمسی']
    
    # تاریخ‌های ۶ ماه گذشته
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    print("🔄 در حال تولید داده‌های مهمانان...")
    
    # --- تولید داده‌های مهمانان ---
    guests = []
    for i in range(200):
        guest = {
            'guest_id': f'G{1000+i}',
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'email': f'guest{i}@example.com',
            'phone': f'0912{random.randint(1000000, 9999999)}',
            'city': random.choice(['تهران', 'شیراز', 'اصفهان', 'مشهد', 'تبریز', 'یزد', 'کاشان', 'کرمان']),
            'first_visit': random.choice(date_range).strftime('%Y-%m-%d'),
            'total_visits': random.randint(1, 12),
            'preferences': random.choice(['موسیقی', 'شعر', 'فیلم', 'هنر', 'تاریخ', 'غذا', 'معماری']),
            'loyalty_score': round(random.uniform(0, 100), 1)
        }
        guests.append(guest)
    
    guests_df = pd.DataFrame(guests)
    guests_df.to_csv('data/guests.csv', index=False, encoding='utf-8-sig')
    print(f"✅ {len(guests_df)} مهمان ساخته شد!")
    
    # --- تولید داده‌های رزرو ---
    print("🔄 در حال تولید داده‌های رزرو...")
    reservations = []
    room_types = ['اتاق سنتی', 'اتاق مدرن', 'سوئیت', 'اتاق خانوادگی']
    event_names = ['شب شعر', 'کنسرت موسیقی', 'تحلیل فیلم', 'کارگاه خوشنویسی', 'شب داستان‌گویی', 
                   'نمایشگاه نقاشی', 'شب موسیقی سنتی']
    channels = ['Website', 'Booking.com', 'Instagram', 'Phone', 'Walk-in', 'Google Hotels']
    
    for i in range(500):
        check_in = random.choice(date_range)
        stay_days = random.randint(1, 5)
        check_out = check_in + timedelta(days=stay_days)
        
        # ۳۰٪ رزروها با ایونت همراه هستند
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
    print(f"✅ {len(reservations_df)} رزرو ساخته شد!")
    
    # --- تولید داده‌های ایونت‌ها ---
    print("🔄 در حال تولید داده‌های ایونت‌ها...")
    events = []
    event_types = ['شب شعر بهار', 'کنسرت نی', 'تحلیل فیلم سینمایی', 'کارگاه شعر معاصر', 
                   'شب موسیقی سنتی', 'نمایشگاه عکس', 'جشنواره فیلم کوتاه']
    
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
            'category': random.choice(['موسیقی', 'شعر', 'فیلم', 'هنر'])
        }
        events.append(event)
    
    events_df = pd.DataFrame(events)
    events_df.to_csv('data/events.csv', index=False, encoding='utf-8-sig')
    print(f"✅ {len(events_df)} ایونت ساخته شد!")
    
    print("\n🎉 همه داده‌ها با موفقیت در پوشه 'data' ذخیره شدند!")
    return guests_df, reservations_df, events_df

# اگر فایل مستقیم اجرا شود
if __name__ == "__main__":
    generate_sample_data()

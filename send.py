import pandas as pd
import pywhatkit as kit
import time
import re

# Load contacts CSV with phone numbers as strings to keep leading zeros
contacts = pd.read_csv('contacts.csv', dtype={'Phone': str})
contacts.columns = contacts.columns.str.strip()

def format_phone(phone):
    phone = str(phone).strip()
    phone = re.sub(r'[^\d+]', '', phone)  # Keep digits and '+'

    # Already valid international format +countrycode
    if phone.startswith('+') and re.fullmatch(r'\+\d{10,15}', phone):
        return phone

    # Bangladesh number starting with 880 (without '+')
    if phone.startswith('880') and len(phone) == 13:
        return '+' + phone


    # Bangladesh number starting with 0 and 11 digits total
    if phone.startswith('0') and len(phone) == 11:
        return '+880' + phone[1:]

    # 11 digits number without prefix, assume BD and add +88
    if re.fullmatch(r'\d{11}', phone):
        return '+880' + phone

    # Invalid format
    
    return None

def generate_message(name):
    return f"""প্রিয় {name} ভাই/আপু,

আমি H4K2LIV3 কমিউনিটির পক্ষ থেকে AZAM বলছি।

আপনি HackToLive  Community এর Free✅ Learn Cybersecurity Batch - 07 এ জয়েন করার জন্য স্টুডেন্ট ফর্ম ফিলাপ করেছিলেন। আমরা খুব শিঘ্রই আমাদের Batch - 07 এর কার্যক্রম শুরু করতে যাচ্ছি। তারই পরিপ্রেক্ষিতে [ আজ ১৬ তারিখ বুধবার রাত ১০ টায় ] আপনাদের সাথে আমাদের একটি Introduction মিটিং রাখা হয়েছে।

সেখানে আমরা আপনাদের সাথে পরিচিত হবো এবং আমাদের সকল রুলস গুলো জানিয়ে দেওয়া হবে, সেই সাথে আপনাদের সকল প্রশ্নের উত্তর দেওয়া হবে ইনশাআল্লাহ। আজকের মিটিং এ অবশ্যই উপস্থিত থাকবেন।

Join Discord voice channel link: https://discord.com/channels/1142016529014214746/1143005048897536011

Meeting Time : Tonight at 10 PM

আশা করি ✅সম্পূর্ণ ফ্রিতে✅ সাইবার সিকিউরিটি শেখার জার্নিতে আপনাকে পেয়ে আমাদের কমিউনিটির উদ্দেশ্য সফল হবে।

ধন্যবাদ 
HackToLive Community"""

for index, row in contacts.iterrows():
    name = str(row['Name']).strip()
    raw_phone = row['Phone']
    phone = format_phone(raw_phone)

    if not phone:
        print(f"⚠️ Skipping invalid phone number: {raw_phone} (Name: {name})")
        continue

    message = generate_message(name)

    try:
        print(f"📤 Sending message to {name} ({phone})")
        kit.sendwhatmsg_instantly(phone_no=phone, message=message, wait_time=10, tab_close=True)
        time.sleep(15)  # wait between messages to avoid blocks
    except Exception as e:
        print(f"❌ Failed to send message to {name} ({phone}): {e}")

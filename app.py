import streamlit as st
import json
import os
import random
from datetime import datetime

# --- إعدادات الصفحة (ممنوع اللمس) ---
st.set_page_config(page_title="The Final Kingdom of Sally", page_icon="👑", layout="centered")

DB_FILE = "data.json"

# --- تحميل البيانات وحفظها ---
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: 
                return json.load(f)
        except: 
            return None
    return None

def save_data(data):
    with open(DB_FILE, "w") as f: 
        json.dump(data, f)

# --- إعداد قاعدة البيانات في الجلسة ---
if 'db' not in st.session_state:
    saved_db = load_data()
    st.session_state.db = saved_db if saved_db else {
        "current_gift": 100,
        "viewing_gift": False,
        "page": "vow_text",
        "authenticated": False,
        "memories": [],
        "secret_messages": []
    }

# --- القفل الذكي: يطلب الرمز عند تحديث الصفحة ---
if 'session_auth' not in st.session_state:
    st.session_state.session_auth = False

# --- حساب الوقت مع بعض ---
def get_together_time():
    start_date = datetime(2024, 7, 13)
    now = datetime.now()
    diff = now - start_date
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days} يوم و {hours} ساعة و {minutes} دقيقة و {seconds} ثانية"

# --- التنسيقات الجمالية ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&family=Cairo:wght@700;900&family=Aref+Ruqaa:wght@700&display=swap');

.stApp { 
    background: linear-gradient(-45deg, #ee9ca7, #ffafbd, #ffc3a0, #ffafbd);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    background-attachment: fixed; 
}
@keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }

.ultra-royal-card { 
    background: rgba(255, 255, 255, 0.2); 
    backdrop-filter: blur(25px); 
    border-radius: 50px; 
    border: 2px solid rgba(255,255,255,0.5); 
    padding: 40px; 
    text-align: center; 
    box-shadow: 0 25px 50px rgba(0,0,0,0.1); 
    margin-bottom: 20px;
}

.diamond-title { font-family: 'Cairo', sans-serif; font-size: 55px !important; color: #ad1457; text-shadow: 2px 2px 10px rgba(0,0,0,0.1); }

.big-vow-text { 
    font-family: 'Aref Ruqaa', serif; font-size: 45px !important; color: #c2185b; 
    line-height: 1.6; text-align: center; padding: 25px;
    background: rgba(255,255,255,0.4); border-radius: 35px; border: 1px solid white;
}

.vow-box { 
    font-family: 'Amiri', serif; font-size: 35px !important; color: #880e4f; 
    padding: 35px; background: white; border-radius: 30px; 
    border-right: 20px solid #ff4d6d; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}

.tip-box { 
    font-family: 'Amiri', serif; font-size: 40px !important; color: #ad1457; 
    padding: 40px; background: rgba(255,255,255,0.85); border-radius: 35px; 
    border: 2px dashed #ff85a2;
}

.mega-counter { font-size: 150px !important; color: white; font-family: 'Cairo'; line-height: 1; text-shadow: 0 10px 20px rgba(0,0,0,0.2); }

.stButton>button { 
    background: linear-gradient(90deg, #ff4d6d, #c9184a) !important; 
    color: white !important; border-radius: 50px !important; padding: 18px !important; 
    font-size: 20px !important; font-weight: bold; width: 100%; border: none; transition: 0.4s;
}
.stButton>button:hover { transform: scale(1.02); box-shadow: 0 15px 30px rgba(201, 24, 74, 0.3); }

.memory-item { background: white; padding: 20px; margin: 10px; border-radius: 20px; text-align: right; border-bottom: 5px solid #ffafbd; font-size: 20px; }

.nav-bar { background: rgba(255,255,255,0.5); padding: 10px; border-radius: 100px; margin-bottom: 20px; display: flex; justify-content: space-around; }

header, footer, #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- قائمة الوعد المئة ---
vows_list = ["الوعد {}: كل عام وأنتِ بخير، أعدكِ أن أكون لكِ الأمان الذي لا يخون.".format(i) for i in range(1,101)]

# --- قائمة النصائح ---
tips_list = [
    "ابتسامتكِ دواء لروحي.", "لا تدعي الحزن يقربكِ.", "أنتِ قوية جداً.", 
    "ثقي بنفسكِ دائماً.", "قلبي معكِ دائماً."
]

# --- نظام الدخول --- 
if not st.session_state.session_auth:
    st.markdown('<div class="ultra-royal-card">', unsafe_allow_html=True)
    st.markdown('<p class="diamond-title">مَمْلَكَةُ سَالِي الأبدية</p>', unsafe_allow_html=True)
    pw = st.text_input("أدخلي ميثاق الدخول الملكي:", type="password", placeholder="أكتبي الرمز هنا...")
    if st.button("فتح البوابات ✨"):
        if pw == "180111124": 
            st.session_state.session_auth = True
            st.rerun()
        else: st.error("عذراً ملكتي.. الرمز خاطئ.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()
    # --- صفحات المقدمة ---
if st.session_state.db["page"] == "vow_text":
    st.markdown('<div class="ultra-royal-card">', unsafe_allow_html=True)
    st.markdown('<div class="big-vow-text">🌸 كل عام وأنتِ بمليون خير يا سالي 🌸</div>', unsafe_allow_html=True)
    
    greeting_msg = """
    إلى ملكة قلبي "سالي"..
    في هذا اليوم السعيد، أجدد لكِ عهد الوفاء الذي لا ينكسر.
    أنتِ لستِ فقط حبيبتي، أنتِ موطني، أماني، وضحكتي التي تلون أيامي.
    كل عام وأنتِ تسكنين قلبي، وكل عام وأنا أزداد بكِ فخراً.
    أعدكِ أن أبقى السند، أن أبقى الأمان، وأن أحبكِ مئة ضعف المئة.. للأبد.
    """
    st.markdown(f'<div style="font-family:Cairo; font-size:24px; color:#4a001f; text-align:center; padding:20px; font-weight:bold;">{greeting_msg}</div>', unsafe_allow_html=True)
    
    vow_long_html = f"""<div style="height:300px; overflow-y:scroll; text-align:right; font-family:'Amiri'; font-size:24px; padding:25px; background:rgba(255,255,255,0.4); border-radius:30px; border:1px solid #ffafbd;">
    أعدكِ بكل سطر وبكل نبضة...<br><br>""" + "<br>".join([f"السطر {i}: مئة ضعف الوفاء والحب لكِ يا سالي." for i in range(1, 101)]) + "</div>"
    st.markdown(vow_long_html, unsafe_allow_html=True)

    if st.button("تأكيد الميثاق.. اذهب للصوت 🎙️"):
        st.session_state.db["page"] = "audio_page"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.db["page"] == "audio_page":
    st.markdown('<div class="ultra-royal-card">', unsafe_allow_html=True)
    st.markdown('<p class="diamond-title">صوتُ الوفاء</p>', unsafe_allow_html=True)

    AUDIO_FILE = "sally_voice.aac"
    if os.path.exists(AUDIO_FILE):
        with open(AUDIO_FILE, "rb") as f:
            st.audio(f.read(), format="audio/aac")
    else:
        st.warning("ملف الصوت غير موجود")

    if st.button("سماع الصوت.. اذهب للميثاق 📜"):
        st.session_state.db["page"] = "mithaq_page"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.db["page"] == "mithaq_page":
    st.markdown('<div class="ultra-royal-card">', unsafe_allow_html=True)
    st.markdown('<p class="diamond-title">ميثاق الرجال</p>', unsafe_allow_html=True)
    st.markdown('<div class="vow-box">"أعاهدُ الله وأعاهدُكِ، أن أصونكِ في غيابكِ قبل حضوركِ، وأن أكون لكِ أباً وأخاً وحبيباً.. هذا عهدُ رَجُلٍ لا يخون."</div>', unsafe_allow_html=True)
    if st.button("قسم الوفاء.. ادخلي المملكة ✨"):
        st.session_state.db["page"] = "home"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- النظام الرئيسي (الصفحة الرئيسية: المملكة، الراحة، الأرشيف، الأوسمة، الخزنة) ---
elif st.session_state.db["page"] in ["home", "safe", "archive", "achievements", "malyaze"]:
    
    # عداد الوقت مع حبنا
    st.markdown(f'<div style="text-align:center;"><div style="background:white; border-radius:50px; padding:8px 30px; display:inline-block; font-family:Cairo; color:#c2185b; box-shadow:0 5px 15px rgba(0,0,0,0.05);">⌛ مضى على حبنا: {get_together_time()}</div></div>', unsafe_allow_html=True)
    
    # ناف بار ملكي (خانات فوق)
    c = st.columns(6)
    pages = ["home", "safe", "archive", "achievements", "malyaze", "vow_text"]
    icons = ["🏰", "☁️", "🎞️", "🏅", "🔐", "📜"]
    for i in range(6):
        with c[i]: 
            if st.button(icons[i]): st.session_state.db["page"] = pages[i]; st.rerun()

# --- خانة المملكة: الوعد الملكي ---
    if st.session_state.db["page"] == "home":
        st.markdown('<div class="ultra-royal-card">', unsafe_allow_html=True)
        st.markdown(f'<p class="mega-counter">{st.session_state.db["current_gift"]}</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#880e4f; font-family:Cairo; font-size:24px;">وعد متبقي لكِ في ذمتي</p>', unsafe_allow_html=True)
        
        idx = 100 - st.session_state.db["current_gift"]
        if st.session_state.db["current_gift"] > 0:
            if not st.session_state.db.get("viewing_gift"):
                if st.button(f"🎁 افتحي الوعد الملكي رقم {idx + 1}"):
                    st.session_state.db["viewing_gift"] = True; st.rerun()
            else:
                st.markdown(f'<div class="vow-box">{vows_list[idx]}</div>', unsafe_allow_html=True)
                note = st.text_input("احفظي ذكرى لهذا الوعد 🔒")
                if st.button("❤️ تخليد الوعد في تاريخنا"):
                    if note: st.session_state.db["memories"].append(f"وعد {idx+1}: {note}")
                    st.session_state.db["current_gift"] -= 1
                    st.session_state.db["viewing_gift"] = False
                    save_data(st.session_state.db); st.balloons(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        # --- خانة راحة القلب ---
if st.session_state.db["page"] == "safe":
    st.markdown('<div class="ultra-royal-card">', unsafe_allow_html=True)
    st.markdown('<p class="diamond-title">راحة قلبكِ 🌿</p>', unsafe_allow_html=True)
    st.progress(random.randint(80, 100) / 100)
    
    mood = st.select_slider("كيف حال نبضكِ الآن؟", options=["متعب", "هادئ", "بخير", "سعيد", "فوق الغيم"])
    
    if st.button("أريد نصيحة تقوي قلبي ✨"):
        st.markdown(f'<div class="tip-box">{random.choice(tips_list)}</div>', unsafe_allow_html=True)
        st.snow()
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- خانة ملاذي السري ---
elif st.session_state.db["page"] == "malyaze":
    st.markdown('<div class="ultra-royal-card">', unsafe_allow_html=True)
    st.markdown('<p class="diamond-title">🔐 ملاذي السري</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#4a001f;">هنا تگدرين تكتبين أي شي ببالج، رسالة، فضفضة، أو أي شي يبقى مخزون للأبد</p>', unsafe_allow_html=True)
    
    secret = st.text_area("أكتبي ما في قلبكِ هنا...")
    if st.button("إرسال إلى الخزنة 🔒"):
        if secret:
            st.session_state.db["secret_messages"].append(f"{datetime.now().strftime('%Y-%m-%d')}: {secret}")
            save_data(st.session_state.db)
            st.success("تم الحفظ في أعماق المملكة.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- خانة صندوق الذكريات ---
elif st.session_state.db["page"] == "archive":
    st.markdown('<div class="ultra-royal-card">', unsafe_allow_html=True)
    st.markdown('<p class="diamond-title">صندوق الذكريات 🎞️</p>', unsafe_allow_html=True)
    
    if st.session_state.db["current_gift"] > 0:
        st.warning("🔒 الخزنة تفتح بالكامل بعد الـ 100 وعد.")
    else:
        tab1, tab2 = st.tabs(["وعودنا", "رسائلج السرية"])
        with tab1:
            for m in st.session_state.db["memories"]:
                st.markdown(f'<div class="memory-item">{m}</div>', unsafe_allow_html=True)
        with tab2:
            for s in st.session_state.db.get("secret_messages", []):
                st.markdown(f'<div class="memory-item" style="border-bottom-color:#c2185b;">{s}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- خانة الأوسمة الملكية ---
elif st.session_state.db["page"] == "achievements":
    st.markdown('<div class="ultra-royal-card">', unsafe_allow_html=True)
    st.markdown('<p class="diamond-title">أوسمة الملكة 🏅</p>', unsafe_allow_html=True)
    
    done = 100 - st.session_state.db["current_gift"]
    col1, col2 = st.columns(2)
    if done >= 10: col1.markdown('<div style="background:#fff3f5; padding:20px; border-radius:20px; border:2px solid #ffafbd;">🏅<br>وسام البداية الصادقة</div>', unsafe_allow_html=True)
    if done >= 50: col2.markdown('<div style="background:#fff3f5; padding:20px; border-radius:20px; border:2px solid #ff4d6d;">💖<br>وسام الوفاء المستمر</div>', unsafe_allow_html=True)
    if done == 100: st.markdown('<div style="background:linear-gradient(to right, #ffd700, #fff); padding:30px; border-radius:30px; margin-top:20px;">👑 تاج المملكة الأبدي 👑</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- ترتيب أسماء الأقسام تحت الأيقونات (فوق) ---
st.markdown("""
<div style="display:flex; justify-content:space-around;
font-family:Cairo; font-size:18px; color:#880e4f; font-weight:bold;">
<span>المملكة</span>
<span>راحة القلب</span>
<span>صندوق الذكريات</span>
<span>الأوسمة الملكية</span>
<span>ملاذي السري</span>
<span>الميثاق</span>
</div>
""", unsafe_allow_html=True)
# =====================================
# اقتباسات حب عشوائية
# =====================================
love_quotes = [
    "وجودكِ في حياتي أجمل قدر.",
    "أنتِ أجمل صدفة حدثت لي.",
    "قلبي اختاركِ دون تفكير.",
    "كل يوم معكِ هو نعمة.",
    "أنتِ بداية كل شيء جميل.",
    "وجودكِ يجعل حياتي أجمل.",
    "أنتِ الحلم الذي تحقق.",
    "أنا محظوظ لأنكِ في حياتي.",
    "أحبكِ أكثر مما تتخيلين.",
    "أنتِ النور في أيامي.",
    "وجودكِ يمنح قلبي السلام.",
    "كل لحظة معكِ ذكرى جميلة.",
    "أنتِ أعظم هدية في حياتي."
]

st.markdown(
f"<div style='text-align:center;font-family:Cairo;font-size:20px;color:#c2185b;margin-top:10px;'>💌 {random.choice(love_quotes)}</div>",
unsafe_allow_html=True
)

# =====================================
# تاريخ بداية القصة
# =====================================
st.markdown(
"<div style='text-align:center;font-family:Cairo;font-size:18px;color:#ad1457;'>📅 بداية قصتنا: 13 / 7 / 2024</div>",
unsafe_allow_html=True
)

# =====================================
# عداد عيد ميلاد سالي
# =====================================
today = datetime.now()
birthday_this_year = datetime(today.year, 3, 16)

if today > birthday_this_year:
    birthday_this_year = datetime(today.year + 1, 3, 16)

days_left = (birthday_this_year - today).days

st.markdown(
f"<div style='text-align:center;font-family:Cairo;font-size:20px;color:#880e4f;'>🎂 باقي على عيد ميلاد سالي: {days_left} يوم</div>",
unsafe_allow_html=True
)

# =====================================
# حساب عمر سالي
# =====================================
birth_date = datetime(2003, 3, 16)
age = today.year - birth_date.year
if (today.month, today.day) < (birth_date.month, birth_date.day):
    age -= 1

st.markdown(
f"<div style='text-align:center;font-family:Cairo;font-size:18px;color:#c2185b;'>👑 عمر الملكة حالياً: {age} سنة</div>",
unsafe_allow_html=True
)

# =====================================
# زر مفاجأة ملكية (مع عرض أكبر وأجمل)
# =====================================
if st.button("🎲 مفاجأة ملكية"):
    surprises = [
        "أنتِ أجمل شيء حدث في حياتي.",
        "أنا فخور بكِ دائماً.",
        "وجودكِ يجعل الدنيا أجمل.",
        "ابتسامتكِ تساوي العالم.",
        "أنتِ ملكة قلبي للأبد.",
        "أنا ممتن لوجودكِ في حياتي.",
        "كل يوم معكِ نعمة.",
        "اليوم يومك المشرق يا سالي 🌸",
        "أنتِ فرحة قلبي الدائمة.",
        "سحر حضورك لا يزول أبداً."
    ]
    message = random.choice(surprises)
    st.markdown(
        f"""
        <div style="
            text-align:center; 
            font-family:Cairo; 
            font-size:36px; 
            color:#c2185b; 
            background:rgba(255,255,255,0.8); 
            padding:40px; 
            border-radius:35px; 
            border:3px solid #ff4d6d;
            box-shadow: 0 15px 30px rgba(201, 24, 74, 0.3);
        ">
        🎉 {message} 🎉
        </div>
        """, unsafe_allow_html=True
    )
# =====================================
# نهاية الكود العملاق
# =====================================
st.markdown("<hr style='border:2px solid #ff85a2;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; font-family:Cairo; font-size:16px; color:#880e4f;'>👑 كل شيء مرتب، كل الخانات مفعلة، وكل المفاجآت جاهزة! 👑</div>", unsafe_allow_html=True)
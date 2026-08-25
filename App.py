import os
from PIL import Image
import g4f
import streamlit as st

# 1. إعدادات الصفحة والمسارات
st.set_page_config(page_title="منظومة الذكاء الاصطناعي", page_icon="🤖", layout="wide")

# إنشاء مجلد الكوكيز تلقائياً لمنع أخطاء HAR
cookies_dir = "./har_and_cookies"
if not os.path.exists(cookies_dir):
    os.makedirs(cookies_dir, exist_ok=True)
g4f.cookies_dir = cookies_dir

# 2. القائمة الجانبية وإدارة الأقسام
st.sidebar.title("📊 إدارة المنظومة والشركات")
role = st.sidebar.selectbox(
    "اختر وضع المساعد / الشركة:",
    [
        "👨‍💼 المستشار الشخصي ومدير الأعمال",
        "📊 قسم إدارة المشاريع والشركات",
        "📈 قسم التحليل المالي والاستثمار",
        "💻 قسم التطوير الذاتي والتحديث البرمجي",
    ],
)

st.title("🤖 منظومة الذكاء الاصطناعي التفاعلية")

# 3. قسم رفع الملفات (صور وفيديوهات من المعرض)
st.subheader("📁 رفع الوسائط من المعرض")
uploaded_file = st.file_uploader(
    "اختر صورة أو مقطع فيديو للتطوير والتحليل:",
    type=["jpg", "jpeg", "png", "mp4", "mov"],
)

if uploaded_file is not None:
    if uploaded_file.type.startswith("image"):
        image = Image.open(uploaded_file)
        st.image(image, caption="الصورة المرفوعة", use_container_width=True)
    elif uploaded_file.type.startswith("video"):
        st.video(uploaded_file)

# 4. إدارة سجل المحادثة (الذاكرة)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. استقبال مربع النص وإرسال الطلب
prompt = st.chat_input("اطلب ما تريد يا أبو خليفة...")

if prompt:
    # عرض سؤال المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # معالجة الطلب واستدعاء نموذج الذكاء الاصطناعي
    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير والأجابة..."):
            try:
                # إعداد التعليمات البرمجية وتمرير الدور
                system_instruction = (
                    f"أنت مساعد ذكي في وضع: {role}. أجب بدقة ووضوح."
                )
                formatted_messages = [
                    {"role": "system", "content": system_instruction}
                ]

                for msg in st.session_state.messages:
                    formatted_messages.append(
                        {"role": msg["role"], "content": msg["content"]}
                    )

                # طلب الإجابة باستخدام موفر مستقر
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4o,
                    provider=g4f.Provider.Blackbox,
                    messages=formatted_messages,
                )

                # عرض الإجابة
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

                # تشغيل الصوت للرد (Text-to-Speech تلقائي)
                tts_audio = f"""
                <audio autoplay style="display:none;">
                    <source src="https://translate.google.com/translate_tts?ie=UTF-8&q={response[:200]}&tl=ar&client=tw-ob" type="audio/mpeg">
                </audio>
                """
                st.components.v1.html(tts_audio, height=0)

            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال: {e}")

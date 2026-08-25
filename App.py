import os
from google import generativeai as genai
from PIL import Image
import streamlit as st
from streamlit_mic_recorder import speech_to_text

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة الذكاء الاصطناعي", page_icon="🤖", layout="wide")

st.title("🤖 منظومة الذكاء الاصطناعي التفاعلية")

# 2. القائمة الجانبية وإدخال مفتاح API
st.sidebar.title("📊 إدارة المنظومة")
role = st.sidebar.selectbox(
    "اختر وضع المساعد / الشركة:",
    [
        "👨‍💼 المستشار الشخصي ومدير الأعمال",
        "📊 قسم إدارة المشاريع والشركات",
        "📈 قسم التحليل المالي والاستثمار",
        "💻 قسم التطوير الذاتي والتحديث البرمجي",
    ],
)

api_key = st.sidebar.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")

# 3. ميزة رفع الصور والفيديو من المعرض
st.subheader("📁 رفع الوسائط من المعرض")
uploaded_file = st.file_uploader(
    "اختر صورة أو فيديو من الاستديو:",
    type=["jpg", "jpeg", "png", "mp4", "mov"],
)

if uploaded_file is not None:
    if uploaded_file.type.startswith("image"):
        img = Image.open(uploaded_file)
        st.image(img, caption="الصورة المرفوعة", use_container_width=True)
    elif uploaded_file.type.startswith("video"):
        st.video(uploaded_file)

# 4. ميزة التحدث الصوتي المباشر (Speech to Text)
st.subheader("🎙️ التحدث الصوتي")
text_from_speech = speech_to_text(
    language="ar",
    start_prompt="اضغط للتحدث 🎤",
    stop_prompt="إيقاف التسجيل ⏹️",
    key="speech",
)

# 5. إدارة الذاكرة وسجل النص
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

text_input = st.chat_input("اطلب ما تريد يا أبو خليفة...")

# تحديد نص الإدخال سواء كان كتابة أو صوتاً
user_prompt = text_input or text_from_speech

if user_prompt:
    if not api_key:
        st.error("يرجى إدخال مفتاح Gemini API في القائمة الجانبية لتشغيل الخدمة.")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير والتحديث..."):
                try:
                    prompt_context = f"أنت مساعد ذكي في دور {role}. اجب على الطلب التالي: {user_prompt}"
                    
                    if uploaded_file and uploaded_file.type.startswith("image"):
                        response = model.generate_content([prompt_context, Image.open(uploaded_file)])
                    else:
                        response = model.generate_content(prompt_context)

                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

                    # نطق رد البوت تلقائياً
                    clean_text = response.text.replace("\n", " ").replace("'", "")
                    tts_code = f"""
                    <script>
                    var msg = new SpeechSynthesisUtterance('{clean_text[:200]}');
                    msg.lang = 'ar-SA';
                    window.speechSynthesis.speak(msg);
                    </script>
                    """
                    st.components.v1.html(tts_code, height=0)

                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال: {e}")

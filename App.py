from google import genai
from PIL import Image
import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة الذكاء الاصطناعي", page_icon="🤖", layout="wide")

# 2. القائمة الجانبية وإدارة الأقسام وإدخال مفتاح API
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

# مفتاح Google Gemini API
api_key = st.sidebar.text_input("أدخل مفتاح Gemini API:", type="password")

st.title("🤖 منظومة الذكاء الاصطناعي التفاعلية")

# 3. ميزة التحدث الصوتي ورفع الملفات
st.subheader("🎙️ التحدث الصوتي ورفع الوسائط")
col1, col2 = st.columns(2)

with col1:
    audio_input = st.audio_input("اضغط لتسجيل صوتك والتحدث مع البوت مباشرة")

with col2:
    uploaded_file = st.file_uploader(
        "اختر صورة أو مقطع فيديو من المعرض:",
        type=["jpg", "jpeg", "png", "mp4", "mov"],
    )

if uploaded_file is not None:
    if uploaded_file.type.startswith("image"):
        image = Image.open(uploaded_file)
        st.image(image, caption="الصورة المرفوعة", use_container_width=True)
    elif uploaded_file.type.startswith("video"):
        st.video(uploaded_file)

# 4. إدارة الذاكرة وسجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. معالجة النص والإدخال الصوتي
user_prompt = st.chat_input("اطلب ما تريد يا أبو خليفة...")

# إذا قام المستخدم بالتسجيل الصوتي
if audio_input and not user_prompt:
    user_prompt = "تم إرسال تسجيل صوتي، يرجى الاستجابة والمساعدة."

if user_prompt:
    if not api_key:
        st.warning(
            "يرجى إدخال مفتاح Gemini API في القائمة الجانبية لتشغيل الخدمة بنجاح."
        )
    else:
        st.session_state.messages.append(
            {"role": "user", "content": user_prompt}
        )
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير والتحديث..."):
                try:
                    client = genai.Client(api_key=api_key)

                    # إعداد السياق والذاكرة
                    prompt_with_context = (
                        f"أنت مساعد ذكي في وضع: {role}. الإجابة المباشرة: {user_prompt}"
                    )

                    response = client.models.generate_content(
                        model="gemini-2.5-flash", contents=prompt_with_context
                    )

                    st.markdown(response.text)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response.text}
                    )

                    # تشغيل الصوت لرد البوت تلقائياً
                    tts_script = f"""
                    <script>
                    var msg = new SpeechSynthesisUtterance({repr(response.text[:200])});
                    msg.lang = 'ar-SA';
                    window.speechSynthesis.speak(msg);
                    </script>
                    """
                    st.components.v1.html(tts_script, height=0)

                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال: {e}")

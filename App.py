import streamlit as st
import g4f
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة الذكية", page_icon="🤖", layout="wide")

# 2. القائمة الجانبية لإدارة المهام والأقسام
st.sidebar.title("🏢 إدارة المنظومة والشركات")
role = st.sidebar.selectbox(
    "اختر وضع المساعد / الشركة:",
    [
        "👨‍💼 المستشار الشخصي ومدير الأعمال",
        "📊 قسم إدارة المشاريع والشركات",
        "📈 قسم التحليل المالي والاستثمار",
        "💻 قسم التطوير الذاتي والتحديث البرمجي"
    ]
)

st.sidebar.markdown("---")
st.sidebar.write("📸 **مرفقات:** يمكنك رفع الصور والملفات أدناه ليتعامل معها النظام:")
uploaded_file = st.sidebar.file_uploader("رفع صورة للتحليل:", type=["png", "jpg", "jpeg"])

# 3. ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 منظومة الذكية")
st.caption(f"الوضع الحالي: **{role}** (يعمل بشكل مباشر وبدون API)")

# عرض المحادثات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. استقبال الأوامر
if prompt := st.chat_input("اطلب ما تريد يا أبو خليفة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # بناء تعليمات النظام
    system_instruction = f"أنت تعمل الآن بصفتك: {role}. أجب بدقة واحترافية كصديق ومدير أعمال لأبو خليفة."
    
    if "تطوير" in role or "التحديث" in role:
        system_instruction += " إذا طلب منك أبو خليفة تعديل الكود أو إضافة ميزة، قم بكتابة الكود البرمجي الجديد المحدث فوراً."

    full_prompt = f"{system_instruction}\n\nسؤال/أمر أبو خليفة: {prompt}"

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("جاري التفكير والرد..."):
            try:
                # إرسال الطلب عبر محرك مجاني بدون API Key
                response = g4f.ChatCompletion.create(g4f.cookies_dir = "./har_and_cookies"
                    model=g4f.models.gpt_4o,
                    messages=[{"role": "user", "content": full_prompt}]
                )
                * حدد الموفر صراحة ليكون **Blackbox** أو **DDG** لتتجنب خطأ Copilot/OpenaiChat:
  ```python
  provider=g4f.Provider.Blackbox
                reply_text = str(response)
                message_placeholder.markdown(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text})
            except Exception as e:
                message_placeholder.error(f"حدث خطأ في الاتصال بالمحرك المجاني: {e}")
uploaded_file = st.file_uploader(
    "اختر صورة أو فيديو من الاستديو", type=["jpg", "png", "mp4"]
)
* **لإضافة التسجيل الصوتي:**
  أضف أداة استقبال الصوت المدمجة:
  ```python
  audio_val = st.audio_input("سجل صوتك للتحدث مع البوت")

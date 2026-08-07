import streamlit as st
import os
import edge_tts
import asyncio
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(token=HF_TOKEN)
async def generate_audio(text):
    communicate = edge_tts.Communicate(text, "ru-RU-DmitryNeural")
    await communicate.save("audio.mp3")
st.title("MindBridge")
st.subheader("Адаптация учебных материалов с помощью искусственного интеллекта")
st.markdown("""
#### Что такое MindBridge?

MindBridge — это образовательное веб-приложение, которое помогает адаптировать учебные материалы под разные образовательные потребности с помощью искусственного интеллекта.

Пользователь вставляет учебный текст, выбирает необходимый тип поддержки и получает адаптированную версию материала, которая становится проще и удобнее для восприятия.
""")

st.divider()
st.info(
    "Вставьте учебный материал, выберите необходимый тип поддержки, "
    "и MindBridge автоматически адаптирует текст для более удобного обучения."
)
st.subheader("Адаптация учебного материала")
student_need = st.selectbox(
    "Выберите образовательную потребность:",
   [
       
    "Общая поддержка обучения",
    "Дислексия",
    "СДВГ (ADHD)",
    "Нарушение зрения",
    "Нарушение слуха"
]
)
text = st.text_area(
    "📄 Вставьте текст из учебника, статьи или конспекта:",
    height=200,
    placeholder="Например: вставьте параграф из учебника, научной статьи или конспекта..."
)

support = st.selectbox(
    "Что нужно сделать с текстом?",
    [
       "Упростить текст",
       "Структурировать текст",
       "Объяснить сложные слова",
       "Создать краткое содержание"
    ]
)
need_instructions = {
    "СДВГ (ADHD)": """
Use short sections.
Highlight key ideas.
Avoid long paragraphs.
Use bullet points when helpful.
Do not add adaptations for other accessibility needs.
""",

    "Дислексия": """
Use short, clear sentences.
Avoid unnecessarily difficult words.
Separate information into small sections.
Explain complex terms simply.
Do not add adaptations for other accessibility needs.
""",

    "Нарушение зрения": """
Use clear text-based explanations.
Do not rely on phrases such as "as shown above".
Describe important visual information in words when it exists in the original material.
Do not add adaptations for other accessibility needs.
""",

    "Нарушение слуха": """
Present all necessary information clearly in written form.
Use clear headings and short sections.
Use bullet points for key information when helpful.
Make all explanations understandable without audio or spoken instructions.
Clearly write out any information that would normally be explained verbally.
Keep important academic information accurate.
Do not add adaptations for other accessibility needs.
""",

    "Общая поддержка обучения": """
Use clear, student-friendly language.
Keep important academic information accurate.
Do not add adaptations for other accessibility needs.
"""
}
if  st.button("Адаптировать материал"):
    if not text:
        st.warning("Сначала вставьте учебный материал.")
    elif not HF_TOKEN:
        st.error("Токен Hugging Face не найден.")
    else:
        prompt = f"""
You are an educational assistant specializing in adapting educational materials for inclusive education.

Your task is NOT to summarize unless the user specifically asks for a summary.

Always adapt the text according to the selected educational need.

Rules:
- Use simple and clear language.
- Keep all important facts.
- Do not invent new information.
- Split long paragraphs into short ones.
- Use bullet points whenever appropriate.
- Explain difficult words in simple language.
- Make the material easy for students to understand.

Learner accessibility need:
{student_need}

Student request:
{support}

Special adaptation instructions:
{need_instructions[student_need]}

Original text:
{text}
        
Adapt the learning material according to the accessibility instructions above
and the student's request.

Important rules:
- Always answer in the SAME language as the original text.
- Never translate the text unless the student explicitly asks for translation.
- Follow ONLY the accessibility instructions for the selected learner need.
- Do not mention disabilities or diagnoses unless necessary.
- Do not say that the material was adapted for ADHD, dyslexia, visual impairment, or hearing impairment.
- Keep all important academic information accurate.
- Do not invent information that is not supported by the original material.
- Do not repeat sentences or duplicate information.
- Preserve the original language of the learning material.
- Do not translate the learning material unless the student explicitly requests translation.
- Do not summarize the text unless the student explicitly requests a summary.
- Do not use phrases like "Summary", "Brief summary", or "Here is a summary" unless requested.
- Do not rewrite or simplify the entire text.
- Keep the original text unchanged whenever possible.
- Only explain difficult words and phrases.
- After the text, create a section called "Сложные слова".
- Explain each difficult word or phrase in simple language.
- Do not summarize the text.
- Return only the adapted learning material.

Learning material:
{text}
"""





        try:
            with st.spinner("Обрабатываем материал..."):
                response = client.chat.completions.create(
                    model="Qwen/Qwen2.5-7B-Instruct",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=700
                )



            result = response.choices[0].message.content
            st.session_state["result"] = result
        
            
        except Exception as e:
            st.error(f"Something went wrong: {e}")

if "result" in st.session_state:
    result = st.session_state["result"]

    st.divider()
    st.subheader("✨ Адаптированный материал")
    st.info("Материал адаптирован в соответствии с выбранным режимом обучения.")
    st.markdown(result)

    if student_need != "Нарушение слуха":
        if st.button("🔊 Прослушать материал"):
            try:
                with st.spinner("Создаем озвучку..."):
                    import re
                    clean_text = re.sub(r'#+', '', result)
                    asyncio.run(generate_audio(clean_text))
                    st.session_state["audio_ready"] = True
            except Exception:
                st.error("Audio could not be generated.Please try again.")

            if st.session_state.get("audio_ready"):
               st.audio("audio.mp3")
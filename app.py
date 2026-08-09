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
    "Вставьте учебный материал:",
    height=200,
    placeholder="Вставьте сюда текст из учебника, задания или урока..."
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
        action_instructions = {
            "Упростить текст": """
Rewrite the ENTIRE text in simpler, student-friendly language.
Keep all important facts and academic meaning.
Use short sentences and short paragraphs.
If a technical term is necessary, explain it briefly IN THE SAME SENTENCE where it appears.
Do NOT create a section called 'Сложные слова'.
Do NOT add a glossary, definitions list, summary, or audio instructions.
Do NOT remove important information just to make the text shorter.
""",
            "Структурировать текст": """
Keep the original information and meaning.
Organize it with clear headings, short sections, numbered steps, or bullet points where useful.
Do NOT create a section called 'Сложные слова'.
Do NOT summarize the material.
Do NOT add a glossary or extra explanations that were not requested.
""",
            "Объяснить сложные слова": """
Keep the original text unchanged as much as possible.
Then add a section called 'Сложные слова' and explain only the difficult terms that actually appear in the text.
Do NOT rewrite or summarize the whole material.
""",
            "Создать краткое содержание": """
Create ONLY a concise summary of the original material.
Keep the key ideas, facts, and important relationships.
Do NOT rewrite the entire text.
Do NOT create a section called 'Сложные слова'.
Do NOT explain individual terms.
Do NOT add a glossary, examples, or unrelated information.
"""
        }

        prompt = f"""
You are an educational assistant for inclusive education.

Learner accessibility need: {student_need}
Student request: {support}

Accessibility instructions:
{need_instructions[student_need]}

ACTION-SPECIFIC INSTRUCTIONS:
{action_instructions[support]}

Important rules:
- Perform ONLY the selected action: {support}.
- Do not perform other actions just because they might be useful.
- Follow ONLY the accessibility instructions for the selected learner need.
- Do not mention disabilities or diagnoses unless necessary.
- Keep important academic information accurate.
- Do not invent information that is not supported by the original material.
- Return only the final result.

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
                    max_tokens=1200
                )



            result = response.choices[0].message.content
            st.session_state["result"] = result
            st.session_state["audio_ready"] = False
        
            
        except Exception as e:
            st.error(f"Something went wrong: {e}")

if "result" in st.session_state:
    result = st.session_state["result"]

    st.divider()
    st.subheader("✨ Адаптированный материал")
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
                st.error("Audio could not be generated. Please try again.")

        if st.session_state.get("audio_ready"):
            st.audio("audio.mp3")

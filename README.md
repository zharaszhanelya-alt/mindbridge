# MindBridge

AI-powered platform that adapts educational materials to different learning needs.

## Problem

Educational materials are often presented in the same format for all students, even though students have different learning needs.

This can make learning more difficult for students with dyslexia, ADHD, visual or hearing impairments, as well as for students who need additional learning support.

## Solution

MindBridge is a web application that adapts educational materials according to the user's learning needs.

The user:
1. Selects a learning need.
2. Selects an adaptation method.
3. Enters educational material.
4. Receives an adapted version of the material.

## AI / ML Logic

MindBridge uses the Qwen 2.5 7B Instruct language model through the Hugging Face Inference API.

The application sends the educational text together with instructions based on the selected learning need and adaptation method.

The AI model processes the material and generates an adapted version.

## Technology Stack

- Python
- Streamlit
- Hugging Face Inference API
- Qwen 2.5 7B Instruct
- Edge TTS
- python-dotenv

## Project Structure

- app.py — main application
- requirements.txt — project dependencies
- README.md — project documentation

## Установка

Установите необходимые зависимости:
```bash
pip install -r requirements.txt
```
Создайте файл .env и добавьте Hugging Face API-токен:

```text
HF_TOKEN=your_token_here
```
Запустите приложение:
```bash
streamlit run app.py
```
## Демо

Ссылка на видео-демонстрацию: [ДОБАВИТЬ ССЫЛКУ]

## Дальнейшее развитие

В дальнейшем планируется расширить набор доступных 
адаптаций, протестировать MindBridge на большей группе учеников и повысить точность персонализации.

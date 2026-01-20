from deep_translator import GoogleTranslator

def auto_translate(text: str, source: str, target: str) -> str:
    if not text:
        return ""
    try:
        translated = GoogleTranslator(source=source, target=target).translate(text)
        return translated
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return f"[{target}] {text}"
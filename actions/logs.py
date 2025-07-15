def run():
    try:
        with open("/root/GPT_monitoring/update_log.txt", "r", encoding="utf-8") as f:
            return f.read()[-4000:]
    except Exception as e:
        return f"❌ Помилка при читанні логів: {e}"

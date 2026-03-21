def generate_summary(text, query=""):
    text = text.lower()
    query = query.lower()

    sentences = text.split(".")

    # 🔥 pick most relevant sentence to query
    best_sentence = ""

    for s in sentences:
        if any(word in s for word in query.split()):
            best_sentence = s.strip()
            break

    if not best_sentence:
        best_sentence = sentences[0].strip()

    # 🔥 Simplify output
    if "access" in best_sentence:
        return {"summary": "Unauthorized access is restricted and may lead to punishment."}

    if "penalty" in best_sentence or "punish" in best_sentence:
        return {"summary": "This activity is punishable under law with fine or imprisonment."}

    if "right" in best_sentence:
        return {"summary": "This section explains rights available to citizens."}

    return {"summary": best_sentence.capitalize()}
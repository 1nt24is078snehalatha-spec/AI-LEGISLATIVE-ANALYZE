import spacy

nlp = spacy.load("en_core_web_sm")

# 🔥 TOKEN COMPRESSION
def compress_text(text):
    doc = nlp(text)

    important_sentences = []

    for sent in doc.sents:
        s = sent.text.lower()

        # keep only strong legal meaning
        if any(word in s for word in [
            "punish", "offence", "penalty",
            "imprisonment", "fine", "illegal"
        ]):
            important_sentences.append(s)

    return " ".join(important_sentences[:3])
# 🔥 KEYWORD EXTRACTION
def extract_keywords(text):
    doc = nlp(text)

    keywords = []
    for token in doc:
        if (
            token.is_alpha
            and not token.is_stop
            and len(token.text) > 4
            and token.pos_ in ["NOUN", "VERB"]
        ):
            keywords.append(token.lemma_)

    return list(set(keywords))[:5]
def extract_insights(text):
    text = text.lower()

    penalty = ""
    info = ""
    rights = ""

    if any(word in text for word in ["penalty", "punish", "fine", "imprisonment"]):
        penalty = "⚖️ This may lead to penalty such as fine or imprisonment."

    if any(word in text for word in ["shall", "must", "required", "liable"]):
        info = "📌 This is a legal obligation or responsibility."

    if any(word in text for word in ["right", "freedom", "privacy"]) and "punish" not in text:
        rights = "🛡️ This section describes rights or protections for citizens."


    return penalty, info, rights
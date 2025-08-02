import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Label options
LABELS = ["database_search", "contact_request", "misc"]

# Sample training data
TRAIN_QUERIES = [
    # DB related
    "search the patient record",
    "get appointment info",
    "show all reports",
    "fetch user data from system",

    # Contact/mail related
    "please contact the customer",
    "send an email to admin",
    "mail the details to the client",
    "call the user now",

    # Miscellaneous
    "how does this app work?",
    "what can I ask here?",
    "who are you?",
    "tell me a joke"
]

TRAIN_LABELS = [
    "database_search", "database_search", "database_search", "database_search",
    "contact_request", "contact_request", "contact_request", "contact_request",
    "misc", "misc", "misc", "misc"
]

# File paths
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")
VEC_PATH = os.path.join(os.path.dirname(__file__), "vectorizer.joblib")


def train_and_save_model():
    cleaned_queries = [q.strip().lower() for q in TRAIN_QUERIES]

    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(cleaned_queries)

    model = MultinomialNB()
    model.fit(X_train, TRAIN_LABELS)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VEC_PATH)

    return model, vectorizer


def load_model():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VEC_PATH):
        return train_and_save_model()

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VEC_PATH)
    return model, vectorizer


# Load model and vectorizer
classifier_model, classifier_vectorizer = load_model()


def classify_query(query: str, threshold: float = 0.9) -> str:
    query = query.strip().lower()
    X_test = classifier_vectorizer.transform([query])

    proba = classifier_model.predict_proba(X_test)[0]
    max_index = proba.argmax()
    predicted_label = classifier_model.classes_[max_index]
    confidence = proba[max_index]

    print(f"[DEBUG] Query: {query}")
    print(f"[DEBUG] Predicted: {predicted_label} (confidence: {confidence:.2f})")
    print(f"[DEBUG] All probabilities: {dict(zip(classifier_model.classes_, proba))}")

    if confidence >= threshold:
        return predicted_label
    else:
        print("[INFO] Confidence too low. Falling back to Gemini Flash 2.0...")

        gemini_response = ask_gemini_to_classify(query)
        return gemini_response


def ask_gemini_to_classify(query: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are a smart text classifier for a customer service system.

Classify the following user query into one of these labels:
- database_search: if the query involves retrieving or searching for data or order info.
- contact_request: if the query involves sending a message, calling, emailing, or contacting support.
- misc: if the query is not related to data or contact requests.

Return ONLY the label.

Query: "{query}"
Label:"""

        response = model.generate_content(prompt)
        label = response.text.strip().lower()

        # Validate against known labels
        if label in LABELS:
            return label
        else:
            return "misc"

    except Exception as e:
        print(f"[ERROR] Gemini fallback failed: {e}")
        return "misc"

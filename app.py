import streamlit as st
from datetime import datetime
from textblob import TextBlob

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Conversation Helper", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.main .block-container {
    max-width: 1250px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

.section-title {
    font-size: 1.08rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
}

.section-subtitle {
    color: #9aa0ab;
    font-size: 0.92rem;
    margin-bottom: 0.8rem;
}

.chat-line {
    padding: 0.65rem 0.8rem;
    border-radius: 10px;
    margin-bottom: 0.45rem;
    border: 1px solid rgba(130,140,160,0.22);
    background: rgba(26,31,44,0.40);
}

.chat-customer {
    border-left: 4px solid #f0b35f;
}

.chat-agent {
    border-left: 4px solid #61b0ff;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("Real-Time Conversation Assistant")
st.caption("Real-Time Quality Monitoring for Customer Support Interactions")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_score" not in st.session_state:
    st.session_state.last_score = None

# ---------------- FUNCTIONS ----------------
def sentiment(text):
    score = TextBlob(text).sentiment.polarity
    if score < -0.2:
        return "Negative", score
    elif score > 0.2:
        return "Positive", score
    return "Neutral", score


def analyze_agent_reply(agent_text):
    text = agent_text.lower()
    score = 10
    nudges = []

    toxic_words = ["fuck", "shit", "idiot", "stupid", "bitch"]
    if any(word in text for word in toxic_words):
        return 0, [
            "Unprofessional language detected.",
            "Use respectful tone and focus on resolution."
        ]

    empathy_words = ["sorry", "understand", "apologize"]
    if not any(word in text for word in empathy_words):
        score -= 2
        nudges.append("Add empathy to acknowledge customer concern.")

    if len(agent_text.split()) < 5:
        score -= 2
        nudges.append("Reply is too short. Add more clarity.")

    action_words = ["check", "assist", "help", "update", "resolve", "look into"]
    if not any(word in text for word in action_words):
        score -= 2
        nudges.append("Mention clear next action.")

    if "thank" not in text:
        score -= 1
        nudges.append("Use polite closing like Thank you.")

    if score < 0:
        score = 0

    return score, nudges


def latest_customer_message():
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "Customer":
            return msg["text"]
    return ""


def count_role(role):
    return sum(1 for msg in st.session_state.messages if msg["role"] == role)


def build_reply(customer_text):
    label, _ = sentiment(customer_text)

    if label == "Negative":
        return (
            "I understand your concern and I’m sorry for the inconvenience. "
            "Let me check this right away and update you shortly. Thank you."
        )
    elif label == "Neutral":
        return (
            "Thank you for the details. I’ll check this for you now and share next steps shortly."
        )
    else:
        return (
            "Thank you for the update. Glad to hear that. "
            "I’ll verify everything and confirm shortly."
        )

# ---------------- TOP LAYOUT ----------------
left_col, right_col = st.columns([2, 1], gap="medium")

# =====================================================
# LEFT COLUMN
# =====================================================
with left_col:

    # -------- Message Composer --------
    with st.container(border=True):
        st.markdown('<div class="section-title">Message Composition</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">Add customer or agent messages to simulate support interactions.</div>',
            unsafe_allow_html=True
        )

        sender = st.selectbox("Who is sending message?", ["Customer", "Agent"])
        msg = st.text_area("Enter message", height=130, placeholder="Type message...")

        has_customer = any(m["role"] == "Customer" for m in st.session_state.messages)
        disable_agent = sender == "Agent" and not has_customer

        b1, b2 = st.columns(2)

        with b1:
            send_clicked = st.button(
                "Send Message",
                use_container_width=True,
                disabled=disable_agent
            )

        with b2:
            clear_clicked = st.button(
                "Clear Chat",
                use_container_width=True
            )

        if disable_agent:
            st.info("Customer should send first message.")

    # -------- Button Actions --------
    if clear_clicked:
        st.session_state.messages = []
        st.session_state.last_score = None

    if send_clicked and msg.strip():
        st.session_state.messages.append({
            "role": sender,
            "text": msg.strip(),
            "time": datetime.now().strftime("%H:%M:%S")
        })

    # -------- Conversation --------
    with st.container(border=True):
        st.markdown('<div class="section-title">Conversation Log</div>', unsafe_allow_html=True)

        if not st.session_state.messages:
            st.info("Start by adding a customer message to begin the chat.")

        for item in st.session_state.messages:
            role = item["role"]
            text = item["text"]
            tm = item["time"]

            if role == "Customer":
                st.markdown(
                    f'<div class="chat-line chat-customer">🧑 Customer ({tm}): {text}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="chat-line chat-agent">🎧 Agent ({tm}): {text}</div>',
                    unsafe_allow_html=True
                )

    # -------- Suggested Better Reply --------
    last_customer = latest_customer_message()

    if last_customer:
        with st.container(border=True):
            st.markdown("### Suggested Improved Response")
            st.info(build_reply(last_customer))

# =====================================================
# RIGHT COLUMN
# =====================================================
with right_col:
    with st.container(border=True):
        st.markdown('<div class="section-title">Quality Insights</div>', unsafe_allow_html=True)

        total = len(st.session_state.messages)
        customer_count = count_role("Customer")
        agent_count = count_role("Agent")

        last_customer = latest_customer_message()

        if last_customer:
            sentiment_label, _ = sentiment(last_customer)
        else:
            sentiment_label = "N/A"

        score = st.session_state.last_score
        nudges = []

        if st.session_state.messages:
            last_msg = st.session_state.messages[-1]

            if last_msg["role"] == "Agent":
                score, nudges = analyze_agent_reply(last_msg["text"])
                st.session_state.last_score = score

        score_display = "N/A" if score is None else f"{score}/10"

        st.metric("Current Quality Score", score_display)

        if score is not None:
            st.progress(score / 10)

        c1, c2 = st.columns(2)
        c1.metric("Total Messages", total)
        c2.metric("Agent Messages", agent_count)

        c3, c4 = st.columns(2)
        c3.metric("Customer Messages", customer_count)
        c4.metric("Sentiment", sentiment_label)

        st.divider()

        if score is None:
            st.info("No agent response yet.")
        elif nudges:
            for n in nudges:
                st.warning(n)
        else:
            st.success("Excellent response!")

# ---------------- FOOTER ----------------
st.divider()

with st.expander("Prototype Snapshot"):
    st.write("- Real-time conversation simulation")
    st.write("- Rule-based response scoring")
    st.write("- Sentiment-aware nudges")
    st.write("- Streamlit dashboard UI")


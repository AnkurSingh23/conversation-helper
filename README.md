# Conversation Helper

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![TextBlob](https://img.shields.io/badge/TextBlob-Sentiment%20Analysis-2E86C1)](https://textblob.readthedocs.io/)
[![UI](https://img.shields.io/badge/UI-Interactive%20Prototype-1F2937)]()

A lightweight Streamlit application for simulating customer support conversations, evaluating agent replies, and generating real-time quality feedback.

## Overview

Conversation Helper is a rule-based conversation monitoring prototype designed to help teams review support interactions in a simple, visual way. Users can add customer and agent messages, inspect sentiment, and see coaching suggestions for improving the latest agent response.

## Key Features

- Real-time conversation simulation with customer and agent message roles
- Sentiment analysis for the latest customer message
- Rule-based agent reply scoring out of 10
- Coaching nudges for empathy, clarity, actionability, and tone
- Suggested improved agent response based on customer sentiment
- Clean two-column dashboard layout for quick review

## Tech Stack

- Python
- Streamlit
- TextBlob
- HTML/CSS for custom dashboard styling

## Tags

`python` `streamlit` `textblob` `sentiment-analysis` `customer-support` `conversation-analysis` `quality-monitoring` `dashboard` `prototype` `ui`

## How It Works

1. Add a customer message to start the conversation.
2. Add an agent reply after the customer message.
3. The app evaluates the latest agent response and calculates a quality score.
4. If the response needs improvement, the app shows specific nudges.
5. The app also suggests a cleaner response based on the customer sentiment.

## Installation

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

Start the Streamlit app with:

```bash
streamlit run app.py
```

## Project Structure

```text
.
├── app.py
├── requirements.txt
└── README.md
```

## What You Can Use It For

- Support agent coaching demos
- Conversation quality walkthroughs
- Sentiment-aware response prototyping
- Internal tooling prototypes for customer support operations

## Notes

This project is a prototype and uses lightweight, rule-based scoring. It is useful for demonstrations and internal experimentation, but it is not a production-grade QA or moderation system.
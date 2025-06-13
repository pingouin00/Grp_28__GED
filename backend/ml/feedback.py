from pymongo import MongoClient

client = MongoClient()
db = client.ged_ai

def save_feedback(question, answer, user_feedback):
    db.feedback.insert_one({
        "question": question,
        "answer": answer,
        "feedback": user_feedback
    })

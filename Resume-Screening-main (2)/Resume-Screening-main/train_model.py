import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Load dataset
print("📚 Loading dataset...")
df = pd.read_csv('DataSet/UpdatedResumeDataSet.csv')
print(f"✓ Loaded {df.shape[0]} resumes\n")

# Clean resume function
def cleanResume(txt):
    cleanText = re.sub(r'http\S+\s?', ' ', txt)
    cleanText = re.sub(r'RT|cc', ' ', cleanText)
    cleanText = re.sub(r'#\S+\s?', ' ', cleanText)
    cleanText = re.sub(r'@\S+', ' ', cleanText)
    cleanText = re.sub(r'[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
    cleanText = re.sub(r'\s+', ' ', cleanText)
    return cleanText.strip()

# Balance dataset
print("⚖️  Balancing dataset...")
max_size = df['Category'].value_counts().max()
balanced_df = df.groupby('Category').apply(lambda x: x.sample(max_size, replace=True)).reset_index(drop=True)
df = balanced_df.sample(frac=1).reset_index(drop=True)
print(f"✓ Balanced dataset with {df.shape[0]} total resumes\n")

# Clean resumes
print("🧹 Cleaning resumes...")
df['Resume'] = df['Resume'].apply(cleanResume)
print("✓ Resumes cleaned\n")

# Encode categories
print("🔢 Encoding categories...")
le = LabelEncoder()
le.fit(df['Category'])
df['Category'] = le.transform(df['Category'])
print(f"✓ {len(le.classes_)} categories encoded\n")

# Vectorize text
print("📊 Vectorizing text with TF-IDF...")
tfidf = TfidfVectorizer(stop_words='english')
tfidf.fit(df['Resume'])
X = tfidf.transform(df['Resume'])
print(f"✓ TF-IDF matrix shape: {X.shape}\n")

# Split data
print("✂️  Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, df['Category'], test_size=0.2, random_state=42)
X_train_dense = X_train.toarray()
X_test_dense = X_test.toarray()
print(f"✓ Training samples: {X_train.shape[0]}, Testing samples: {X_test.shape[0]}\n")

# Train model
print("🤖 Training SVC model (this may take a minute)...")
svc_model = OneVsRestClassifier(SVC())
svc_model.fit(X_train_dense, y_train)
y_pred = svc_model.predict(X_test_dense)
accuracy = accuracy_score(y_test, y_pred)
print(f"✓ Model trained! Accuracy: {accuracy:.4f}\n")

# Save models
print("💾 Saving models...")
pickle.dump(tfidf, open('WebSite/tfidf.pkl', 'wb'))
pickle.dump(svc_model, open('WebSite/clf.pkl', 'wb'))
pickle.dump(le, open('WebSite/encoder.pkl', 'wb'))
print("✓ Models saved to WebSite/\n")

print("=" * 50)
print("✅ Training complete! Ready to run web app.")
print("=" * 50)

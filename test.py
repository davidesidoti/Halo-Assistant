import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Load the JSON dataset
with open('./datasets/commands.json') as f:
    dataset = json.load(f)

# Extract the texts and intent labels from the dataset
texts = [d['text'] for d in dataset]
intent_labels = [d['intent'] for d in dataset]

# Preprocess an input sentence
input_sentence = input('Command: ')
# Tokenize the sentence
input_tokens = input_sentence.split()
# Convert the tokens to lowercase
input_tokens = [token.lower() for token in input_tokens]
# Remove stopwords (optional)
stopwords = set(ENGLISH_STOP_WORDS)
input_tokens = [token for token in input_tokens if token not in stopwords]
# Join the tokens back into a single string
input_text = ' '.join(input_tokens)

# Extract features from the input sentence
vectorizer = CountVectorizer()
X = vectorizer.fit_transform([input_text] + texts)

# Train a logistic regression classifier
clf = LogisticRegression()
clf.fit(X[1:], intent_labels)

# Make a prediction on the input sentence
predicted_intent = clf.predict(X[:1])[0]

print(predicted_intent)
# Output: 'time'

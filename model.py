from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import re
import pandas as pd
import spacy
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

def remove_punctuation(match):
  return match.group() if match.group() in ['C++', 'C#'] else ' '

def clean_text(text):
  text = re.sub(r'Ph\.D', 'phd', text)
  text = re.sub(r'C\+\+', 'cplusplus', text, flags=re.IGNORECASE)
  print(text)
  text = re.sub(r'\bC#\b', 'csharp', text, flags=re.IGNORECASE)
  text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
  text = text.lower()
  # text = nltk.word_tokenize(text)
  nlp = spacy.load("en_core_web_sm")
  doc = nlp(text)  
  text = ' '.join(token.text for token in doc if not token.is_stop)
  # text = [word for word in text if word not in stopwords.words('english')]
  # text = [str(item) for item in text]
  # text = " ".join(text)
  return text

def recommandation(df, user_input):
  data = list(df['Combined_Description'])
  data.append(user_input)
  vectorizer = TfidfVectorizer()
  tfidf_matrix = vectorizer.fit_transform(data)
  cosine_similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])
  recommendations = sorted(enumerate(cosine_similarities[0]), key=lambda x: x[1], reverse=True)
  dataset_indices, similarity_scores = zip(*recommendations)

  match_words = []

  for idx, doc in recommendations:
    doc_tfidf = tfidf_matrix[idx]
    matched_indices = doc_tfidf.indices
    feature_names = vectorizer.get_feature_names_out()
    matching_words = [feature_names[index] for index in matched_indices if feature_names[index] in user_input.lower().split()]
    print(matching_words)
    match_words.append(matching_words)

  result_df = df.iloc[list(dataset_indices)][['Title', 'Category', 'Responsibilities', 'Minimum Qualifications', 'Preferred Qualifications']]
  result_df['Score'] = similarity_scores
  result_df['Match Words'] = match_words
  result_df['No'] = list(range(0, len(dataset_indices)))
  result_df.set_index('No', inplace=True)

  return result_df

def raw_data(df, user_input):
  data = list(df['Combined_Description'])
  data.append(user_input)
  raw_df = pd.DataFrame(data, columns=['Raw Data'])

  return raw_df

def clean_data(df, user_input):
  data = list(df['Combined_Description'])
  data.append(user_input)
  clean_df = pd.DataFrame(data, columns=['Clean Data'])

  return clean_df

def tfidf_data(df, user_input):
  data = list(df['Combined_Description'])
  data.append(user_input)
  vectorizer = TfidfVectorizer()
  tfidf_matrix = vectorizer.fit_transform(data)
  df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

  return df_tfidf

def cosine_sim_data(df, user_input):
  data = list(df['Combined_Description'])
  data.append(user_input)
  vectorizer = TfidfVectorizer()
  tfidf_matrix = vectorizer.fit_transform(data)
  cosine_similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])
  df_cosine_sim = pd.DataFrame(cosine_similarities.reshape(-1), columns=["Cosine Similarity"])

  return df_cosine_sim

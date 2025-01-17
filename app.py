from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)


# TODO: Fetch dataset, initialize vectorizer and LSA here
newsgroups = fetch_20newsgroups(subset='all')
stop_words = list(stopwords.words('english'))  
vectorizer = TfidfVectorizer(stop_words=stop_words)
X = vectorizer.fit_transform(newsgroups.data)
svd = TruncatedSVD(n_components=100)
lsa = svd.fit_transform(X)
# the first version of the initalization did not work --> check the fit 
def search_engine(query):
    """
    Function to search for top 5 similar documents given a query
    Input: query (str)
    Output: documents (list), similarities (list), indices (list)
    """
    # TODO: Implement search engine here
    query_vec = vectorizer.transform([query])
    query_lsa = svd.transform(query_vec)
    similarities = cosine_similarity(query_lsa, lsa).flatten()
    #apply the cosine similarity to the query and the lsa 
    top_indices = similarities.argsort()[-5:][::-1]
    
    documents = [newsgroups.data[i] for i in top_indices]
    top_similarities = similarities[top_indices]
    
    return documents, top_similarities.tolist(), top_indices.tolist()
    # return documents, similarities, indices 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    documents, similarities, indices = search_engine(query)
    return jsonify({'documents': documents, 'similarities': similarities, 'indices': indices}) 

if __name__ == '__main__':
    app.run(debug=True,  port = 3000)

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sentence_transformers import SentenceTransformer
import warnings

warnings.filterwarnings("ignore")
nltk.download("stopwords")
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('vader_lexicon')

# 전처리
def preprocess_text(text):
    tokens = word_tokenize(text)  # Tokenization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]  # Lemmatization
    return lemmatized_tokens

# 채점/평가
# 1. 정확 일치
def exact_match(expected_answer, student_answer):
    return int(expected_answer == student_answer)

# 2. 부분 일치
def partial_match(expected_answer, student_answer):
    expected_tokens = preprocess_text(expected_answer)
    student_tokens = preprocess_text(student_answer)
    common_tokens = set(expected_tokens) & set(student_tokens)
    match_percentage = len(common_tokens) / max(len(expected_tokens), len(student_tokens))
    return match_percentage

# 3. 코사인 유사도 (TF-IDF)
def cosine_similarity_score(expected_answer, student_answer):
    vectorizer = TfidfVectorizer(tokenizer=preprocess_text)
    tfidf_matrix = vectorizer.fit_transform([expected_answer, student_answer])
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return cosine_sim

# 4. 감정 분석 점수
def sentiment_analysis(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)['compound']
    return (sentiment_score + 1) / 2  # [0, 1]로 정규화

# 5. Sentence-BERT 기반 문장 유사도
def enhanced_sentence_match(expected_answer, student_answer):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings_expected = model.encode([expected_answer])
    embeddings_student = model.encode([student_answer])
    similarity = cosine_similarity([embeddings_expected.flatten()], [embeddings_student.flatten()])[0][0]
    return similarity

# 6. Multinomial Naive Bayes 점수
def multinomial_naive_bayes_score(expected_answer, student_answer):
    answers = [expected_answer, student_answer]
    vectorizer = CountVectorizer(tokenizer=preprocess_text)
    X = vectorizer.fit_transform(answers)
    y = [0, 1]
    clf = MultinomialNB()
    clf.fit(X, y)
    probs = clf.predict_proba(X)
    return probs[1][1]  # student_answer가 정답일 확률

# 7. Sentence-BERT 기반 시맨틱 유사도
def semantic_similarity_score(expected_answer, student_answer):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings_expected = model.encode([expected_answer])
    embeddings_student = model.encode([student_answer])
    similarity = cosine_similarity([embeddings_expected.flatten()], [embeddings_student.flatten()])[0][0]
    return similarity

# 8. Coherence (길이 기반)
def coherence_score(expected_answer, student_answer):
    len_expected = len(word_tokenize(expected_answer))
    len_student = len(word_tokenize(student_answer))
    coherence_score = min(len_expected, len_student) / max(len_expected, len_student)
    return coherence_score

# 9. Relevance (공통 단어 비율)
def relevance_score(expected_answer, student_answer):
    expected_tokens = set(word_tokenize(expected_answer.lower()))
    student_tokens = set(word_tokenize(student_answer.lower()))
    common_tokens = expected_tokens.intersection(student_tokens)
    relevance_score = len(common_tokens) / len(expected_tokens)
    return relevance_score

# 최종 점수 계산
def weighted_average_score(scores, weights):
    weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
    total_weight = sum(weights)
    return weighted_sum / total_weight

def evaluate(expected, response):
    if expected == response:
        return 10
    elif not response:
        return 0

    # 각 평가 지표별 점수 계산
    exact_match_score = exact_match(expected, response)
    partial_match_score = partial_match(expected, response)
    cosine_similarity_score_value = cosine_similarity_score(expected, response)
    sentiment_score = sentiment_analysis(response)
    enhanced_sentence_match_score = enhanced_sentence_match(expected, response)
    multinomial_naive_bayes_score_value = multinomial_naive_bayes_score(expected, response)
    semantic_similarity_value = semantic_similarity_score(expected, response)
    coherence_value = coherence_score(expected, response)
    relevance_value = relevance_score(expected, response)

    # 가중치 설정
    scores = [
        exact_match_score, partial_match_score, cosine_similarity_score_value,
        sentiment_score, enhanced_sentence_match_score, multinomial_naive_bayes_score_value,
        semantic_similarity_value, coherence_value, relevance_value
    ]
    weights = [0.15, 0.1, 0.1, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1]

    # 점수를 0~10 스케일로 변환
    scaled_scores = [score * 10 for score in scores]

    # 가중 평균 계산
    final_score = weighted_average_score(scaled_scores, weights)
    rounded_score = round(final_score)
    return rounded_score


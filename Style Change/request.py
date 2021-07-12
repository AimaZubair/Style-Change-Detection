from flask import Flask,render_template,request,redirect
import pickle
from chunkers import get_sentences
import numpy as np
from models import MLP

app = Flask(__name__)
estimator = MLP
#model = pickle.load(open('model.pkl','rb'))
@app.route('/')
def home():
     return render_template('Home.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    if estimator:
        clf = estimator()
    if request.method == 'POST':
        input_file = request.files['file']
        text = input_file.filename
        f = open(text,'r')
        text_2 = f.read()
        f.close()
        if not input_file:
                return render_template('Home.html')
        else:
            #test_x = tokenizer.texts_to_matrix(input_file, mode='tfidf')
            #prediction = clf.predict(text_2)[0]
            prediction = get_breach_predictions(clf,text_2)
            return render_template('result.html', prediction_text = prediction)
    else:
        return render_template('Home.html')

def get_breach_predictions(clf, test_x):
    predictions = []
    sentences = get_sentences(test_x)
    breaches = find_breaches(clf, sentences, 0, len(sentences))
    predictions.append(breaches)
    return predictions

def find_breaches(clf, sentences, l, r):
    x = np.expand_dims(' '.join(sentences[l:r]), axis=0)
    has_change = clf.predict(x)[0]

    if not has_change:
        return []

    if r - l <= 10:
        return [len(' '.join(sentences[:(l+r)//2]))]
    else:
        mid = (r-l) // 2
        left = find_breaches(clf, sentences, l, l+mid)
        right = find_breaches(clf, sentences, l+mid, r)
        if len(left) == 0 and len(right) == 0:
            return [len(' '.join(sentences[:l+mid]))]

        return left + right

if __name__ == '__main__':
    app.run(port=3000,debug=True)
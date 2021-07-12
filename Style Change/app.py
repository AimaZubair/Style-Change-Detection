
import time
from flask import Flask,render_template,request,redirect
from sklearn.model_selection import cross_validate, GridSearchCV
from sklearn.metrics import accuracy_score
from utils import get_data, get_results, write_results_to_file, get_external_data
from utils import persist_output, get_n_jobs, get_arguments, print_splits, config_local
from models import MLP
#from models.light_gbm_model import LightGbmWithLogReg
from nltk import ConfusionMatrix
from sklearn.model_selection import StratifiedKFold
import numpy as np
from metrics.breach_evaluator import evaluate, computeMeasures
from sklearn.metrics import confusion_matrix
from chunkers import get_sentences
import pickle
import keras
import PyPDF2 
import docx2txt
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.preprocessing.text import Tokenizer

from models.base_estimator import BaseEstimator

TRAINING_DIR = 'data/training'
TRAINING_EXTERNAL_FILE = 'data/feather/external_stackexchange_feather'
VALIDATION_DIR = 'data/validation'

BREACH_DIR = 'data/breach'

input_dir, output_dir= get_arguments()
TEST_DIR = input_dir or 'data/test'
OUTPUT_DIR = output_dir or 'data/output'


app = Flask(__name__)
cv_split=5
estimator= MLP
with_cross_validation=True
with_validation=True
with_test=False
with_external_data=False
validate_on_external=False
with_grid_search=False
with_full_data_tfidf=False
train_with_validation=True
predict_breaches=False
train_on_breach=False
cutoff=None

if train_on_breach:
        train_x, train_y, train_positions, train_file_names = get_data(
            main_dir=BREACH_DIR,
            external_file=None,
            breach=True
        )
else:
        train_x, train_y, train_positions, train_file_names = get_data(
            main_dir=TRAINING_DIR,
            external_file=TRAINING_EXTERNAL_FILE if with_external_data else None
        )
        if train_with_validation:
            validation_x, validation_y, validation_positions, validation_file_names = get_data(
                main_dir=VALIDATION_DIR
            )
            train_x.extend(validation_x)
            train_y.extend(validation_y)

        if cutoff:
            train_x = train_x[:cutoff]
            train_y = train_y[:cutoff]
            train_positions = train_positions[:cutoff]
if estimator:
    clf=estimator()

if with_validation:
        if not validate_on_external:
            validation_x, validation_y, validation_positions, validation_file_names = get_data(
                main_dir=VALIDATION_DIR
            )
        
        if cutoff:
            validation_x = validation_x[:cutoff]
            validation_y = validation_y[:cutoff]

        t_start = time.time()
        if with_full_data_tfidf:
            clf.fit_with_test(train_x, train_y, train_positions, validation_x)
        else:
            clf.fit(train_x, train_y, train_positions)

        if predict_breaches:
            predictions = get_breach_predictions(clf, validation_x, validation_y)
        else:
            predictions = clf.predict(validation_x)
        t_end = time.time()
        print(ConfusionMatrix(validation_y, predictions))

        val = {
            'accuracy': accuracy_score(validation_y, predictions),
            'time': t_end - t_start
        }
        print(val)
#model = pickle.load(open('model.pkl','rb'))
#clf = estimator()
@app.route('/')
def home():
     return render_template('Home.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    change_predictions = [True]
    if request.method == 'POST':
        text_2 = ''
        input_file = request.files['file']
        text = input_file.filename
        doc = open(text,'r')
        if not input_file:
                return render_template('Home.html')
        else:
            if text.endswith('.txt'):
                text_2 = doc.read()
                prediction = get_breach_predictions(clf,text_2,change_predictions)
            elif text.endswith('.pdf'):
                pdfReader = PyPDF2.PdfFileReader(doc)
                pageObj = pdfReader.getPage(0)
                file_text = pageObj.extractText() 
                prediction = get_breach_predictions(clf,file_text,change_predictions)
                text_2= file_text
            else:
                docText = docx2txt.process(text)
                prediction = get_breach_predictions(clf,docText,change_predictions)
                text_2 = docText

            if(prediction == [[]]):
                text = 'The Given File is Single author'
            else:
                text = 'The Given File is Multi-Author. The positions where Authors changes are '+str(prediction)+' .'

            return render_template('result.html', prediction_text = text, file_text = text_2)
            f.close()
    else:
        return render_template('Home.html')
    
def get_breach_predictions(clf,test_x, change_predictions):
    predictions = []
    sentences = get_sentences(test_x)
    breaches = find_breaches(clf, sentences, 0, len(sentences))
    #print('BREACHES: ', breaches)
    predictions.append(breaches)
    
    return predictions

def find_breaches(clf,sentences, l, r):
    x = np.expand_dims(' '.join(sentences[l:r]), axis=0)
    has_change = clf.predict(x)
     
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

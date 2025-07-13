import json
import string
import random
import nltk
import numpy as num
from nltk.stem import WordNetLemmatizer # It has the ability to lemmatize.
import tensorflow as tensorF # A multidimensional array of elements is represented by this symbol.
from tensorflow.keras import Sequential # Sequential groups a linear stack of layers into a tf.keras.Model
from tensorflow.keras.layers import Dense, Dropout

# nltk.download("punkt")# required package for tokenization
# nltk.download("wordnet")# word database
# nltk.download('omw-1.4')
from tensorflow.python.keras.models import load_model

data_file = open(r'C:\Users\hilus\PycharmProjects\eon\eonapp\static\chatbot\Data.json').read()
data = json.loads(data_file)


lm = WordNetLemmatizer() #reducing words to their base or dictionary form

ourClasses = []
newWords = []
documentX = []
documentY = []
# Each intent is tokenized into words and the patterns and their associated tags are added to their respective lists.
for intent in data["ourIntents"]:
    for pattern in intent["patterns"]:
        ournewTkns = nltk.word_tokenize(pattern)
        newWords.extend(ournewTkns)
        documentX.append(pattern)
        documentY.append(intent['tag'])
    if intent["tag"] not in ourClasses:
        ourClasses.append(intent["tag"])

newWords = [lm.lemmatize(word.lower()) for word in newWords if word not in string.punctuation]
newWords = sorted(set(newWords))
ourClasses = sorted(set(ourClasses))

trainingData  = []
outEmpty = [0] * len(ourClasses)

for idx, doc in enumerate(documentX):
    bag0words = []
    text = lm.lemmatize(doc.lower())
    for word in newWords :
        bag0words.append(1) if word in text else bag0words.append(0)

    outputRow = list(outEmpty)
    outputRow[ourClasses.index(documentY[idx])] = 1
    trainingData.append([bag0words, outputRow])

random.shuffle(trainingData)
trainingData = num.array(trainingData, dtype=object)

x = num.array(list(trainingData[:,0]))
y = num.array(list(trainingData[:,1]))

iShape = (len(x[0]),)
oShape = len(y[0])


# ####           training model
#
# Model = Sequential()
# Model.add(Dense(128, activation="relu" , input_shape=iShape))
# Model.add(Dropout(0.5)) #Dropout is a regularization technique that randomly drops out (sets to zero) some of the inputs to a layer during training to prevent overfitting.
# Model.add(Dense(64, activation="relu"))
# Model.add(Dropout(0.3))
# Model.add(Dense(oShape, activation='softmax'))
# md = tensorF.keras.optimizers.Adam(learning_rate= 0.01)
# Model.compile(optimizer=md, loss='categorical_crossentropy', metrics=['accuracy'])
# print(Model.summary())
# Model.fit(x,y, epochs=200, verbose=1)
# Model.save(r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\model.h5")
#
# ###           training end



#####           open trained model
Model=load_model(r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\model.h5")
#####           open code end



def ourText(text):
  newtkns = nltk.word_tokenize(text)
  newtkns = [lm.lemmatize(word) for word in newtkns]
  return newtkns

def wordBag(text, vocab):
  newtkns = ourText(text)
  bagOwords = [0] * len(vocab)
  for w in newtkns:
    for idx, word in enumerate(vocab):
      if word == w:
        bagOwords[idx] = 1
  return num.array(bagOwords)

def Pclass(text, vocab, labels):
  bagOwords = wordBag(text, vocab)
  ourResult = Model.predict(num.array([bagOwords]))[0]
  newThresh = 0.2
  yp = [[idx, res] for idx, res in enumerate(ourResult) if res > newThresh]

  yp.sort(key=lambda x: x[1], reverse=True)
  newList = []
  for r in yp:
    newList.append(labels[r[0]])
  return newList

def getRes(firstlist, fJson):
  tag = firstlist[0]
  listOfIntents = fJson["ourIntents"]
  ourResult=""
  for i in listOfIntents:
    if i["tag"] == tag:
      ourResult = random.choice(i["responses"])
      break
  return ourResult


def get_Response(newMessage):
    intents = Pclass(newMessage, newWords, ourClasses)
    ourResult = getRes(intents, data)
    return ourResult


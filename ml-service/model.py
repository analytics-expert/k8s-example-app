from random import randint
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

def load_data():
    X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=None)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    return X_train, X_test, y_train, y_test

def train_model():
    hidden_layer_sizes = randint(50, 150)

    X_train, X_test, y_train, y_test = load_data()
    
    clf = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, max_iter=500)
    clf = clf.fit(X_train, y_train)
    model_score = clf.score(X_test, y_test)

    return hidden_layer_sizes, model_score
# id, datetime, hidden_layer_sizes and score

if __name__ == '__main__':
    print(train_model())

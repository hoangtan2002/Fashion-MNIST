# K Nearest Neighbors

import sys
import time
import numpy as np
import pickle
from sklearn import model_selection
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from Fashion_MNIST_Loader.mnist_loader import MNIST
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

label_description = {
    0 : "T-Shirt",
	1 : "Trouser",
	2 : "Pullover",
	3 : "Dress",
	4 : "Coat",
    5 : "Sandal",
    6 : "Shirt",
    7 : "Sneaker",
    8 : "Bag",
    9 : "Ankle boot",
}

old_stdout = sys.stdout
log_file = open("KNN_summary.log","w")
sys.stdout = log_file

tic = time.time()

print('\nLoading MNIST Data...')
data = MNIST('./Fashion_MNIST_Loader/dataset/')

print('\nLoading Training Data...')
img_train, labels_train = data.load_training()
train_img = np.array(img_train)
train_labels = np.array(labels_train)
print('\nLoading Testing Data...')
img_test, labels_test = data.load_testing()
test_img = np.array(img_test)
test_labels = np.array(labels_test)

X = train_img
y = train_labels
X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y,test_size=0.1)
clf = KNeighborsClassifier(n_neighbors=5,algorithm='ball_tree',n_jobs=10,weights='distance')
clf.fit(X_train,y_train)

with open('MNIST_KNN.pickle','wb') as f:
	pickle.dump(clf, f)

# pickle_in = open('MNIST_KNN.pickle','rb')
# clf = pickle.load(pickle_in)

print('\nCalculating Accuracy of trained Classifier...')
confidence = clf.score(X_test,y_test)

print('\nMaking Predictions on Validation Data...')
y_pred = clf.predict(X_test)

print('\nCalculating Accuracy of Predictions...')
accuracy = accuracy_score(y_test, y_pred)

print('\nCreating Confusion Matrix...')
conf_mat = confusion_matrix(y_test,y_pred)

print('\nKNN Trained Classifier Confidence: ',confidence)
print('\nPredicted Values: ',y_pred)
print('\nAccuracy of Classifier on Validation Image Data: ',accuracy)
print('\nConfusion Matrix: \n',conf_mat)


#Plot Confusion Matrix Data as a Matrix
plt.matshow(conf_mat)
plt.title('Confusion Matrix for Validation Data')
plt.colorbar()
plt.ylabel('True label')
plt.xlabel('Predicted label')
# plt.show()


print('\nMaking Predictions on Test Input Images...')
test_labels_pred = clf.predict(test_img)

print('\nCalculating Accuracy of Trained Classifier on Test Data... ')
acc = accuracy_score(test_labels,test_labels_pred)

print('\n Creating Confusion Matrix for Test Data...')
conf_mat_test = confusion_matrix(test_labels,test_labels_pred)

print('\nPredicted Labels for Test Images: ',test_labels_pred)
print('\nAccuracy of Classifier on Test Images: ',acc)
print('\nConfusion Matrix for Test Data: \n',conf_mat_test)

toc = time.time()

print('Total Time Taken: {0} ms'.format((toc - tic)*1000))

# Plot Confusion Matrix for Test Data
plt.matshow(conf_mat_test)
plt.title('Confusion Matrix for Test Data',fontsize=8)
plt.colorbar()
plt.ylabel('True label')
plt.xlabel('Predicted label')
# plt.show()
plt.savefig("confusion_matrix.png")

sys.stdout = old_stdout
log_file.close()

# Show the Test Images with Original and Predicted Labels
a = np.random.randint(1,50,20)
for i in a:
	two_d = (np.reshape(test_img[i], (28, 28)) * 255).astype(np.uint8)
	plt.title('Original Label:{0}, Predicted Label: {1}'.format(label_description[test_labels[i]],label_description[test_labels_pred[i]]),fontsize=8)
	plt.imshow(two_d, interpolation='nearest')
	plt.savefig('{0}.Original Label:{1}-Predicted Label:{2}.png'.format(i,label_description[test_labels[i]],label_description[test_labels_pred[i]]),dpi=300)

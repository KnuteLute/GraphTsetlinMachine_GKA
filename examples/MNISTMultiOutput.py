from PySparseCoalescedTsetlinMachineCUDA.tm import MultiOutputConvolutionalTsetlinMachine2D

import numpy as np
from time import time

from keras.datasets import mnist

factor = 1.25

s = 10.0

T = int(factor*25*100)

ensembles = 10
epochs = 250

patch_size = 10

(X_train, Y_train_org), (X_test, Y_test_org) = mnist.load_data()

X_train = np.where(X_train.reshape((X_train.shape[0], 28*28)) > 75, 1, 0) 
X_test = np.where(X_test.reshape((X_test.shape[0], 28*28)) > 75, 1, 0) 

random_grouping1 = np.random.choice(10, size=5, replace=False)
random_grouping2 = np.random.choice(10, size=5, replace=False)

Y_train = np.empty((Y_train_org.shape[0], 2), dtype=np.uint32)
Y_train[:, 0] = np.where(np.isin(Y_train_org, random_grouping1), 1, 0)
Y_train[:, 1] = np.where(np.isin(Y_train_org, random_grouping2), 1, 0)

Y_test = np.empty((Y_test_org.shape[0], 2), dtype=np.uint32)
Y_test[:, 0] = np.where(np.isin(Y_test_org, random_grouping1), 1, 0)
Y_test[:, 1] = np.where(np.isin(Y_test_org, random_grouping2), 1, 0)

f = open("mnist_%.1f_%d_%d_%d.txt" % (s, int(factor*2000), T,  patch_size), "w+")

for e in range(ensembles):
	tm = MultiOutputConvolutionalTsetlinMachine2D(int(factor*2000), T, s, (28, 28, 1), (patch_size, patch_size))

	for i in range(epochs):
	    start_training = time()
	    tm.fit(X_train, Y_train, epochs=1, incremental=True)
	    stop_training = time()

	    start_testing = time()
	    print(Y_test.shape, tm.predict(X_test).shape)
	    result_test = 100*(tm.predict(X_test)[:,0] == Y_test[:,0]).mean()
	    stop_testing = time()

	    result_train = 100*(tm.predict(X_train[:,0]) == Y_train[:,0]).mean()

	    print("%d %d %.2f %.2f %.2f %.2f" % (e, i, result_train, result_test, stop_training-start_training, stop_testing-start_testing))
	    print("%d %d %.2f %.2f %.2f %.2f" % (e, i, result_train, result_test, stop_training-start_training, stop_testing-start_testing), file=f)
	    f.flush()
f.close()
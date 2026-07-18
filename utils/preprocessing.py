import numpy as np

def create_dataset(data, time_step):
    X = []
    for i in range(time_step, len(data)):
        X.append(data[i-time_step:i, 0])
    
    X = np.array(X)
    X = X.reshape(X.shape[0], X.shape[1], 1)
    return X
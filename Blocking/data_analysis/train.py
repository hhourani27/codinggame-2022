import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz
from sklearn.metrics import jaccard_score, accuracy_score, classification_report, zero_one_loss


import matplotlib.pyplot as plt
import matplotlib.cm as cm


data = np.genfromtxt('data.csv', delimiter=',', dtype=int)

# Only train on middle game
data = data[data[:,1] >15]

# Remove the first 2 columns : game# & turn#
X = data[:,2:2+13*13]
Y = data[:,2+13*13:]

# Split train & test set
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=42)

#%%
# Train classifier
clf = RandomForestClassifier(n_estimators=10, random_state=0, verbose=True, max_depth=25)
clf.fit(X_train, y_train)

#%%
# calculate score
y_pred = clf.predict(X_test)
zero_one_loss(y_test,y_pred)

#%%

# Return an image (x,y,color dimension) where each value in the matrix is mapped to a color
def generate_colored_board(board_2d):
    color_map = {-1: np.array([0, 0, 0]), 
                 0: np.array([255, 255, 255]),
                 1: np.array([0, 0, 255]),
                 2: np.array([0, 255, 255])} 
    board_2d_color = np.ndarray(shape=(board_2d.shape[0], board_2d.shape[1], 3), dtype=int)
    for i in range(0, board_2d.shape[0]):
        for j in range(0, board_2d.shape[1]):
            board_2d_color[i][j] = color_map[board_2d[i][j]]
            
    return board_2d_color

N = 3
# choose 3 random x,y from the test set
idx = np.random.randint(X_test.shape[0], size=N)
x = X_test[idx]
y = y_test[idx]

# predict for each x the cells that should be occupied
preds = clf.predict_proba(x)
# fix the (0,0) and (13,13), as they don't have any prediction
preds[0] = np.array([[1.,1.] for i in range(N)])
preds[-1] = np.array([[1.,1.] for i in range(N)])
# Reshape preds in order to have one row per prediction
preds = np.array(preds)
preds = preds[:,:,1]
preds = np.transpose(preds)

# Each row is a test case
# 3 columns : start board, prediction, next board
fig, ax = plt.subplots(N,3)
color_map = cm.Greens.copy()
color_map.set_under(color='black')
color_map.set_over(color='blue')

for i in range(N):
    # Plot start board
    xi_2d = x[i].reshape(13,13)
    im = ax[i,0].imshow(generate_colored_board(xi_2d))
    
    # Plot prediction 
    predsi = preds[i].reshape(13,13)
    predsi[np.isin(xi_2d,[1])] = 2
    predsi[np.isin(xi_2d,[-1])] = -1
    im = ax[i,1].imshow(predsi,cmap=color_map)
    im.set_clim(vmin=0.0,vmax=1.0)
    
    for r in range(predsi.shape[0]):
        for c in range(0, predsi.shape[1]):
            p = predsi[c,r]
            if 0 < p <= 1.0:
                ax[i,1].text(r, c, '{:.2f}'.format(p), va='center', ha='center', size='2.0')


    # Plot next board
    yi_2d = y[i].reshape(13,13)
    yi_board_2d = xi_2d.copy()
    yi_board_2d[yi_2d == 1] = 2

    im = ax[i,2].imshow(generate_colored_board(yi_board_2d))

    [axi.axis('off') for axi in ax[i]]
    
#plt.show()
plt.savefig('viz.png', dpi=1000, bbox_inches='tight')

#%%

[clf.estimators_[i].tree_.max_depth for i in range(len(clf.estimators_))]
export_graphviz(clf.estimators_[0])

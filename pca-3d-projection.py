# PCA algorithm implementation for 3 dimensions to 2 dimensions
# based on https://plot.ly/ipython-notebooks/principal-component-analysis/
# and https://habr.com/post/304214/

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA

num = 15

x = np.arange(1, num+1)
y = 2 * x + np.random.randn(num)*2
z = x + 2*y + np.random.randn(num)*0.5

dataset = np.vstack((x, y, z))

fig = plt.figure(1, figsize=(6, 5))
ax = Axes3D(fig, elev=48, azim=134)
ax.scatter(x, y, z, c='red')
plt.show()

dataset_cntr = (dataset[0] - x.mean(), dataset[1] - y.mean(), dataset[2] - z.mean())

cov_mat = np.cov(dataset_cntr)
vals, vects = np.linalg.eig(cov_mat)

eig_pairs = [(np.abs(vals[i]), vects[:, i]) for i in range(len(vals))]
eig_pairs.sort()
eig_pairs.reverse()

matrix_w = np.vstack((eig_pairs[0][1],
                      eig_pairs[1][1]))

coord2 = np.dot(matrix_w, dataset_cntr)

plt.figure()
plt.scatter(coord2[0, :], coord2[1, :], c='green')
plt.show()

# comparing to pca from sklearn:
pca = PCA(n_components=2)
PCAreduced = pca.fit_transform(np.transpose(dataset))

print('Our projection: \n', coord2)
print('Sklearn PCA projection: \n', PCAreduced)

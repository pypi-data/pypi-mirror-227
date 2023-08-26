import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
data = pd.read_csv("C:\\Users\\zhangle\\Desktop\\2023年第四届“华数杯”全国大学生数学建模竞赛赛题\\2023年C题\\cleaned .csv",encoding="gbk")
col=["整晚睡眠时间（时：分：秒）","睡醒次数","入睡方式"]
X = np.array(data[col])
kmeans = KMeans(n_clusters=4)
kmeans.fit(X)

labels = kmeans.labels_
centers = kmeans.cluster_centers_

fig = plt.figure(dpi=128,figsize=(8,8))
ax = fig.add_subplot(111, projection='3d')
# 可视化聚类结果
ax.scatter(X[:, 0], X[:, 1],X[:,2], c=labels, cmap='viridis')
ax.scatter(centers[:, 0], centers[:, 1], centers[:,2],c='red', marker='X', s=200)
plt.title('K-Means Clustering')
ax.set_xlabel('睡眠时间', fontsize=10)
ax.set_ylabel('睡醒次数', fontsize=10)
ax.set_zlabel('哄睡方式', fontsize=10)
plt.legend()
# plt.xlabel('睡眠时间')
# plt.ylabel('睡醒次数')
plt.show()

from sklearn.ensemble import RandomForestClassifier
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler

from sklearn.preprocessing import label_binarize


data = pd.read_csv("C:\\Users\\zhangle\\Desktop\\2023年第四届“华数杯”全国大学生数学建模竞赛赛题\\2023年C题\\SMOTE(6)_睡眠质量第四题.csv", encoding='gbk')
X = data.drop('睡眠质量', axis=1)
y = data['睡眠质量']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

n_classes =4

classifier = RandomForestClassifier(n_estimators=200, criterion='entropy', random_state=0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

y_score = classifier.fit(X_train, y_train).predict_proba(X_test)  # 获得预测概率
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
result = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(result)
result1 = classification_report(y_test, y_pred)
print("Classification Report:", )
print(result1)
result2 = accuracy_score(y_test, y_pred)
print("Accuracy:", result2)

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc

# Binarize the labels
y_test_bin = label_binarize(y_test, classes=[1, 2, 3,4])  # Adjust classes here

# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()

for i in range(1, n_classes + 1):  # Adjust loop range
    fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i - 1], y_score[:, i - 1])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Compute macro-average ROC curve and ROC area
all_fpr = np.unique(np.concatenate([fpr[i] for i in range(1, n_classes + 1)]))
mean_tpr = np.zeros_like(all_fpr)
for i in range(1, n_classes + 1):  # Adjust loop range
    mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])
mean_tpr /= n_classes
fpr["macro"] = all_fpr
tpr["macro"] = mean_tpr
roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

# Compute micro-average ROC curve and ROC area
micro_fpr, micro_tpr, _ = roc_curve(y_test_bin.ravel(), y_score.ravel())
roc_auc["micro"] = auc(micro_fpr, micro_tpr)

# Plot ROC curves for each class, macro-average, and micro-average
plt.figure()
lw = 2
colors = ['green', 'pink', 'purple','red']  # Add more colors if needed
for i in range(1, n_classes + 1):  # Adjust loop range
    plt.plot(fpr[i], tpr[i], lw=lw, color=colors[i-1], label='ROC curve of class %d (area = %0.3f)' % (i, roc_auc[i]))

plt.plot(fpr["macro"], tpr["macro"], color='blue', linestyle=':', linewidth=4, label='Macro-average ROC curve (area = %0.3f)' % roc_auc["macro"])
plt.plot(micro_fpr, micro_tpr, color='pink', linestyle=':', linewidth=4, label='Micro-average ROC curve (area = %0.3f)' % roc_auc["micro"])

# Plot random chance line
plt.plot([0, 1], [0, 1], color='grey', lw=lw, linestyle='--')

# Configure plot
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves')
plt.legend(loc="lower right")
plt.show()








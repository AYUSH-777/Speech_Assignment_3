# -*- coding: utf-8 -*-
"""M22AIE251_PA_Sppech_3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ckf6APUtd6FNDDIMnOZNISsY_Yh8A5ID
"""

from transformers import Wav2Vec2ForCTC, Wav2Vec2Config

# Initialize the model with a pre-defined configuration
config = Wav2Vec2Config.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC(config)

from google.colab import drive
drive.mount('/content/drive')

import torch

model_path = '/content/drive/My Drive/LA_model.pth'
state_dict = torch.load(model_path, map_location=torch.device('cpu'))
model.load_state_dict(state_dict)
model.eval()  

import torch
import torch.nn as nn


class YourModelClass(nn.Module):
    def __init__(self):
        super(YourModelClass, self).__init__()

    def forward(self, x):
        return x

model = YourModelClass()

state_dict_path = '/content/drive/My Drive/LA_model.pth'

state_dict = torch.load(state_dict_path, map_location=torch.device('cpu'))

model.load_state_dict(state_dict, strict=False)


model.eval()

import librosa
import numpy as np
import os

def load_and_preprocess_audio(file_path):
    try:
        audio, sr = librosa.load(file_path, sr=None)
        if audio.size == 0:
            print(f"Warning: {file_path} is empty and will be skipped.")
            return None
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        mfccs = mfccs.T
        return mfccs
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

real_dir = '/content/drive/My Drive/Dataset_Speech_Assignment/Real'
fake_dir = '/content/drive/My Drive/Dataset_Speech_Assignment/Fake'
real_features = []
fake_features = []

for filename in os.listdir(real_dir):
    if filename.endswith('.mp3') or filename.endswith('.wav'):
        file_path = os.path.join(real_dir, filename)
        mfccs = load_and_preprocess_audio(file_path)
        if mfccs is not None:
            real_features.append(mfccs)
        else:
            print(f"Skipped None from real: {filename}")
for filename in os.listdir(fake_dir):
    if filename.endswith('.mp3') or filename.endswith('.wav'):
        file_path = os.path.join(fake_dir, filename)
        mfccs = load_and_preprocess_audio(file_path)
        if mfccs is not None:
            fake_features.append(mfccs)
        else:
            print(f"Skipped None from fake: {filename}")

X = real_features + fake_features
print(f"Total features collected: {len(X)}")
X = [x for x in X if x is not None]
print(f"Total features after filtering: {len(X)}")

from sklearn.metrics import roc_curve, auc

def calculate_eer(y_true, y_scores):
    fpr, tpr, thresholds = roc_curve(y_true, y_scores, pos_label=1)
    eer = fpr[np.nanargmin(np.abs(fpr - (1 - tpr)))]
    return eer

def calculate_auc(y_true, y_scores):
    return auc(fpr, tpr)

import numpy as np
from sklearn.model_selection import train_test_split

max_length = max(len(mfcc) for mfcc in X)

if X:
    max_length = max(len(mfcc) for mfcc in X)

    def pad_mfcc(mfcc, max_length):
        padding = max_length - len(mfcc)
        if padding > 0:
            return np.pad(mfcc, ((0, padding), (0, 0)), mode='constant', constant_values=(0, 0))
        return mfcc

    X_padded = np.array([pad_mfcc(mfcc, max_length) for mfcc in X])
else:
    print("No valid data to process")




X = real_features + fake_features

max_length = max(len(mfcc) for mfcc in X)

X_padded = np.array([pad_mfcc(mfcc, max_length) for mfcc in X])

y = [1] * len(real_features) + [0] * len(fake_features)  # 1 for Real, 0 for Fake

X_train, X_test, y_train, y_test = train_test_split(X_padded, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve


X_flattened = np.array([x.flatten() for x in X_padded])

X_train, X_test, y_train, y_test = train_test_split(X_flattened, y, test_size=0.2, random_state=42)


model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

y_pred_probs = model.predict_proba(X_test)[:, 1]  # Get the probabilities for the positive class

from sklearn.metrics import roc_auc_score
from scipy.optimize import brentq
from scipy.interpolate import interp1d
from sklearn.metrics import roc_curve

auc = roc_auc_score(y_test, y_pred_probs)
print(f'AUC: {auc}')

fpr, tpr, thresholds = roc_curve(y_test, y_pred_probs)
eer = brentq(lambda x: 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
print(f'EER: {eer}')

import matplotlib.pyplot as plt

plt.figure()
plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()

import torch
import torch.nn as nn
import numpy as np
from sklearn.model_selection import train_test_split
import librosa
import os

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1 = nn.Linear(64 * 64 * 32, 128)
        self.fc2 = nn.Linear(128, 2)  # Output has 2 classes

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 64 * 64 * 32)  # Flatten before fully connected layer
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

new_model = SimpleCNN()

def load_and_preprocess_audio(file_path):
    try:
        audio, sr = librosa.load(file_path, sr=None)
        if audio.size == 0:  # Check if the audio is empty
            print(f"Warning: {file_path} is empty and will be skipped.")
            return None
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        mfccs = mfccs.T
        return mfccs
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

real_dir = '/content/drive/My Drive/for_2_sec/data/real'
fake_dir = '/content/drive/My Drive/for_2_sec/data/fake'
real_features = []
fake_features = []

for filename in os.listdir(real_dir):
    if filename.endswith('.mp3') or filename.endswith('.wav'):
        file_path = os.path.join(real_dir, filename)
        mfccs = load_and_preprocess_audio(file_path)
        if mfccs is not None:
            real_features.append(mfccs)
        else:
            print(f"Skipped None from real: {filename}")  # Debug message

for filename in os.listdir(fake_dir):
    if filename.endswith('.mp3') or filename.endswith('.wav'):
        file_path = os.path.join(fake_dir, filename)
        mfccs = load_and_preprocess_audio(file_path)
        if mfccs is not None:
            fake_features.append(mfccs)
        else:
            print(f"Skipped None from fake: {filename}")  # Debug message

X = real_features + fake_features
X = [x for x in X if x is not None]  # Filter out None values

y = [1] * len(real_features) + [0] * len(fake_features)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

import numpy as np
from sklearn.model_selection import train_test_split

max_length = max(len(mfcc) for mfcc in X)

if X:  # Check if X is not empty
    max_length = max(len(mfcc) for mfcc in X)

    def pad_mfcc(mfcc, max_length):
        padding = max_length - len(mfcc)
        if padding > 0:
            return np.pad(mfcc, ((0, padding), (0, 0)), mode='constant', constant_values=(0, 0))
        return mfcc

    X_padded = np.array([pad_mfcc(mfcc, max_length) for mfcc in X])
else:
    print("No valid data to process")




X = real_features + fake_features

max_length = max(len(mfcc) for mfcc in X)

X_padded = np.array([pad_mfcc(mfcc, max_length) for mfcc in X])

y = [1] * len(real_features) + [0] * len(fake_features)  # 1 for Real, 0 for Fake

X_train, X_test, y_train, y_test = train_test_split(X_padded, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve

X_flattened = np.array([x.flatten() for x in X_padded])

X_train, X_test, y_train, y_test = train_test_split(X_flattened, y, test_size=0.2, random_state=42)


model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

y_pred_probs = model.predict_proba(X_test)[:, 1]  # Get the probabilities for the positive class

from sklearn.metrics import roc_auc_score
from scipy.optimize import brentq
from scipy.interpolate import interp1d
from sklearn.metrics import roc_curve

auc = roc_auc_score(y_test, y_pred_probs)
print(f'AUC: {auc}')

fpr, tpr, thresholds = roc_curve(y_test, y_pred_probs)
eer = brentq(lambda x: 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
print(f'EER: {eer}')   ### FOR Dataset

import torch
import torch.nn as nn
import numpy as np
from sklearn.model_selection import train_test_split
import librosa
import os

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1 = nn.Linear(64 * 64 * 32, 128)
        self.fc2 = nn.Linear(128, 2)  # Output has 2 classes

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 64 * 64 * 32)  # Flatten before fully connected layer
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

new_model = SimpleCNN()

def load_and_preprocess_audio(file_path):
    try:
        audio, sr = librosa.load(file_path, sr=None)
        if audio.size == 0:  # Check if the audio is empty
            print(f"Warning: {file_path} is empty and will be skipped.")
            return None
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        mfccs = mfccs.T
        return mfccs
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

real_dir = '/content/drive/My Drive/custom_dataset/data/real'
fake_dir = '/content/drive/My Drive/custom_dataset/data/fake'
real_features = []
fake_features = []

for filename in os.listdir(real_dir):
    if filename.endswith('.mp3') or filename.endswith('.wav'):
        file_path = os.path.join(real_dir, filename)
        mfccs = load_and_preprocess_audio(file_path)
        if mfccs is not None:
            real_features.append(mfccs)
        else:
            print(f"Skipped None from real: {filename}")  # Debug message

for filename in os.listdir(fake_dir):
    if filename.endswith('.mp3') or filename.endswith('.wav'):
        file_path = os.path.join(fake_dir, filename)
        mfccs = load_and_preprocess_audio(file_path)
        if mfccs is not None:
            fake_features.append(mfccs)
        else:
            print(f"Skipped None from fake: {filename}")  # Debug message

X = real_features + fake_features
X = [x for x in X if x is not None]  # Filter out None values

y = [1] * len(real_features) + [0] * len(fake_features)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

import numpy as np
from sklearn.model_selection import train_test_split

max_length = max(len(mfcc) for mfcc in X)

if X:  
    max_length = max(len(mfcc) for mfcc in X)

    def pad_mfcc(mfcc, max_length):
        padding = max_length - len(mfcc)
        if padding > 0:
            return np.pad(mfcc, ((0, padding), (0, 0)), mode='constant', constant_values=(0, 0))
        return mfcc

    X_padded = np.array([pad_mfcc(mfcc, max_length) for mfcc in X])
else:
    print("No valid data to process")




X = real_features + fake_features

max_length = max(len(mfcc) for mfcc in X)

X_padded = np.array([pad_mfcc(mfcc, max_length) for mfcc in X])

y = [1] * len(real_features) + [0] * len(fake_features)  # 1 for Real, 0 for Fake

X_train, X_test, y_train, y_test = train_test_split(X_padded, y, test_size=0.2, random_state=42)


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve


X_flattened = np.array([x.flatten() for x in X_padded])

X_train, X_test, y_train, y_test = train_test_split(X_flattened, y, test_size=0.2, random_state=42)


model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

y_pred_probs = model.predict_proba(X_test)[:, 1]  # Get the probabilities for the positive class

from sklearn.metrics import roc_auc_score
from scipy.optimize import brentq
from scipy.interpolate import interp1d
from sklearn.metrics import roc_curve

auc = roc_auc_score(y_test, y_pred_probs)
print(f'AUC: {auc}')

fpr, tpr, thresholds = roc_curve(y_test, y_pred_probs)
eer = brentq(lambda x: 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
print(f'EER: {eer}') ### Custom Dataset

#!/usr/bin/env python
# coding: utf-8




#importing libraries

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn import preprocessing


# In[2]:


#reading batsman file
batsman=pd.read_csv('Batsman_2019_Data_csv.csv')
bowler=pd.read_csv('Bowler_2019_Data_csv.csv')

bowler=bowler.fillna(0)
batsman=batsman.fillna(0)


# In[3]:


#how does the data look
batsman.tail(5)


# In[4]:


#are all the columns except the player name column numeric?
flag=0
for col in batsman.columns:
    if(col!='pname' and batsman[col].dtypes=='O'):
        flag=1
        break
if flag==0:
    print("Clustering can be carried out!!")
else:
    print("need to convert")


# In[5]:


#how does bowler data looks
bowler.tail(5)


# In[6]:


#similarly check if clustering can be carried out?
flag=0
for col in bowler.columns:
    if(col!='pname' and bowler[col].dtypes=='O'):
        flag=1
        break
if flag==0:
    print("Clustering can be carried out!!")
else:
    print("need to convert")


# In[8]:


# data preprocessing before k means for bowlers
bowler_data=bowler.drop(columns=['pname'])  #removing first column


# In[9]:


#k means
wss=np.zeros([15])
for i in range(1,15):
    kmeans_bowler=KMeans(n_clusters=i,random_state=0,init='k-means++').fit(bowler_data)
    wss[i]=kmeans_bowler.inertia_

#elbow plot
plt.plot(range(1,15),wss[1:])
plt.xlabel(' No. of clusters')
plt.ylabel(' Total Within Sum of Squares')
plt.title('Elbow plot showing the reduction in WSS with cluster num')


# In[10]:


#optimum clusters is chosen as 4
kmeans_bowler=KMeans(n_clusters=4,random_state=0,init='k-means++').fit(bowler_data)
kmeans_bowler.labels_

#adding labels to original data
bowler['labels']=kmeans_bowler.labels_


# In[11]:


#PCA for visualization

#standardizing the data
# Get column names first
names = bowler_data.columns
# Create the Scaler object
scaler = preprocessing.StandardScaler()
# Fit your data on the scaler object
scaled_bowler_data = scaler.fit_transform(bowler_data)
scaled_bowler_data = pd.DataFrame(scaled_bowler_data, columns=names)


# In[13]:


#performing pca
pca_bowler=PCA(n_components=2)
pca_bowler.fit(scaled_bowler_data)


# In[14]:


#explanation of variability
pca_bowler.explained_variance_ratio_


# In[15]:


pca_bowler_answer=pca_bowler.transform(scaled_bowler_data)


# In[16]:


bowler_visualizer=pd.DataFrame(pca_bowler_answer,columns=['PCA_1','PCA_2'])
bowler_visualizer['labels']=kmeans_bowler.labels_
bowler_visualizer['pname']=bowler['pname']


# In[17]:


bowler_visualizer


# In[18]:


for l, c, m in zip(range(5), ('blue', 'red', 'green','black'), ('^', 's', 'o','d')):
    plt.scatter(bowler_visualizer.loc[bowler_visualizer['labels']==l,'PCA_1'],
                bowler_visualizer.loc[bowler_visualizer['labels']==l,'PCA_2'],
                color=c,
                label='class %s' % l,
                #alpha=0.5,
                marker=m
                )
plt.xlabel('1st PCA component')
plt.ylabel('2nd PCA component')
plt.title('Plot showing the Cluster of Bowlers using PCA')
plt.legend(loc='upper right')
plt.show()


# In[23]:


for i in range(4):
    print("cluster size : ",len(bowler.loc[bowler['labels']==i]),"  for ",i," th cluster")


# In[24]:


bowler.loc[bowler['labels']==0].mean()
bowler.loc[bowler['labels']==1].mean()
bowler.loc[bowler['labels']==2].mean()
bowler.loc[bowler['labels']==3].mean()


# In[29]:


# data preprocessing before k means
batsman_data=batsman.drop(columns=['pname'])  #removing first column

#k means
wss=np.zeros([15])
for i in range(1,15):
    kmeans_batsman=KMeans(n_clusters=i,random_state=0,init='k-means++').fit(batsman_data)
    wss[i]=kmeans_batsman.inertia_

#elbow plot
plt.plot(range(1,15),wss[1:])
plt.xlabel(' No. of clusters')
plt.ylabel(' Total Within Sum of Squares')
plt.title('Elbow plot showing the reduction in WSS with cluster num')

#optimum clusters is chosen as 4
kmeans_batsman=KMeans(n_clusters=4,random_state=0,init='k-means++').fit(batsman_data)
#kmeans_batsman.labels_

#adding labels to original data
batsman['labels']=kmeans_batsman.labels_

#PCA for visualization

#standardizing the data
# Get column names first
names = batsman_data.columns
# Create the Scaler object
scaler = preprocessing.StandardScaler()
# Fit your data on the scaler object
scaled_batsman_data = scaler.fit_transform(batsman_data)
scaled_batsman_data = pd.DataFrame(scaled_batsman_data, columns=names)

#performing pca
pca_batsman=PCA(n_components=2)
pca_batsman.fit(scaled_batsman_data)


# In[30]:


pca_batsman.explained_variance_ratio_


# In[31]:


pca_batsman_answer=pca_batsman.transform(scaled_batsman_data)
batsman_visualizer=pd.DataFrame(pca_batsman_answer,columns=['PCA_1','PCA_2'])
batsman_visualizer['labels']=kmeans_batsman.labels_
batsman_visualizer['pname']=batsman['pname']
for l, c, m in zip(range(5), ('blue', 'red', 'green','black'), ('^', 's', 'o','d')):
    plt.scatter(batsman_visualizer.loc[batsman_visualizer['labels']==l,'PCA_1'],
                batsman_visualizer.loc[batsman_visualizer['labels']==l,'PCA_2'],
                color=c,
                label='class %s' % l,
                #alpha=0.5,
                marker=m
                )
plt.xlabel('1st PCA component')
plt.ylabel('2nd PCA component')
plt.title('Plot showing the Cluster of Batsmen using PCA')
plt.legend(loc='upper right')
plt.show()





for i in range(4):
    print("cluster size : ",len(batsman.loc[batsman['labels']==i]),"  for ",i," th cluster")





batsman.loc[batsman['labels']==0].mean()
batsman.loc[batsman['labels']==1].mean()
batsman.loc[batsman['labels']==2].mean()
batsman.loc[batsman['labels']==3].mean()








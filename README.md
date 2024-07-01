#### Learning-Decision-Rules-with-C4.5

### 🎯 Problem Statement
When dealing with datasets where passing records vastly outnumber failing records (more than 90% passing, less than 10% failing), identifying the conditions leading to failure poses a significant challenge.

### 📊 Information Gain vs. Entropy
Traditional approaches rely on information gain to select the optimal attribute for decision tree splits. However, in scenarios where one branch contains only failing records and the other a mix of pass and fail, the conventional method may falter.

### 🔄 Understanding Entropy Dynamics
The entropy of the latter branch, containing both pass and fail records, remains relatively unchanged post-split, diminishing the impact of information gain.

### 📉 Importance of Gain Ratio
In such imbalanced scenarios, gain ratio, the ratio of information gain to split info, emerges as a critical metric. Split info decreases as one branch accumulates more records, amplifying the significance of gain ratio.

### ⚖️ Achieving the Optimal Split
To achieve the desired split—where one branch exclusively contains failing records and the other all passing records—a meticulous consideration of gain ratio becomes imperative.

### 📱 Streamlit app
App link:https://financial-discrepancy-detection-with-c45.streamlit.app/ \n
Data file: https://github.com/KayalvizhiT513/Financial-Discrepancy-Detection-with-C4.5/blob/main/V4%20PortfolioType_bool.xlsx

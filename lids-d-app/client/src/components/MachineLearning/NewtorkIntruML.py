# @author Josh Shoemaker

import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

# Establish a database connection
# Replace the placeholder values with your actual database credentials
database_url = 'postgresql://username:password@localhost/dbname'
engine = create_engine(database_url)

# Define your SQL query
query = """
SELECT *
FROM your_table_name;
"""

# Execute the query and load the data into a pandas DataFrame
data = pd.read_sql_query(query, con=engine)

# Assuming the column names in your DataFrame match the ones you provided
X = data[['network protocol', 'Source IP Address', 'Dest IP', 'Service', 'bytes sent/received']]
Y = data['attack/normal']

# Split the data
X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.3, random_state=42)

# Initial hyperparameters
h_old = {'max_depth': None, 'min_samples_leaf': 1}

def train_classifier(X_train, Y_train, hyperparameters):
    model = DecisionTreeClassifier(max_depth=hyperparameters['max_depth'],
                                   min_samples_leaf=hyperparameters['min_samples_leaf'])
    model.fit(X_train, Y_train)
    return model

# First training
model = train_classifier(X_train, Y_train, hyperparameters=h_old)

# Evaluate performance
Y_predict_train = model.predict(X_train)
Y_predict_val = model.predict(X_val)
train_performance = metrics.accuracy_score(Y_train, Y_predict_train)
val_performance = metrics.accuracy_score(Y_val, Y_predict_val)

# Example of changing hyperparameters if not satisfied with performance
if val_performance < 0.95:
    h_new = {'max_depth': 10, 'min_samples_leaf': 4}
    model = train_classifier(X_train, Y_train, hyperparameters=h_new)
    Y_predict_val = model.predict(X_val)
    val_performance = metrics.accuracy_score(Y_val, Y_predict_val)

# Check new performance
print(f'Validation Performance: {val_performance}')

# Now you can either return the model or use it to predict on new data
# e.g., model.predict(X_test)

import pandas as pd
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from urllib.parse import urlparse

from sklearn.tree import DecisionTreeRegressor

def train_decision_tree():
    data = pd.read_csv('data/output.csv')
    with mlflow.start_run():
        
        X = data.drop(columns=['Quantity'],axis=1)
        y = data['Quantity']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        decision_tree = DecisionTreeRegressor(max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            max_features=None,
            max_leaf_nodes=None,
            min_impurity_decrease=0.0,
            random_state=42)
        decision_tree.fit(X_train, y_train)
        y_pred = decision_tree.predict(X_test)
        mse_1 = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred) 
        signature = infer_signature(X,y_pred)
        mlflow.log_metric("MSE",mse_1)
        mlflow.log_metric("MAE",mae)
        mlflow.log_metric("r2",r2)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        mlflow.sklearn.log_model(decision_tree,"model",registered_model_name="DecisionTreeRegressor",signature=signature)

if __name__=="__main__":
    train_decision_tree()
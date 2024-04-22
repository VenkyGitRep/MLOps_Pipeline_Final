import pandas as pd
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from urllib.parse import urlparse

def train_sgd():
    data = pd.read_csv('data/output.csv')
    with mlflow.start_run():
        
        X = data.drop(columns=['Quantity'],axis=1)
        y = data['Quantity']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        #Linear Regression:
        sgd_regressor = SGDRegressor(max_iter=1000, tol=1e-3, penalty='l2', alpha=0.001)
        sgd_regressor.fit(X_train, y_train)

        predictions = sgd_regressor.predict(X_test)
        mse_1 = mean_squared_error(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions) 
        signature = infer_signature(X,predictions)
        mlflow.log_metric("MSE",mse_1)
        mlflow.log_metric("MAE",mae)
        mlflow.log_metric("r2",r2)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        mlflow.sklearn.log_model(sgd_regressor,"model",registered_model_name="SGDRegressor",signature=signature)

if __name__=="__main__":
    train_sgd()
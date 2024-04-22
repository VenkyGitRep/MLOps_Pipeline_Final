import pandas as pd
import sklearn
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from urllib.parse import urlparse
from mlflow.models.signature import infer_signature
from mlflow.utils.environment import _mlflow_conda_env
import cloudpickle
import time

from sklearn.tree import DecisionTreeRegressor

# The predict method of sklearn's RandomForestClassifier returns a binary classification (0 or 1).
# The following code creates a wrapper function, SklearnModelWrapper, that uses 
# the predict_proba method to return the probability that the observation belongs to each class.

class SklearnModelWrapper(mlflow.pyfunc.PythonModel):
    def __init__(self, model):
        self.model = model

    def predict(self, context, model_input):
        return self.model.predict(model_input)


def train_decision_tree():
    data = pd.read_csv('data/output.csv')
    with mlflow.start_run(run_name='DecisionTreeRegressor'):
        
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
        wrappedModel = SklearnModelWrapper(decision_tree)
        y_pred = decision_tree.predict(X_test)
        mse_1 = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred) 
        signature = infer_signature(X,wrappedModel.predict(None, X_train))
        mlflow.log_metric("MSE",mse_1)
        mlflow.log_metric("MAE",mae)
        mlflow.log_metric("r2",r2)
        
        conda_env =  _mlflow_conda_env(
            additional_conda_deps=None,
            additional_pip_deps=["cloudpickle=={}".format(cloudpickle.__version__), "scikit-learn=={}".format(sklearn.__version__)],
            additional_conda_channels=None,
        )
        mlflow.pyfunc.log_model("DecisionTreeRegressor",
                            python_model=wrappedModel,
                            conda_env=conda_env,
                            signature=signature)
        #Register model
        run_id = mlflow.search_runs(filter_string='tags.mlflow.runName = "DecisionTreeRegressor"').iloc[0].run_id
        model_name = "online_sales"
        print("run_id:",run_id)
        model_version = mlflow.register_model(f"runs:/{run_id}/DecisionTreeRegressor", model_name)
        mlflow.log_param('Model', "online_sales_model")
        mlflow.sklearn.log_model(decision_tree, "DecisionTreeRegressor")
        # Registering the model takes a few seconds, so add a small delay
        time.sleep(15)

if __name__=="__main__":
    train_decision_tree()
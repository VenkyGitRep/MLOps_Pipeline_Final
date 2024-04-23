# Machine Learning Operations - Model Pipeline for Stock Price Prediction

## Problem Statement
We aim to predict stock prices using two years of data from the Online Retail Dataset, which includes sales of stocks in the United Kingdom and other parts of Europe. While it is recognized that using historical data to predict stock prices may not be effective in real-world scenarios, this dataset serves the purpose of building the infrastructure for model training and deployment in this project.

### Dataset
The [Online Retail Dataset](https://www.kaggle.com/datasets/ulrikthygepedersen/online-retail-dataset) contains information about sales transactions, including stock codes, quantities sold, invoice dates, and countries.

## Objective
Our goal is to leverage this dataset to develop a machine learning pipeline that can predict future stock prices based on historical data.

## Pipeline

The data pipeline is built using Apache Airflow and consists of the following Directed Acyclic Graphs (DAGs):

- **download_file_task**: Downloads the dataset from a specified URL (`https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip`), saves it locally, and returns the path to the downloaded zip file. It creates a directory to store the data if it does not exist and prints messages indicating the download progress.

- **unzip_file_task**: Extracts the contents of a specified zip file (`online_retail_II.zip`) to a designated output directory. It utilizes the Python `zipfile` module for extraction and handles exceptions, such as bad zip files. Upon successful extraction, it prints a completion message and returns the path to the extracted file (`Online_Retail_II.xlsx`).

- **create_newfile_task**: Executes a task to create new Excel files from the `online_retail_II.xlsx` input file. This task calls the `create_newfile` function, which reads data from the input Excel file, separates it into two dataframes, and saves each dataframe as a new Excel file (`data_1.xlsx` and `data_2.xlsx`). The paths to the created files are returned by the function.

- **merge_files_task**: Executes a task to merge multiple Excel files into a single CSV file. This task calls the `merg_files` function, which searches for Excel files with names starting with "data" in the `data` directory, reads them into pandas dataframes, concatenates them into a single dataframe, and then saves the merged dataframe as a CSV file named `Online_Retail.csv` in the same directory.

- **preprocess_data_task**: Executes a task to preprocess the raw data from the `Online_Retail.csv` file. This task calls the `preprocess()` function, which reads the raw data, removes rows with missing Description values, drops unnecessary columns, filters out frequent StockCodes, extracts date features, converts categorical variables to numerical labels using `LabelEncoder`, and filters out outliers. The preprocessed data is then written to a CSV file named `output.csv`. 

- **upload_processed_data_gcs**: Executes a task to upload the preprocessed data CSV file (`output.csv`) to Google Cloud Storage (GCS). This task uses the `LocalFilesystemToGCSOperator` operator to transfer the file from the local filesystem to the specified GCS bucket (`dvc_bucket_mlops_lab`). The source file path is defined as the absolute path to the `output.csv` file in the `data` directory. The destination path in GCS is set as `processed_output_data/output.csv`. The `gcp_conn_id` parameter specifies the Google Cloud Platform (GCP) connection to use for authentication.

- **slack_processing_complete**: Executes a task to send a notification message to a Slack channel indicating that the processing of data is complete. This task uses the `SlackWebhookOperator` operator to send a message to the specified Slack channel (`#mlops_alerts`) using the webhook connection ID `mlops_slack_alerts`. The message content is set as "Processed data has been uploaded to Google Cloud Storage bucket."

- **train_sgd_task**:The `train_sgd_task` DAG trains an SGDRegressor model on the online retail dataset. It uses the `train_sgd()` function, which reads the preprocessed data, splits it into training and testing sets, initializes the SGDRegressor model, trains it, evaluates its performance, and logs the model and its associated metrics using MLflow. Additionally, it registers the trained model with MLflow for later use.

- **train_decision_tree_task** : This DAG trains a Decision Tree Regressor model on preprocessed data to predict stock quantities. It loads the preprocessed data, splits it into training and testing sets, and initializes a DecisionTreeRegressor model. The trained model's performance metrics such as Mean Squared Error (MSE), Mean Absolute Error (MAE), and R-squared (R2) are logged with MLflow. Additionally, the trained model is logged and registered with MLflow for model tracking and versioning.

- **train_knn_task** : This DAG trains a K-Nearest Neighbors (KNN) regressor model using the provided dataset. It loads the data, splits it into training and testing sets, trains the model, evaluates its performance, and logs the results to MLflow. Finally, the trained model is wrapped, logged, and registered for future reference and deployment.

- **get_best_run_task** : Retrieves the best MLflow run based on logged metrics. It loads the corresponding model and makes predictions using the loaded model. This task is essential for model selection and evaluation in the machine learning pipeline.

- **send_slack_notification**: Sends a notification to a Slack channel specified by '#mlops_alerts' using a webhook connection named 'mlops_slack_alerts'. The message "Your datapipeline is complete." indicates the completion of the data pipeline execution.


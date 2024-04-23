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

## Airflow DAG Overview

The visual represents the Directed Acyclic Graph (DAG) designed in Apache Airflow for our machine learning pipeline. It is constructed to ensure a seamless sequence of tasks, from data preparation to model training and final notifications.

The model training tasks for SGD Regressor, Decision Tree Regressor, and K-Nearest Neighbors are configured to run in parallel. This design demonstrates an efficient use of resources, allowing multiple models to be trained simultaneously, following the successful completion of the preprocessing task.

Following the training, the `get_best_run_task` is engaged to evaluate each model against set performance metrics. The model that exhibits the best metrics is flagged as the 'best model.' This strategy ensures that our pipeline not only trains multiple models but also selects the most effective one, reflecting our commitment to accuracy and reliability in stock price prediction.

The DAG concludes with a `send_slack_notification` task, signaling the successful completion of the pipeline and the readiness of the chosen model for deployment or further evaluation.
![alt text](<images_report/Airflow_DAGs.png>)

## Experimental Tracking with MLflow

MLflow provides a robust platform for managing the machine learning lifecycle, including experimentation, reproducibility, and deployment. Below is a snapshot of the MLflow tracking interface, capturing various runs of the machine learning models trained during our experiments:

- **Run Name**: Indicates the type of model trained during each run. For example, `knn_regressor` represents a K-Nearest Neighbors regressor model.

- **Created**: Shows the timestamp of when the model training was initiated, providing insights into the duration and recentness of each experiment.

- **Duration**: Reflects the time taken to train each model, which is crucial for understanding the computational efficiency of different algorithms.

- **Source**: This column provides a link to the specific execution source, which could be a notebook or a script, facilitating traceability and reproducibility of the experiments.

- **Models**: Indicates the models that were output from each run, with a direct link to the stored model for ease of access and further analysis.

In our MLflow dashboard, we can observe the runs of different models like `sgd_regressor`, `DecisionTreeRegressor`, and `knn_regressor`. Each run is logged with comprehensive details, allowing us to track the performance of different algorithms systematically. By comparing metrics across these runs, we can determine the best-performing model for our stock price prediction objective.

The MLflow interface also enables us to perform complex queries to filter runs, such as `metrics.rmse < 1 and params.model == "tree"`—demonstrating its powerful search capabilities for identifying the most promising models based on specified criteria.

Through MLflow, we establish a structured and scalable approach to experimenting with various models, thereby enhancing our capability to manage and optimize machine learning workflows.

![alt text](<images_report/ML_Flow_Dashboard.png>)

## Model Performance Comparison in MLflow

The MLflow tracking system provides a detailed comparison of model performance across three key metrics: Mean Absolute Error (MAE), Mean Squared Error (MSE), and the coefficient of determination (R2). Here's a snapshot of the tracked metrics for our three models: SGD Regressor, KNN Regressor, and Decision Tree Regressor.

### Mean Absolute Error (MAE)
- **SGD Regressor**: Demonstrates a relatively low MAE, suggesting a closer average predicted value to the actual data points.
- **KNN Regressor**: Exhibits a MAE value in the same range as the SGD Regressor, indicating comparable average accuracy.
- **Decision Tree Regressor**: Shows varied MAE results across different runs, hinting at potential overfitting or sensitivity to the dataset's features.

### Mean Squared Error (MSE)
- **SGD Regressor**: Presents a consistent MSE, reflecting a stable prediction error across multiple runs.
- **KNN Regressor**: Reports a similar MSE to the SGD Regressor, affirming its reliable prediction capability.
- **Decision Tree Regressor**: The MSE varies significantly, which could be due to the complexity of the model and its interaction with different data splits.

### R-Squared (R2)
- **SGD Regressor**: The R2 score is close to 0, suggesting that the model may not be capturing all the variability in the data.
- **KNN Regressor**: Similar to the SGD, its R2 score is around 0, indicating room for improvement in model performance.
- **Decision Tree Regressor**: Exhibits erratic R2 values, some of which are negative, implying that certain runs of the model perform worse than a horizontal line fit.

The MLflow charts illustrate the need for careful model selection and hyperparameter tuning. By leveraging MLflow’s visualization capabilities, we can better understand model behaviors and guide the refinement of our predictive models for enhanced stock price prediction accuracy.
![alt text](<images_report/ML_flow_visualization.png>)

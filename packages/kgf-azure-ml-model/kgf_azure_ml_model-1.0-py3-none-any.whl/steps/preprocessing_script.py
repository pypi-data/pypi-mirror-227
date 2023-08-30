import os
import argparse

import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest, f_classif
from azureml.core import Workspace, Experiment, Environment, Dataset
from constants import ENVIRONMENT_NAME
from utils import StepsUtils

class DataPreprocessor:

    def __init__(self, data_file):
        self.data_file = data_file
        self.encoder = None
        self.scaler = None
        self.smote = None
        self.selector = None
        self.pca = None
        self.vectorizer = None
        self.imputer = None

    
    def load_data(self):
        data = pd.read_csv(self.data_file)
        return data
    
    def load_data_from_file(self, filename):
        """
        Load data from a CSV file.

        Parameters:
        - filename (str): Path to the CSV file.

        Returns:
        - data (pd.DataFrame): Loaded data as a pandas DataFrame.
        """
        data = pd.read_csv(filename)
        return data
    
    
    def remove_special_characters(self, text):
        """
        Remove special characters from text.

        Parameters:
        - text (str): Input text.

        Returns:
        - cleaned_text (str): Text with special characters removed.
        """
        cleaned_text = re.sub(r'[^\w\s]', '', text)
        return cleaned_text

    def remove_hyperlinks(self, text):
        """
        Remove hyperlinks from text.

        Parameters:
        - text (str): Input text.

        Returns:
        - cleaned_text (str): Text with hyperlinks removed.
        """
        cleaned_text = re.sub(r'http\S+', '', text)
        return cleaned_text

    def handle_missing_values(self, data, columns_to_impute):
        """
        Handle missing values in specified columns using mean imputation.

        Parameters:
        - data (pd.DataFrame): Input data.
        - columns_to_impute (list): List of column names to impute.

        Returns:
        - imputed_data (pd.DataFrame): Data with missing values imputed.
        """
        self.imputer = SimpleImputer(strategy='mean')
        data[columns_to_impute] = self.imputer.fit_transform(data[columns_to_impute])
        return data

    def process_text_column(self, text_column):
        """
        Process a text column by removing special characters, hyperlinks, and converting to lowercase.

        Parameters:
        - text_column (pd.Series): Text column to be processed.

        Returns:
        - processed_column (pd.Series): Processed text column.
        """
        processed_column = text_column.apply(self.remove_special_characters)
        processed_column = processed_column.apply(self.remove_hyperlinks)
        processed_column = processed_column.str.lower()
        return processed_column

    def preprocess_data(self, data, columns_to_impute, text_columns):
        """
        Preprocess data by handling missing values and processing text columns.

        Parameters:
        - data (pd.DataFrame): Input data.
        - columns_to_impute (list): List of column names to impute.
        - text_columns (list): List of text column names to process.

        Returns:
        - preprocessed_data (pd.DataFrame): Data after preprocessing.
        """
        cleaned_data = data.copy()
        cleaned_data = self.handle_missing_values(cleaned_data, columns_to_impute)
        for col in text_columns:
            cleaned_data[col] = self.process_text_column(cleaned_data[col])
        return cleaned_data
    

    def transform_categorical(self, data):
        """
        Transform categorical features using one-hot encoding.

        Parameters:
        - data (pd.DataFrame): Data with categorical features.

        Returns:
        - data_encoded (pd.DataFrame): Data with one-hot encoded categorical features.
        """
        self.encoder = OneHotEncoder()
        encoded_features = self.encoder.fit_transform(data[['categorical_column']])
        data_encoded = pd.concat([data, pd.DataFrame(encoded_features.toarray(), columns=self.encoder.get_feature_names_out(['categorical_column']))], axis=1)
        data_encoded.drop(['categorical_column'], axis=1, inplace=True)
        return data_encoded

    def split_data(self, data, target_column, test_size=0.2, random_state=42):
        """
        Split data into training and testing sets.

        Parameters:
        - data (pd.DataFrame): Data to be split.
        - target_column (str): Name of the target column.
        - test_size (float, optional): Proportion of data to be used for testing. Default is 0.2.
        - random_state (int, optional): Random seed for reproducibility. Default is 42.

        Returns:
        - X_train (pd.DataFrame): Training features.
        - X_test (pd.DataFrame): Testing features.
        - y_train (pd.Series): Training target.
        - y_test (pd.Series): Testing target.
        """
        X = data.drop([target_column], axis=1)
        y = data[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        return X_train, X_test, y_train, y_test

    def scale_features(self, X_train, X_test):
        """
        Scale numerical features using StandardScaler.

        Parameters:
        - X_train (pd.DataFrame): Training features.
        - X_test (pd.DataFrame): Testing features.

        Returns:
        - X_train_scaled (pd.DataFrame): Scaled training features.
        - X_test_scaled (pd.DataFrame): Scaled testing features.
        """
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled

    def resample_data(self, X_train, y_train):
        """
        Resample imbalanced data using SMOTE.

        Parameters:
        - X_train (pd.DataFrame): Training features.
        - y_train (pd.Series): Training target.

        Returns:
        - X_resampled (pd.DataFrame): Resampled training features.
        - y_resampled (pd.Series): Resampled training target.
        """
        self.smote = SMOTE()
        X_resampled, y_resampled = self.smote.fit_resample(X_train, y_train)
        return X_resampled, y_resampled

    def select_features(self, X_train, X_test, y_train):
        """
        Select the most important features using SelectKBest.

        Parameters:
        - X_train (pd.DataFrame): Training features.
        - X_test (pd.DataFrame): Testing features.
        - y_train (pd.Series): Training target.

        Returns:
        - X_train_selected (pd.DataFrame): Selected training features.
        - X_test_selected (pd.DataFrame): Selected testing features.
        """
        self.selector = SelectKBest(score_func=f_classif, k=10)
        selected_features = self.selector.fit_transform(X_train, y_train)
        X_train_selected = self.selector.transform(X_train)
        X_test_selected = self.selector.transform(X_test)
        return X_train_selected, X_test_selected

    def reduce_dimensionality(self, X_train_selected, X_test_selected, n_components=2):
        """
        Reduce dimensionality using PCA.

        Parameters:
        - X_train_selected (pd.DataFrame): Selected training features.
        - X_test_selected (pd.DataFrame): Selected testing features.
        - n_components (int, optional): Number of components for PCA. Default is 2.

        Returns:
        - X_train_reduced (pd.DataFrame): Reduced training features.
        - X_test_reduced (pd.DataFrame): Reduced testing features.
        """
        self.pca = PCA(n_components=n_components)
        X_train_reduced = self.pca.fit_transform(X_train_selected)
        X_test_reduced = self.pca.transform(X_test_selected)
        return X_train_reduced, X_test_reduced

    def vectorize_text(self, text_data):
        """
        Vectorize text data using CountVectorizer.

        Parameters:
        - text_data (list): List of text strings.

        Returns:
        - vectorized_text (scipy.sparse.csr_matrix): Vectorized text data.
        """
        self.vectorizer = CountVectorizer()
        vectorized_text = self.vectorizer.fit_transform(text_data)
        return vectorized_text
    
  

    def preprocess(self, data):
        X = data.drop([ 'New Application ID'], axis=1)
    
        label_encoders = {}
        for column in X.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            X[column] = le.fit_transform(X[column])
            label_encoders[column] = le
        
        y = X['Applied Residency programs']
        
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        return X_train, X_val, y_train, y_val, label_encoders
    
    def kfold_preprocess(self, data):
        #X = data.drop([ 'New Application ID'], axis=1)
        data['target'] = LabelEncoder().fit_transform(data['Applied Residency programs'])

        X = data.drop(columns=['target'])  # Make sure 'Total Score' column is in the DataFrame

        label_encoders = {}
        for column in X.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            X[column] = le.fit_transform(X[column])
            label_encoders[column] = le
        
        y = data['target']
    

        return X, y, label_encoders

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, help='Path to data')
    args = parser.parse_args()
    
    ws = StepsUtils.get_workspace()
    data_path = args.data_path

    obj = DataPreprocessor(data_path)
    # df = obj.load_data()

    dataset = Dataset.get_by_name(ws, name='candidates')
    df = dataset.to_pandas_dataframe()

    print(df)

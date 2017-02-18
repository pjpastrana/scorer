import sys
import pandas as pd
import json
import numpy as np

RAW_DATA = None

def main(argv):
    (data, features) = load_data(argv[1])
    weights = load_weights(argv[2], features)
    results = calculate_score(data, weights)

def load_data(csv_file_location):
    global RAW_DATA
    RAW_DATA = pd.read_csv(csv_file_location)
    data = RAW_DATA.copy(deep=True)
    all_columns = data.columns.values
    numeric_columns = data._get_numeric_data().columns.values
    categorical_columns = list(set(all_columns) - set(numeric_columns))
    for column in categorical_columns:
        data[column] = data[column].astype('category').cat.codes + 1
    return (data.as_matrix(), data.columns.values)

def load_weights(json_file_location, features):
    fin = open(json_file_location)
    jsonString = fin.read().strip()
    fin.close()
    json_obj = json.loads(jsonString)
    num_features = len(features)
    weights = np.zeros(num_features)
    for i in range(num_features):
        feature = features[i]
        weights[i] = json_obj[feature]
    return weights

# TODO: how to consider weights on categorical data
def calculate_score(data, weights):
    print data.dot(weights)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Provide weights and data files")
        sys.exit(0)
    
    main(sys.argv)
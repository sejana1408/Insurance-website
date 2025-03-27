import pandas as pd 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE

def preprocess_data(file_path):
    df = pd.read_csv(file_path)

    df.fillna("Unknown", inplace=True)
    remove_cols=['Source_of_Lead','Time_Since_First_Contact','Conversion_Status','Website_Visits','Inquiries','Quotes_Requested','Time_to_Conversion','Premium_Amount']
    df=df.drop(columns=remove_cols)
    label_encoders = {}
    categorical_cols = ['Marital_Status', 'Prior_Insurance', 'Claims_Severity', 'Policy_Type', 'Region']
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    X = df.drop(columns=["Policy_Type"])
    y = df["Policy_Type"]

    smote = SMOTE(sampling_strategy="not majority", random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    print("\nAfter SMOTE:\n", pd.Series(y_resampled).value_counts())

    df_resampled = pd.DataFrame(X_resampled, columns=X.columns)
    df_resampled["Policy_Type"] = y_resampled

    return df_resampled, label_encoders

def train_model(df):
    X = df.drop(columns=['Policy_Type'])  
    y = df['Policy_Type']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred) * 100
    print(f"Model Accuracy: {accuracy:.2f}%")
    print("Classification Report:\n", classification_report(y_test, y_pred))
    
    return model, X.columns

def match_policy(prediction, age):
    policy_mapping = {
        0:"health insurance",
        1: "Life Insurance",
        2: "Auto Insurance",
        3: "Homeowners Insurance",
        4: "Renters Insurance",
        5: "Disability Insurance",
        6: "Travel Insurance",
        7: "Business Insurance",
        8: "Pet Insurance",
        9: "Cyber Insurance"
    }

    # Apply Age-Based Constraints
    if age < 18:
        return "No Insurance Available for Minors"
    elif age < 25 and prediction in [3, 5, 7]:  
        return "Age Restricted - Alternative: Renters Insurance"
    elif age > 70 and prediction in [2, 5]:
        return "Age Restricted - Alternative: Health Insurance"
    
    return policy_mapping.get(prediction, "Unknown Policy")

def recommend_policy(user_input, model, feature_cols, label_encoders):
    # Preprocess user input
    user_df = pd.DataFrame([user_input], columns=feature_cols)
    
    # Encode categorical features using the same label encoders
    for col in user_df.select_dtypes(include=["object"]).columns:
        if col in label_encoders:
            user_df[col] = label_encoders[col].transform(user_df[col])
    
    # Make prediction
    prediction = model.predict(user_df)[0]
    return match_policy(prediction, user_input['Age'])

# Path to your dataset
dataset_path = "D:\\FINAI\\synthetic_insurance_data.csv"

# Preprocess data
df, label_encoders = preprocess_data(dataset_path)

# Train model
model, feature_cols = train_model(df)

# User input for recommendation
user_input = {
    "Age":34,
    "Income": 75000,
    "Credit_Score": 720,
    "Car_Ownership": 0,   
    "Marital_Status": 1,
    "Prior_Insurance": 1,
    "Claims_Frequency": 2,
    "Claims_Severity": 1,
    "Policy_Adjustment": 1,
    "Safe_Driver_Discount": 0,
    "Multi_Policy_Discount": 1,
    "Bundling_Discount": 0,
    "Total_Discounts": 1,
    "Premium_Adjustment_Credit": -100,
    "Region": 2,  
    "Premium_Adjustment_Region": 200,
}

# Recommend Insurance Policy
recommended_policy = recommend_policy(user_input, model, feature_cols, label_encoders)
print(f"Recommended Insurance Policy: {recommended_policy}")
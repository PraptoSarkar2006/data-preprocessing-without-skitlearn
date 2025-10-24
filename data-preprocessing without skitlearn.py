import pandas as pd 
##identifying categorical variables, and showing them
def get_categorical_columns(df):
    s = (df.dtypes == 'object')
    object_cols = list(s[s].index)
    print("\nCategorical variables:")
    print(object_cols)
    return object_cols 
##one hot encoding function
def one_hot_encode(df, categorical_cols):
    print("\n--- One-Hot Encoding ---")
    for col in categorical_cols:
        unique_vals = df[col].dropna().unique()
        for val in unique_vals:
            new_col_name = f"{col}_{val}"
            df[new_col_name] = (df[col] == val).astype(int)
        df.drop(columns=[col], inplace=True)
    print("One-hot encoding done for:", categorical_cols)
    return df
##ordinal encoding function
def ordinal_encode(df, categorical_cols):
    print("\n--- Ordinal Encoding ---")
    for col in categorical_cols:
        unique_vals = df[col].dropna().unique()
        mapping = {val: i for i, val in enumerate(unique_vals)}
        df[col] = df[col].map(mapping)
        print(f"Column '{col}' mapping:", mapping)
    print("Ordinal encoding done for:", categorical_cols)
    return df
## Fill missing numeric values with mean(imputation ) and add a column to record which values were missing.only uses numeric column
## imputation where missingg data is not recorded ,sometimes give better result
## deleting the entire column 😅😅 if not nessesary enough
def missingValue(df):
   
    numeric_columns = df.select_dtypes(exclude=['object']).columns

    # Find numeric columns with missing values
    missing_columns = [col for col in numeric_columns if df[col].isnull().any()]

    if not missing_columns:
        print("no numeric columns have missing values!!😃")
        return df

    #Shows the columns for a check for a choice
    print("\nColumns with missing values and their counts:")
    for col in missing_columns:
        missing_count = df[col].isnull().sum()
        print(col + ": " + str(missing_count) + " missing values")  

        print("Choose method for '" + col + "':")
        print("1 for Extended Imputation (fill with mean & record missing)")
        print("2 for Manual Imputation (you enter value)")
        print("3 for Delete column")

        choice = input("Enter 1, 2, or 3: ")
        while choice not in ['1', '2', '3']:
            choice = input("Please enter correctly 😡 1, 2, or 3: ")

        
        if choice == '1':
            # Extended imputation
            df[col + "_was_missing"] = df[col].isnull().astype(int)
            mean_value = df[col].mean()
            df[col].fillna(mean_value, inplace=True)
            print(f"Filled '{col}' with mean ({mean_value}) and recorded missing values.")

        elif choice == '2':
            # simple imputation
            mean_value = df[col].mean()
            df[col].fillna(mean_value, inplace=True)
            print("Filled column '" + col + "' with mean value " + str(mean_value))

        else:
            # Delete column
            df.drop(columns=[col], inplace=True)
            print(f"Deleted column '{col}'")

    return df

#file loading using panda 
def main():
    print("Prapto sarkar - Data Preprocessing Tool")
    file_name = input("Enter your CSV file name (with .csv): ")

    df = pd.read_csv(file_name)
    print("\n File loaded successfully!\n")
    print("Here’s a preview of your data:\n")
    print(df.head())
    ##for categorical coloumns handling
    cat_cols = get_categorical_columns(df)

    if cat_cols:
        print("\nChoose encoding method for categorical variables:")
        print("1 for One-Hot Encoding")
        print("2 for Ordinal Encoding")
        user_choice = input("Enter 1 or 2: ")
        while user_choice not in ['1', '2']:
            user_choice = input("Please enter correctly 😡 1 or 2: ")

        if user_choice == '1':
            df = one_hot_encode(df, cat_cols)
        else:
            df = ordinal_encode(df, cat_cols)
    
    # --- Handle numeric missing values ---
    df = missingValue(df)

    print("\n--- Preprocessing Completed ---")
    print("Here’s a preview of your processed data:\n")
    print(df.head())

    return df
# --- Run the program ---
if __name__ == "__main__":
    main()

   
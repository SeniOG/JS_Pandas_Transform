import pandas as pd
import os, re
from config import directory_path
from skills_list import skills_list
from datetime import datetime, timedelta

from datetime import datetime, timedelta


def parse_date(date_str, scrape_date_str):
    if isinstance(date_str, float):  # Check if date_str is a float
        return None
    elif date_str == 'Recently':
        return scrape_date_str
    elif date_str == 'Expires Today':
        return None  
    elif date_str == 'Yesterday':
        scrape_date = datetime.strptime(scrape_date_str, '%d-%m-%Y')
        return (scrape_date - timedelta(days=1)).strftime('%d-%m-%Y')
    elif 'Posted' in date_str and 'days ago' in date_str:
        days_ago = int(date_str.split()[1])  # Extract the number of days ago
        scrape_date = datetime.strptime(scrape_date_str, '%d-%m-%Y')
        return (scrape_date - timedelta(days=days_ago)).strftime('%d-%m-%Y')
    

def skill_search(large_string):
    if isinstance(large_string, str):  # Check if large_string is a string

       words = large_string.split()
       words = re.findall(r'\b\w+\b', large_string.lower())

    
       matching_words = set()

       for word in words:
           if word in skills_list:
               matching_words.add(word)
        
       return(matching_words)
    else:
        return(set())
    
def extract_salary(text):
    # Regular expression pattern to match salaries with or without commas and decimals, including ranges like '£70k - £90k'
    pattern = r'£?(\d{1,3}(?:,\d{3})*\.?\d*)(?:\s*k)?(?:\s*-\s*£?(\d{1,3}(?:,\d{3})*\.?\d*)(?:\s*k)?)?'
    match = re.search(pattern, text)
    if match:
        # Extract the lower bound if available, otherwise extract the single salary value
        if match.group(1):
            salary_str = match.group(1).replace(',', '')
            if 'k' in text:
                return int(float(salary_str) * 1000)  # Convert 'k' to thousand
            else:
                return int(float(salary_str))  # Convert the salary string to float first to handle decimals
        elif match.group(2):
            upper_bound_str = match.group(2).replace(',', '')
            return int(float(upper_bound_str))  # Convert the salary string to float first to handle decimals
    return None


    
def clean_salary(text):
    text = str(text)
    if 'market rates' in text.lower():
        return 'market rate'
    elif 'per day' in text.lower():
        return 'day rate'
    elif 'per annum' in text.lower():
        salary = extract_salary(text)
        return salary
    elif 'negotiable' in text.lower() or 'competitive' in text.lower():
        return 'undisclosed'
    elif 'k' in text:
        return extract_salary(text)
    else:
        try:
            return extract_salary(text)
        except:
            return None

# Get the terminal width 
terminal_width = os.get_terminal_size().columns

# Set the display width to the terminal width
pd.set_option('display.width', terminal_width)
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns

# Initialize an empty list to store DataFrames
dfs = []

# Iterate over CSV files in the directory
for file in os.listdir(directory_path):
    if file.endswith(".csv"):
        # Read the CSV file into a DataFrame
        file_path = os.path.join(directory_path, file)
        df = pd.read_csv(file_path, delimiter='|', skiprows=1, header=None)
        
        # Specify column names
        column_names = ["TITLE", "SALARY", "RECRUITER", "DATE", "LINK", "JOB_DESC", "SCRAPE_DATE"]
        df.columns = column_names

        # Adjust column widths to fit terminal width
        num_columns = len(column_names) + 1 #add one more for skills column
        column_width = int(terminal_width / num_columns)
        pd.set_option('display.max_colwidth', column_width)

        # Clean the 'JOB_DESC' column using skill_search function
        try:
            df['SKILLS'] = df['JOB_DESC'].apply(lambda x: ', '.join(skill_search(x)))
        except Exception as e:
             df['SKILLS'] = 'ERROR'
             print('Error occured:', e)
        # Append the DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames into a single DataFrame
dirty_df = pd.concat(dfs, ignore_index=True)

# Remove newline characters and column titles
dirty_df = dirty_df.apply(lambda col: col.map(lambda x: x.replace('\n', '') if isinstance(x, str) else x))
dirty_df = dirty_df.apply(lambda col: col.map(lambda x: x.split(':', 1)[-1].strip() if isinstance(x, str) else x))

dirty_df.drop_duplicates(inplace= True)

dirty_df['DATE'] = dirty_df.apply(lambda row: parse_date(row['DATE'], row['SCRAPE_DATE']), axis=1)
dirty_df['SALARY2'] = dirty_df.apply(lambda row: clean_salary(row['SALARY']), axis=1)

clean_df = dirty_df.dropna()


# alphabetical order
# dirty_df= dirty_df.sort_values(by='TITLE', ascending=True)





print('\n')
print(dirty_df)

print('\n')
print(clean_df)

today_date = datetime.today().strftime('%d-%m-%Y')

# Create the directory if it does not exist
os.makedirs('cleanData', exist_ok=True)

# Define the file path with today's date
file_path = f'cleanData/clean_data-{today_date}.csv'

# Save the DataFrame to the specified file path
clean_df.to_csv(file_path, index=False)

print(f'DataFrame saved to {file_path}')

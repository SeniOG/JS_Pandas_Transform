# Job Listings Data Cleaning Script
This Python script is designed to clean and preprocess job listings data obtained from CSV files. It performs various data cleaning tasks such as removing newline characters, extracting relevant information, and converting date formats. The cleaned data is then stored in a Pandas DataFrame for further analysis.

## Features
Data Cleaning: Removes newline characters and extracts relevant information from job listings data.
Date Parsing: Converts date strings to a standard format, handling cases such as "Yesterday" and "Expires Today".
Skills Extraction: Extracts relevant skills from job descriptions using a predefined list of skills.
Terminal Display: Adjusts column widths to fit the terminal width for better readability.
## Usage
Clone the repository to your local machine.
Ensure you have Python installed along with the required dependencies listed in requirements.txt.
Place your CSV files containing job listings data in the specified directory (directory_path).
Run the script (TJPdClean.py).

### Mac
python3 TJPdClean.py
### Windows
python TJPdClean.py 

View the cleaned data displayed in the terminal.

## Dependencies
python3
pandas
datetime
## Configuration
Modify directory_path in config.py to specify the directory where your CSV files are located.
Update skills_list.py to include the list of relevant skills for extraction.
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT
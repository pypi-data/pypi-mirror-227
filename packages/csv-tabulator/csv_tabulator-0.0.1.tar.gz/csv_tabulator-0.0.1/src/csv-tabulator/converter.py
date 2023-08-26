'''
The method simply converts the csv file to an html table
Author(s):
  1. Amiay Narayan
  2.
'''



import argparse
import pandas as pd
import re
import sys

def decorate_table(html_table):
  '''method to add bling to the table'''
  html_table = re.sub(r'<table .*>', '<table class="table table-striped">', html_table)
  html_table = re.sub(r'<tr .*>', '<tr>', html_table)
  #html_table = html_table.replace('<tr>', '<tr><th scope="row">1</th>')
  return f'''
  <!DOCTYPE html>
  <html>
  <head>
    <title>CSV to HTML</title>
    <!-- Include Bootstrap CSS link -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  </head>
  <body>
    <div class="container mt-6">
      {html_table}
    </div>
    <!-- Include Bootstrap JS and jQuery scripts (optional) -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  </body>
  </html>
  '''

def create_table(data):
  '''method to create the table'''
  # Convert DataFrame to HTML table
  print('Converting to HTML...')
  try:
    html_table = data.to_html(index=False)
  except Exception as error:
    sys.exit('Problem converting to HTML table... Please make sure that the data is properly formatted as CSV')
  # Save HTML table to a file
  # time.sleep()
  return decorate_table(html_table) 

def write_table(html, html_output_path):
  '''write the html'''
  print(f'Writing the HTML file to {html_output_path}')
  try:
    with open(html_output_path, 'w') as html_file:
      html_file.write(html)
  except Exception as error:
    print(error)
    sys.exit('The File location that you provided does not exist on your local system')

def read_file(csv_file_path):
  '''method to read the csv file'''
  # Read CSV file into a DataFrame
  try:
    data = pd.read_csv(csv_file_path)
  except Exception as error:
    print(error)
    sys.exit('Problem reading file... Prabho!')
  print('File Reading... Done!')
  return data

def csv_to_html(csv_file_path, html_output_path):
  data = read_file(csv_file_path)
  file = create_table(data)
  write_table(file, html_output_path)
  print('Done...!')

def main():
  args = read_args()
  csv_file_path = args.csv_file
  html_output_path = args.html_file
  csv_to_html(csv_file_path, html_output_path)

def read_args():
  '''method to read arguments'''
  parser = argparse.ArgumentParser(description="Convert CSV to HTML table")
  parser.add_argument("--csv-file", required=True, help="Path to input CSV file")
  parser.add_argument("--html-file", required=True, help="Path to output HTML file")

  return parser.parse_args()

if __name__ == "__main__":
    main()


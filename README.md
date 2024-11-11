# Python Job Vacancies Scraper and Analysis

This project includes a Scrapy spider for scraping Python job vacancies from [jobs.dou.ua](https://jobs.dou.ua/) and an analytical part that extracts Python technologies from the job descriptions, creates a word cloud, and visualizes the top technologies.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Scrapy Spider](#scrapy-spider)
4. [Analytical Part](#analytical-part)
5. [Word Cloud](#word-cloud)
6. [Contact](#contact)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/python-job-vacancies.git
    cd python-job-vacancies
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Running the Scrapy Spider

To run the Scrapy spider and scrape the job vacancies, use the following command:
```sh
scrapy crawl vacancies
```

The scraped data will be saved in `data/vacancies.csv`.

### Analytical Part
After scraping the data, use the provided script to analyze the data and generate visualizations.

Open a Python script or Jupyter notebook.

Use the following code to read the data and perform the analysis:

python
```
# Imports
import re
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

from analysis.python_technologies import python_technologies_list


# Read csv file
df = pd.read_csv("../data/vacancies.csv")

# Function definition for finding technologies in the vacancy description
def find_technologies(description: str) -> str:
    found_techs = []
    for tech in python_technologies_list:
        if re.search(r"\b" + re.escape(tech) + r"\b", description, re.IGNORECASE):
            found_techs.append(tech)
    return ", ".join(found_techs)

# Applying function to the dataframe
df["technologies"] = df["description"].apply(find_technologies)

# Plotting top-20 technologies
all_techs = df["technologies"].str.split(", ").explode()

tech_counts = all_techs.value_counts().head(20)

plt.figure(figsize=(8, 4))
plt.bar(tech_counts.index, tech_counts.values, color="skyblue")
plt.xlabel("Number of Vacancies")
plt.ylabel("Technologies")
plt.title("Occurrences of Python Technologies in Job Vacancies (All Experience Levels)")

for j, value in enumerate(tech_counts.values):
    plt.annotate(str(value), xy=(j, value), ha="center", va="bottom")

plt.tight_layout()
plt.xticks(rotation=80)

# Saving the plot
plt.savefig(f"plots/top-20-technologies-all-{datetime.now().strftime('%d-%m-%y')}.png", format="png")

plt.show()

```

## Scrapy Spider
The Scrapy spider is defined in scraping/spiders/vacancies.py. It uses Selenium to load job listings and extract details such as job title, description, experience level, company, placing date, location, and salary.

## Analytical Part
The analytical part involves processing the scraped data to identify the most common Python technologies mentioned in job descriptions. It includes:

* Splitting the technologies into separate rows.
* Grouping technologies by experience levels.
* Counting occurrences of each technology.
* Visualizing the top technologies using bar charts.

## Word Cloud
A word cloud is generated from the technologies mentioned in the job descriptions to provide a visual representation of their frequency.

## Contact
For any inquiries, please contact [vladislav.tsybuliak@gmail.com](mailto:vladislav.tsybuliak@gmail.com).

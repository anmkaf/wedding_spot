# Wedding Spot Scraper

This Scrapy project scrapes venue data from [Wedding Spot](https://www.wedding-spot.com) and saves it in a CSV file.

## Setup and Run

Follow these steps to set up and run the project:

### 1. Create Project Folder
```bash
mkdir scrapandey
cd scrapandey
```

### 2. Create Virtual Environment
```bash
python3 -m venv scrape
```

### 3. Activate Virtual Environment

#### On macOS/Linux:
```bash
source scrape/bin/activate
```

#### On Windows:
```bash
scrape\Scripts\activate
```

### 4. Install Scrapy
```bash
pip install scrapy
```

### 5. Create Scrapy Project
```bash
scrapy startproject wedding_spot
cd wedding_spot
```

### 6. Generate Spider
```bash
scrapy genspider venues www.wedding-spot.com
```

### 7. Run the Spider
```bash
scrapy crawl venues -o output.csv
```

## Output
The scraped data will be saved in `output.csv` in the project folder.

## Project Structure
```
scrapandey/
├── scrape/                   # Virtual environment
├── wedding_spot/             # Scrapy project
│   ├── wedding_spot/         # Project module
│   │   ├── spiders/          # Spiders directory
│   │   │   └── venues.py     # Spider for Wedding Spot
│   │   ├── items.py          # Data structure definitions
│   │   ├── pipelines.py      # Data processing pipelines
│   │   ├── settings.py       # Project settings
│   │   └── ...
│   └── scrapy.cfg            # Scrapy configuration file
```


## Deactivating the Virtual Environment
To exit the virtual environment, run:
```bash
deactivate
```

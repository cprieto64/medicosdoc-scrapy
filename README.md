## MedicosDoc Scraper

This is a Scrapy spider designed to extract data about doctors from the website medicosdoc.com.

### Inputs

- **Start URLs:** The spider begins scraping from a list of provided URLs. By default, it starts from `https://medicosdoc.com/categoria/instituciones-barranquilla` but can be modified in the `start_urls` variable.
- **MongoDB Connection:** The spider connects to a MongoDB database to store scraped data. The connection details (host, port, username, password, database name) are specified in the script. 

### Outputs

- **MongoDB Collection:** The spider saves scraped data to a MongoDB collection named `instituciones-scrapeops`. Each doctor is represented as a document with the following fields:
    - `doctor_id`: A unique ID generated from the doctor's name using a MD5 hash.
    - `nombre`: The doctor's name.
    - `telefono`: A list of phone numbers associated with the doctor.
    - `especializacion`: A list of the doctor's specializations.
    - `seguro`: The insurance accepted by the doctor, if available.
    - `direccion`: The doctor's address.
    - `source`: The URL from which the doctor's information was scraped.

### Usage

1. **Install Dependencies:** Ensure that all required Python packages are installed, including `Scrapy`, `pymongo`, and `requests`.
2. **Configure MongoDB Connection:** Update the MongoDB connection details in the script to match your specific MongoDB setup.
3. **Run the Spider:** Execute the command `scrapy runspider medicos_spider.py` to start the scraping process. The spider will traverse the website, extract doctor data, and store it in the MongoDB collection.
4. **Monitor the Process:** The spider logs errors to the console. You can check the log messages to monitor the scraping process and identify any issues.

### Notes

- The spider utilizes `Scrapy-UserAgents` and `scrapy_proxy_pool` to manage user agents and proxies, respectively, for improved scraping performance and bypass detection.
- The spider uses `ScrapeOps` for monitoring and rotating proxies.
- The spider has a limit of 50 pages to scrape. This can be changed in the `CLOSESPIDER_PAGECOUNT` setting.
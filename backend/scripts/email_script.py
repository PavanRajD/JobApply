import sys

def main(job_title, location):
    # Your scraping and email sending logic here
    print(f"Running script for job title: {job_title} in location: {location}")

if __name__ == "__main__":
    job_title = sys.argv[1]
    location = sys.argv[2]
    main(job_title, location)

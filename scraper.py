import aiohttp # run pip install aiohttp to install
from bs4 import BeautifulSoup # run pip install bs4 to install
import asyncio
import json

# Single request
url = "https://www.tiktok.com/@therock"
proxy = "my_rotating_proxy_url_here" # Enter your entire proxy URL - authentication and all.
async with aiohttp.ClientSession() as session:
    async with session.get(url, proxy=proxy) as response:
        text = await response.text()

soup = BeautifulSoup(text) # Parse the HTML
script_tag = soup.select_one("script#SIGI_STATE") # Select the SIGI_STATE tag
tag_contents = script_tag.contents[0] # Extract the contents
sigi_json = json.loads(tag_contents) # Load it into a python dictionary
profile_data = sigi_json.get("UserModule")


#  Running concurrent requests
async def scrape_profile(username: str):
    """Scrape a single TikTok profile by username"""
    url = "https://tiktok.com/@" + username
    for i in range(5):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy=proxy) as response:
                    text = await response.text()
                    soup = BeautifulSoup(text) 
                    script_tag = soup.select_one("script#SIGI_STATE") 
                    tag_contents = script_tag.contents[0] 
                    sigi_json = json.loads(tag_contents) 
                    return sigi_json.get("UserModule")
        except Exception as e:
            print(f"Request {i} failed with error {str(e)}")
            continue

async def main():
    """Function from which we call our scraping function"""
    usernames = ["therock", "nyjah.huston", "kingrygarcia", "codescope", "khabylame"]
    tasks = [asyncio.create_task(scrape_profile(user)) for user in usernames] # Create scrape_profile() task for each profile in our list of usernames.
    results = asyncio.gather(*tasks, return_exceptions=True) # Get the results of the tasks
    return [res for res in results if not isinstance(res, Exception)] # Return the results of the data that did not cause an exception

data = asyncio.run(main)
with open("output_file.json", "w") as f:
    json.dump(data, f)

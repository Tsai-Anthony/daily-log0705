import discord
import asyncio
from bs4 import BeautifulSoup
import requests

# Discord bot setup
client = discord.Client()
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    # Run the scraping loop initially
    await scrape_and_send()
    # Schedule the scraping loop to run every 24 hours
    while True:
        await asyncio.sleep(24 * 60 * 60)  # 24 hours
        await scrape_and_send()

async def scrape_and_send():
    # Web scraping setup
    keyword = "test automation engineer"
    url = f"https://www.indeed.com/jobs?q={keyword}&sort=date"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Scrape job listings
    job_listings = []
    for listing in soup.find_all(class_="jobsearch-SerpJobCard"):
        title = listing.find(class_="title").get_text(strip=True)
        company = listing.find(class_="company").get_text(strip=True)
        link = "https://www.indeed.com" + listing.find("a", class_="jobtitle")["href"]
        job_listings.append(f"**{title}**\nCompany: {company}\n[Apply here]({link})\n")

    # Send job listings to Discord channel
    channel_id = YOUR_DISCORD_CHANNEL_ID
    channel = client.get_channel(channel_id)
    message = "\n\n".join(job_listings)
    await channel.send(message)

# Run the bot
client.run(TOKEN)

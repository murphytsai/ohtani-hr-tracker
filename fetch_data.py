import json
import urllib.request
import pandas as pd

# MLB API endpoint for Ohtani's HRs
# Shohei Ohtani MLBAM ID: 660271
OHTANI_ID = 660271

def fetch_ohtani_hrs():
    url = f"https://statsapi.mlb.com/api/v1/people/{OHTANI_ID}/stats?stats=gameLog&group=hitting&gameType=R&season=2018&season=2019&season=2020&season=2021&season=2022&season=2023&season=2024&season=2025&season=2026"
    print("Fetching MLB API data...")
    # We can also fetch play-by-play or statcast search for pitch-by-pitch HR details.
    
if __name__ == '__main__':
    fetch_ohtani_hrs()

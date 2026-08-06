import concurrent.futures
import requests
import json
import time

OHTANI_ID = 660271
SEASONS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]

def fetch_game_pbp(g, season):
    game_pk = g['game']['gamePk']
    game_date = g['date']
    team = g['team']['name']
    opponent = g['opponent']['name']
    
    pbp_url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
    try:
        pbp_res = requests.get(pbp_url, timeout=10).json()
    except Exception as e:
        print(f"Error fetching gamePk {game_pk}: {e}", flush=True)
        return []
        
    all_plays = pbp_res.get('liveData', {}).get('plays', {}).get('allPlays', [])
    hrs_in_game = []
    
    for play in all_plays:
        batter_id = play.get('matchup', {}).get('batter', {}).get('id')
        event = play.get('result', {}).get('event', '')
        
        if batter_id == OHTANI_ID and event == 'Home Run':
            pitcher_name = play.get('matchup', {}).get('pitcher', {}).get('fullName', 'Unknown Pitcher')
            pitcher_id = play.get('matchup', {}).get('pitcher', {}).get('id')
            pitcher_hand = play.get('matchup', {}).get('pitchHand', {}).get('code', 'R')
            
            inning = play.get('about', {}).get('inning')
            half_inning = play.get('about', {}).get('halfInning')
            half_str = "Top" if half_inning == "top" else "Bot"
            
            rbi = play.get('result', {}).get('rbi', 1)
            hr_type = "Solo" if rbi == 1 else (f"{rbi}-Run" if rbi < 4 else "Grand Slam")
            
            # Pitch details
            play_events = play.get('playEvents', [])
            pitch_events = [p for p in play_events if p.get('isPitch', False)]
            last_pitch = pitch_events[-1] if pitch_events else {}
            
            pitch_type = last_pitch.get('details', {}).get('type', {}).get('description', 'N/A')
            pitch_speed = last_pitch.get('pitchData', {}).get('startSpeed', None)
            
            hit_data = last_pitch.get('hitData', {})
            launch_speed = hit_data.get('launchSpeed', None)
            launch_angle = hit_data.get('launchAngle', None)
            distance = hit_data.get('totalDistance', None)
            
            count_obj = play.get('count', {})
            count_str = f"{count_obj.get('balls', 0)}-{count_obj.get('strikes', 0)}"
            
            hrs_in_game.append({
                'date': game_date,
                'year': season,
                'team': team,
                'opponent': opponent,
                'inning': f"{half_str} {inning}",
                'pitcher_id': pitcher_id,
                'pitcher_name': pitcher_name,
                'pitcher_hand': pitcher_hand,
                'pitch_type': pitch_type,
                'pitch_speed': round(pitch_speed, 1) if pitch_speed else None,
                'exit_velocity': round(launch_speed, 1) if launch_speed else None,
                'launch_angle': round(launch_angle, 1) if launch_angle else None,
                'distance': round(distance) if distance else None,
                'count': count_str,
                'rbi': rbi,
                'hr_type': hr_type
            })
    return hrs_in_game

def fetch_all_hrs():
    all_games = []
    
    for season in SEASONS:
        print(f"Fetching game logs for season {season}...", flush=True)
        url = f"https://statsapi.mlb.com/api/v1/people/{OHTANI_ID}/stats?stats=gameLog&group=hitting&gameType=R&season={season}"
        res = requests.get(url).json()
        
        stats = res.get('stats', [])
        if not stats or 'splits' not in stats[0]:
            print(f"No splits found for season {season}", flush=True)
            continue
            
        splits = stats[0]['splits']
        hr_games = [s for s in splits if s['stat'].get('homeRuns', 0) > 0]
        print(f"Season {season}: {len(hr_games)} games with HRs", flush=True)
        for g in hr_games:
            all_games.append((g, season))
            
    print(f"Total games to fetch across all seasons: {len(all_games)}. Fetching concurrently...", flush=True)
    
    all_hrs = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_game_pbp, g, season) for g, season in all_games]
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                all_hrs.extend(res)
                
    # Sort all HRs chronologically by date
    all_hrs.sort(key=lambda x: x['date'])
    
    # Calculate career HR number and season HR number
    year_counters = {}
    for idx, hr in enumerate(all_hrs, start=1):
        hr['hr_num'] = idx
        yr = hr['year']
        year_counters[yr] = year_counters.get(yr, 0) + 1
        hr['season_hr_num'] = year_counters[yr]
        
    print(f"Total HRs fetched: {len(all_hrs)}", flush=True)
    
    with open('ohtani_hrs_mlb.json', 'w', encoding='utf-8') as f:
        json.dump(all_hrs, f, ensure_ascii=False, indent=2)
        
    print("Saved ohtani_hrs_mlb.json successfully!", flush=True)

if __name__ == '__main__':
    fetch_all_hrs()

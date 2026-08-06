import subprocess
import datetime
import os

def update_job():
    print(f"[{datetime.datetime.now()}] Starting scheduled Ohtani HR update...")
    try:
        # Step 1: Fetch newest Statcast HR data
        res1 = subprocess.run(["python3", "generate_data.py"], capture_output=True, text=True)
        print("Data Sync Output:", res1.stdout)
        
        # Step 2: Copy to main JSON
        if os.path.exists("ohtani_hrs.json"):
            with open("ohtani_hrs.json", "r") as f_in:
                content = f_in.read()
            with open("ohtani_hrs_mlb.json", "w") as f_out:
                f_out.write(content)
                
        # Step 3: Rebuild HTML Dashboard
        res2 = subprocess.run(["python3", "build_web.py"], capture_output=True, text=True)
        print("Web Build Output:", res2.stdout)
        print(f"[{datetime.datetime.now()}] Update completed successfully!")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] Error updating Ohtani HR data: {e}")

if __name__ == '__main__':
    update_job()

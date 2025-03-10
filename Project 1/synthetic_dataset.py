import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Setting random seed for reproducibility
np.random.seed(42)

def generate_time(target_hour, std_dev_minutes=30):
    """
    Function to generate random time with normal distribution around a target hour

    Args:
        target_hour (int): Target hour for the generated time
        std_dev_minutes (int): Standard deviation for the normal distribution
    
    Returns:
        generated_time (str): Random time in HH:MM format
    """
    # Generating time around target hour
    base_time = datetime.strptime(f"{target_hour}:00", "%H:%M")
    # Adding random variation to the time
    variation = np.random.normal(0, std_dev_minutes)

    generated_time = (base_time + timedelta(minutes=variation)).strftime("%H:%M")

    return generated_time

# Setting 1000 samples for the dataset
n_samples = 1000
data = []

for _ in range(n_samples):
    # Generating wake-up times between 5:00 and 9:00
    wake_hour = np.random.uniform(5, 9)
    wake_time = generate_time(int(wake_hour), std_dev_minutes=30)

    # Calculating ideal bedtime (assuming ~8 hours of sleep)
    wake_datetime = datetime.strptime(wake_time, "%H:%M")
    bedtime_datetime = wake_datetime - timedelta(hours=8)

    # Adding some natural variation to recommended sleep duration (7.5-8.5 hours)
    sleep_variation = np.random.uniform(-0.5, 0.5)
    bedtime_datetime = bedtime_datetime + timedelta(hours=sleep_variation)

    # Formatting bedtime
    if bedtime_datetime.day != wake_datetime.day:
        # If bedtime is previous day, use 24-hour format
        bedtime = bedtime_datetime.strftime("%H:%M")
    else:
        bedtime = bedtime_datetime.strftime("%H:%M")

    # Adding quality score (higher for more natural sleep patterns)
    quality_score = 100 - abs(wake_datetime.hour + wake_datetime.minute/60 - 7) * 5  # Optimal wake time around 7 AM
    quality_score = max(min(quality_score, 100), 60)  # Limit scores between 60 and 100

    data.append({
        'wake_time': wake_time,
        'recommended_bedtime': bedtime,
        'sleep_quality_score': round(quality_score, 2)
    })

# Creating DataFrame
df = pd.DataFrame(data)

# Sorting by wake_time for better readability
df = df.sort_values('wake_time').reset_index(drop=True)

# Saving to a CSV file
df.to_csv('sleep_patterns.csv', index=False)

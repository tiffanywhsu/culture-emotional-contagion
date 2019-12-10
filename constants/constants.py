"""Define constants to be used throughout repo"""
import numpy as np
import pandas as pd
from pathlib import Path


# project directories
PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# calculate_exposure constants
TIMESAMPLES = 50
TIMELAPSE = np.timedelta64(1, 'h')

# collection times
US_COLLECTION_TIMES = ["12.19.18.6pm", "12.13.18.7pm", "12.11.18.11pm",
                       "12.5.18.5pm", "12.3.18.12am", "11.29.18.12am",
                       "11.16.18.10pm", "11.8.18.10am", "11.6.18.3pm",
                       "11.3.18.3pm", "11.1.18.7pm", "10.29.18.7pm",
                       "10.28.18.4pm", "1.11.19.4pm", "1.8.19.10pm",
                       "1.6.19.11pm"]

JP_COLLECTION_TIMES = ["12.14.18.12pm", "12.12.18.4pm", "12.6.18.10am",
						"11.29.18.5pm", "11.17.18.3pm", "11.9.18.4am",
						"11.7.18.8am", "11.4.18.4pm", "11.2.18.11am",
						"10.30.18.11am", "1.12.19.9am", "1.9.19.3pm",
						"1.7.19.4pm"]

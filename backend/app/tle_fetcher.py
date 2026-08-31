import os
import httpx
from typing import List, Tuple
from dotenv import load_dotenv

load_dotenv()

def fetch_tle_data() -> List[Tuple[str, str, str, str]]:
    """
    Fetch TLE data from CelesTrak. If it fails or DEMO_MODE=true,
    returns hardcoded demo TLE data.
    """
    demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    
    if not demo_mode:
        try:
            results = []
            urls = [
                "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle",
                "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
            ]
            for url in urls:
                response = httpx.get(url, timeout=10.0)
                if response.status_code == 200:
                    lines = response.text.strip().split("\n")
                    # Limit to 50
                    count = 0
                    for i in range(0, len(lines), 3):
                        if count >= 50:
                            break
                        if i+2 < len(lines):
                            name = lines[i].strip()
                            line1 = lines[i+1].strip()
                            line2 = lines[i+2].strip()
                            results.append((name, line1, line2, "PAYLOAD"))
                            count += 1
            if results:
                return results
        except Exception as e:
            print(f"Failed to fetch TLE data: {e}")

    # Fallback to Demo TLEs (2026 epoch)
    return [
        # Active Payloads
        ("ISS (ZARYA)",
         "1 25544U 98067A   26243.50000000  .00016717  00000-0  30000-3 0  9997",
         "2 25544  51.6401 123.4567 0004567  12.3456 123.4567 15.50000000123456",
         "PAYLOAD"),
        ("STARLINK-1007",
         "1 44713U 19074A   26243.50000000  .00001000  00000-0  50000-4 0  9999",
         "2 44713  53.0500 123.4567 0001234  12.3456 123.4567 15.06000000123456",
         "PAYLOAD"),
        ("STARLINK-2305",
         "1 47913U 21024A   26243.50000000  .00001000  00000-0  50000-4 0  9999",
         "2 47913  53.0500 234.5678 0001234  12.3456 123.4567 15.06000000123456",
         "PAYLOAD"),
        ("HUBBLE SPACE TELESCOPE",
         "1 20580U 90037B   26243.50000000  .00001200  00000-0  60000-4 0  9991",
         "2 20580  28.4700 280.1234 0002345  45.6789 314.3210 15.09000000123456",
         "PAYLOAD"),
        ("TIANGONG",
         "1 48274U 21035A   26243.50000000  .00015000  00000-0  27000-3 0  9994",
         "2 48274  41.4700 210.5678 0006123  89.1234 271.0000 15.61000000123456",
         "PAYLOAD"),
        ("SENTINEL-6A",
         "1 46984U 20089A   26243.50000000  .00000200  00000-0  10000-4 0  9998",
         "2 46984  66.0000 312.4567 0001100  98.7654 261.3456 13.74000000123456",
         "PAYLOAD"),
        ("LANDSAT-9",
         "1 49260U 21088A   26243.50000000  .00000150  00000-0  80000-5 0  9997",
         "2 49260  98.2200  47.8901 0001456 108.2345 251.9012 14.57000000123456",
         "PAYLOAD"),
        ("NOAA-20",
         "1 43013U 17073A   26243.50000000  .00000100  00000-0  50000-5 0  9992",
         "2 43013  98.7400 162.3456 0001234 135.6789 224.4321 14.19000000123456",
         "PAYLOAD"),
        # Space Debris
        ("COSMOS 2251 DEB",
         "1 33751U 93036F   26243.50000000  .00001000  00000-0  50000-4 0  9999",
         "2 33751  74.0000 123.4567 0001234  12.3456 123.4567 14.50000000123456",
         "DEBRIS"),
        ("FENGYUN 1C DEB",
         "1 30000U 99025A   26243.50000000  .00001000  00000-0  50000-4 0  9999",
         "2 30000  98.0000 123.4567 0001234  12.3456 123.4567 14.00000000123456",
         "DEBRIS"),
        ("IRIDIUM 33 DEB",
         "1 33752U 97051C   26243.50000000  .00001000  00000-0  50000-4 0  9999",
         "2 33752  86.0000 123.4567 0001234  12.3456 123.4567 14.30000000123456",
         "DEBRIS"),
        # Rocket Bodies
        ("SL-8 R/B",
         "1 20000U 89001A   26243.50000000  .00001000  00000-0  50000-4 0  9999",
         "2 20000  82.0000 123.4567 0001234  12.3456 123.4567 13.90000000123456",
         "ROCKET_BODY")
    ]

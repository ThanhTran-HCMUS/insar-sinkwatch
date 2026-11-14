"""
NASA ASF DAAC Open SAR Data Query Tool
Directly interfaces with NASA's Alaska Satellite Facility Vertex API
Allows searching, filtering, and retrieving open SAR/NISAR metadata for Vietnam coordinates.
"""

import urllib.request
import urllib.parse
import json

def query_nasa_asf_sar_granules(
    min_lon: float = 106.60,
    min_lat: float = 10.68,
    max_lon: float = 106.85,
    max_lat: float = 10.88,
    start_date: str = "2024-01-01",
    end_date: str = "2024-12-31",
    max_results: int = 5
) -> list:
    """
    Queries NASA Alaska Satellite Facility (ASF DAAC) REST API
    for SAR satellite scenes covering the designated area of interest.
    
    API Endpoint: https://api.daac.asf.alaska.edu/services/search/param
    """
    # WKT Polygon format for geographic search
    polygon_wkt = f"POLYGON(({min_lon} {min_lat}, {max_lon} {min_lat}, {max_lon} {max_lat}, {min_lon} {max_lat}, {min_lon} {min_lat}))"
    
    params = {
        "intersectsWith": polygon_wkt,
        "platform": "SENTINEL-1",
        "processingLevel": "SLC",  # Single Look Complex for InSAR
        "start": start_date,
        "end": end_date,
        "output": "json",
        "maxResults": str(max_results)
    }
    
    query_string = urllib.parse.urlencode(params)
    api_url = f"https://api.daac.asf.alaska.edu/services/search/param?{query_string}"
    
    print(f"🛰️ Querying NASA ASF DAAC API: {api_url[:80]}...")
    
    req = urllib.request.Request(
        api_url,
        headers={"User-Agent": "NASA-SpaceApps-VisionSpace_UsxSgu"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            granules = data[0] if isinstance(data, list) and len(data) > 0 else []
            return granules
    except Exception as e:
        print(f"⚠️ Note: Direct network query restricted or offline. ({e})")
        return []

if __name__ == "__main__":
    print("Testing NASA ASF DAAC Query Module...")
    results = query_nasa_asf_sar_granules(max_results=3)
    print(f"Returned {len(results)} granules from NASA ASF repository.")

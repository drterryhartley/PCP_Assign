import pandas as pd
import random
import numpy as np
from geopy.distance import geodesic

# Haversine function to calculate distance between two lat/long points
def haversine(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).miles

# Function to check if an address (latitude, longitude) is within Texas
def is_within_texas(lat, lon):
    # Texas latitude and longitude ranges
    texas_lat_range = (25.83, 36.5)
    texas_lon_range = (-106.65, -93.51)
    
    return texas_lat_range[0] <= lat <= texas_lat_range[1] and texas_lon_range[0] <= lon <= texas_lon_range[1]

# Generate sample member data with latitude and longitude
members = pd.DataFrame({
    'member_id': [f'M{str(i).zfill(3)}' for i in range(1, 21)],
    'age': [random.randint(18, 65) for _ in range(20)],
    'gender': [random.choice(['Male', 'Female', 'Other']) for _ in range(20)],
    'ethnicity': [random.choice(['Hispanic', 'Non-Hispanic White', 'Black', 'Asian']) for _ in range(20)],
    'location': [random.choice(['Urban', 'Suburban', 'Rural']) for _ in range(20)],
    'lat': [random.uniform(29.0, 30.0) if random.random() > 0.1 else random.uniform(10.0, 20.0) for _ in range(20)],  # Some bad latitudes outside Texas
    'lon': [random.uniform(-99.0, -97.0) if random.random() > 0.1 else random.uniform(-120.0, -110.0) for _ in range(20)], # Some bad longitudes outside Texas
    'previous_pcp_rating': [random.uniform(1, 5) for _ in range(20)]
})

# Generate sample PCP data with latitude and longitude and panel size
pcps = pd.DataFrame({
    'pcp_id': [f'P{str(i).zfill(3)}' for i in range(1, 11)],
    'specialization': [random.choice(['General Practice', 'Pediatrics', 'Family Medicine']) for _ in range(10)],
    'min_age': [random.randint(18, 40) for _ in range(10)],
    'max_age': [random.randint(50, 80) for _ in range(10)],
    'gender_pref': [random.choice(['Male', 'Female', 'Any']) for _ in range(10)],
    'ethnicity_pref': [random.choice(['Hispanic', 'Non-Hispanic White', 'Black', 'Asian', 'Any']) for _ in range(10)],
    'location_served': [random.choice(['Urban', 'Suburban', 'Rural']) for _ in range(10)],
    'performance_score': [random.uniform(1, 5) for _ in range(10)],
    'accepting_new_patients': [random.choice([True, False]) for _ in range(10)],
    'current_panel_size': [random.randint(0, 100) for _ in range(10)],  # Current number of patients
    'panel_limit': [random.randint(80, 120) for _ in range(10)],  # Max number of patients
    'lat': [random.uniform(29.0, 30.0) if random.random() > 0.1 else random.uniform(10.0, 20.0) for _ in range(10)],  # Some bad latitudes outside Texas
    'lon': [random.uniform(-99.0, -97.0) if random.random() > 0.1 else random.uniform(-120.0, -110.0) for _ in range(10)] # Some bad longitudes outside Texas
})

# Convert categorical columns to numerical values
def preprocess_data(members, pcps):
    gender_map = {'Male': 0, 'Female': 1, 'Other': 2, 'Any': -1}
    ethnicity_map = {'Hispanic': 0, 'Non-Hispanic White': 1, 'Black': 2, 'Asian': 3, 'Any': -1}
    location_map = {'Urban': 0, 'Suburban': 1, 'Rural': 2}
    
    members['gender_num'] = members['gender'].map(gender_map)
    members['ethnicity_num'] = members['ethnicity'].map(ethnicity_map)
    members['location_num'] = members['location'].map(location_map)
    
    pcps['gender_pref_num'] = pcps['gender_pref'].map(gender_map)
    pcps['ethnicity_pref_num'] = pcps['ethnicity_pref'].map(ethnicity_map)
    pcps['location_served_num'] = pcps['location_served'].map(location_map)
    
    return members, pcps

# Preprocess data
members, pcps = preprocess_data(members, pcps)

# Define a distance function that accounts for criteria match and geography
def custom_distance(member, pcp):
    # Calculate geographic distance
    distance = haversine(member['lat'], member['lon'], pcp['lat'], pcp['lon'])
    
    # Check panel restrictions (accepting new patients and panel size)
    if not pcp['accepting_new_patients'] or pcp['current_panel_size'] >= pcp['panel_limit']:
        return float('inf')
    
    # Age, gender, ethnicity match
    age_match = pcp['min_age'] <= member['age'] <= pcp['max_age']
    gender_match = pcp['gender_pref_num'] == -1 or pcp['gender_pref_num'] == member['gender_num']
    ethnicity_match = pcp['ethnicity_pref_num'] == -1 or pcp['ethnicity_pref_num'] == member['ethnicity_num']
    location_match = pcp['location_served_num'] == member['location_num']
    
    # Penalize mismatches by adding large values
    if not age_match:
        distance += 1000
    if not gender_match:
        distance += 1000
    if not ethnicity_match:
        distance += 1000
    if not location_match:
        distance += 1000
    
    # Use PCP's performance score as part of the distance (better scores = closer)
    distance += (5 - pcp['performance_score'])  # Higher performance score is better
    
    return distance

# Assign each member to the best matching PCP with panel restrictions
def assign_pcp_to_members(members, pcps):
    assignments = []
    exception_status = []
    
    for i, member in members.iterrows():
        # Check if the member's address is valid (within Texas)
        if not is_within_texas(member['lat'], member['lon']):
            assignments.append('Invalid Address')
            exception_status.append(f"Member {member['member_id']} has an invalid address")
            continue
        
        best_pcp = None
        best_distance = float('inf')
        
        for j, pcp in pcps.iterrows():
            # Check if the PCP's address is valid (within Texas)
            if not is_within_texas(pcp['lat'], pcp['lon']):
                exception_status.append(f"PCP {pcp['pcp_id']} has an invalid address")
                continue
            
            dist = custom_distance(member, pcp)
            if dist < best_distance:
                best_distance = dist
                best_pcp = pcp['pcp_id']
        
        if best_pcp:
            assignments.append(best_pcp)
        else:
            assignments.append('No Match')
    
    return assignments, exception_status

# Perform the assignment
members['assigned_pcp'], exceptions = assign_pcp_to_members(members, pcps)

# Display the assignments and exceptions
print("\nMember Assignments:\n", members[['member_id', 'assigned_pcp']])
print("\nExceptions:\n", exceptions)

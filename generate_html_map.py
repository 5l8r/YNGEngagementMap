import pandas as pd
import folium
from folium.plugins import MarkerCluster
import random

def generate_html_map(df, output_html_file, chapter_filter=None, interest_filter=None, industry_filter=None):
    # Filter data based on chapter, interest, and industry
    if chapter_filter and chapter_filter != 'Pacific US Region':
        df = df[df['Chapter Affiliation'] == chapter_filter]
    
    if interest_filter and interest_filter != 'Any':
        df = df[df['Interests'].str.contains(interest_filter, na=False)]

    if industry_filter and industry_filter != 'Any':
        df = df[df['Industry'] == industry_filter]

    # Ensure no NaN values in location columns
    df = df.dropna(subset=['Latitude', 'Longitude'])

    # Determine the center and zoom level
    if not df.empty:
        min_lat, max_lat = df['Latitude'].min(), df['Latitude'].max()
        min_lon, max_lon = df['Longitude'].min(), df['Longitude'].max()
        center = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]

        if len(df) == 1:
            zoom_start = 12
        else:
            bounds = [[min_lat, min_lon], [max_lat, max_lon]]
            distance_lat = max_lat - min_lat
            distance_lon = max_lon - min_lon
            max_distance = max(distance_lat, distance_lon)

            # Adjust zoom level based on the maximum distance between points
            if max_distance < 0.01:
                zoom_start = 15
            elif max_distance < 0.1:
                zoom_start = 14
            elif max_distance < 1:
                zoom_start = 12
            elif max_distance < 10:
                zoom_start = 10
            elif max_distance < 20:
                zoom_start = 8
            else:
                zoom_start = 6
                center = (37.0902, -95.7129)  # Default to the center of the Pacific US Region
    else:
        center = (37.0902, -95.7129)
        zoom_start = 6

    # Create the base map
    map_ = folium.Map(
        location=center,
        zoom_start=zoom_start,
        tiles="CartoDB positron"
    )

    if 'bounds' in locals() and max_distance < 20:
        map_.fit_bounds(bounds)

    if df.empty:
        # Just display an empty map
        pass
    else:
        # Create marker cluster with custom icon creation function
        marker_cluster = MarkerCluster(
            icon_create_function="""
                function(cluster) {
                    var count = cluster.getChildCount();
                    var color = 'rgba(116, 185, 65, 1)';  // Green by default
                    if (count >= 50) {
                        color = 'rgba(240, 85, 101, 1)';  // Red
                    } else if (count >= 25) {
                        color = 'rgba(30, 128, 195, 1)';  // Blue
                    } else if (count > 1) {
                        color = 'rgba(225, 163, 38, 1)';  // Yellow
                    }
                    return L.divIcon({
                        html: '<div style="background-color:' + color + '; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; color: white;">' + count + '</div>',
                        className: 'marker-cluster'
                    });
                }
            """).add_to(map_)

        for index, row in df.iterrows():
            popup_text = f"""
            <div style="font-family:'Montserrat',sans-serif; font-size:12px; width:250px; padding:10px; background-color:#f9f9f9; border-radius:5px; box-shadow:0 0 10px rgba(0,0,0,0.1);">
                <b>Name:</b> {row['Name']}<br>
                <b>Chapter Affiliation:</b> {row['Chapter Affiliation']}<br>
                <b>Interests:</b> {row['Interests']}<br>
                <b>Industry:</b> {row['Industry']}<br>
                {"<b>LinkedIn:</b> Request Needed to Access<br>" if row['LinkedIn'] == 'NP' else f"<a href='https://linkedin.com/in/{row['LinkedIn']}'>LinkedIn</a><br>"}
                {"<b>Instagram:</b> Request Needed to Access<br>" if row['Instagram'] == 'NP' else f"<a href='https://instagram.com/{row['Instagram']}'>Instagram</a><br>"}
                {"<b>Phone Number:</b> Request Needed to Access<br>" if row['Phone Number'] == 'NP' else f"<b>Phone Number:</b> {row['Phone Number']}<br>"}
                {"<b>Email:</b> Request Needed to Access<br>" if row['Email'] == 'NP' else f"<b>Email:</b> {row['Email']}<br>"}
                <form style="margin-top:10px;">
                    <p type="Your Name:"><input type="text" id="name" name="name" style="width:calc(50% - 12px); margin-right:12px; margin-bottom:5px; border:none;" placeholder="Your name.."></input><input type="tel" id="phone" name="phone" style="width:calc(50% - 12px); border:none;" placeholder="Your phone.."></input></p>
                    <p type="Your Email:"><input type="email" id="email" name="email" style="width:calc(50% - 12px); margin-right:12px; border:none;" placeholder="Your email.."></input><input type="text" id="linkedin" name="linkedin" style="width:calc(50% - 12px); border:none;" placeholder="Your LinkedIn.."></input></p>
                    <p type="Your Instagram:"><input type="text" id="instagram" name="instagram" style="width:calc(50% - 12px); margin-right:12px; border:none;" placeholder="Your Instagram.."></input></p>
                    <p type="Your Note:"><textarea id="note" name="note" maxlength="400" style="width:100%; border:none;" placeholder="Your note.."></textarea></p>
                    <button type="submit" style="width:100%; padding:8px; background:#78788c; color:white; border:none; border-radius:3px;">Request</button>
                </form>
            </div>
            """


            if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
                # Add a larger random offset to each marker to avoid overlap
                offset_lat = row['Latitude'] + random.uniform(-0.005, 0.005)
                offset_lon = row['Longitude'] + random.uniform(-0.005, 0.005)
                
                folium.CircleMarker(
                    location=[offset_lat, offset_lon],
                    radius=5,
                    color='rgba(116, 185, 65, 1)',  # Green color
                    fill=True,
                    fill_color='rgba(116, 185, 65, 1)',  # Green color
                    fill_opacity=1.0,
                    popup=popup_text,
                    tooltip=row['Name']
                ).add_to(marker_cluster)
            else:
                print(f"Skipping {row['Name']} due to missing coordinates.")

    map_.save(output_html_file)
    print(f"Map has been created and saved as '{output_html_file}'")
    return not df.empty

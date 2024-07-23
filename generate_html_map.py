import pandas as pd
import folium
from folium.plugins import MarkerCluster
import random

def generate_html_map(df, output_html_file, center=(37.0902, -95.7129), zoom_start=4, chapter_filter=None, zip_code_filter=None):
    # Filter data based on chapter and zip code
    if chapter_filter:
        df = df[df['Chapter Affiliation'] == chapter_filter]

    if zip_code_filter:
        df = df[df['Zip Code'] == zip_code_filter]

    if not df.empty:
        # Calculate the bounds of the filtered data
        min_lat, max_lat = df['Latitude'].min(), df['Latitude'].max()
        min_lon, max_lon = df['Longitude'].min(), df['Longitude'].max()
        bounds = [[min_lat, min_lon], [max_lat, max_lon]]
        center = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]
        
        # Calculate zoom level based on distance between the points
        distance_lat = max_lat - min_lat
        distance_lon = max_lon - min_lon
        max_distance = max(distance_lat, distance_lon)

        if max_distance < 0.01:
            zoom_start = 14
        elif max_distance < 0.1:
            zoom_start = 12
        elif max_distance < 1:
            zoom_start = 10
        elif max_distance < 2:
            zoom_start = 8
        else:
            zoom_start = 6
    else:
        # Default to the entire US
        bounds = [[24.396308, -125.0], [49.384358, -66.93457]]
        center = (37.0902, -95.7129)
        zoom_start = 4

    # Create the base map with restricted bounds
    map_ = folium.Map(
        location=center,
        zoom_start=zoom_start,
        tiles="CartoDB positron",
        max_bounds=True
    )
    map_.fit_bounds(bounds)

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
        <b>Name:</b> {row['Name']}<br>
        <b>Chapter Affiliation:</b> {row['Chapter Affiliation']}<br>
        """

        if row['LinkedIn'] != 'NP':
            if row['LinkedIn Public'] == 'yes':
                popup_text += f"<a href='https://linkedin.com/in/{row['LinkedIn']}'>LinkedIn</a><br>"
            else:
                popup_text += "<b>LinkedIn:</b> Request Needed to Access<br>"

        if row['Instagram'] != 'NP':
            if row['Instagram Public'] == 'yes':
                popup_text += f"<a href='https://instagram.com/{row['Instagram']}'>Instagram</a><br>"
            else:
                popup_text += "<b>Instagram:</b> Request Needed to Access<br>"

        if row['Phone Number'] != 'NP':
            if row['Phone Number Public'] == 'yes':
                popup_text += f"<b>Phone Number:</b> {row['Phone Number']}<br>"
            else:
                popup_text += "<b>Phone Number:</b> Request Needed to Access<br>"

        if row['Email'] != 'NP':
            if row['Email Public'] == 'yes':
                popup_text += f"<b>Email:</b> {row['Email']}<br>"
            else:
                popup_text += "<b>Email:</b> Request Needed to Access<br>"

        if any(row[col] == 'no' for col in ['LinkedIn Public', 'Instagram Public', 'Phone Number Public', 'Email Public']):
            popup_text += """
            <form action="#" method="post">
                <label for="name">Your Name:</label><br>
                <input type="text" id="name" name="name"><br>
                <label for="email">Your Email:</label><br>
                <input type="email" id="email" name="email"><br>
                <label for="phone">Your Phone Number:</label><br>
                <input type="tel" id="phone" name="phone"><br>
                <label for="linkedin">Your LinkedIn:</label><br>
                <input type="text" id="linkedin" name="linkedin"><br>
                <label for="instagram">Your Instagram:</label><br>
                <input type="text" id="instagram" name="instagram"><br>
                <input type="submit" value="Request">
            </form>
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

import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd


st.title("Philly Eats")

gif_html = """
<div style="position: absolute; top: 0; right: 0; margin-top: -130px;">  <!-- Adjusted margin-top to raise GIF by 30 pixels -->
    <iframe src="https://giphy.com/embed/x5wC9Udx9eUdeao5oE" width="180" height="180" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
</div>
"""
st.markdown(gif_html, unsafe_allow_html=True)


st.sidebar.header("Random Restaurant!")


st.sidebar.markdown("""
<div style="border: 2px solid black; padding: 10px; border-radius: 5px; background-color: #ADD8E6;">
    <p>1. Select your preferred cuisine from the dropdown menu. If you want a random option, leave it blank.</p>
    <p>2. Choose your budget from the cost dropdown.</p>
    <p>3. Press the button below to reveal a surprise restaurant location on the map.</p>
</div>
""", unsafe_allow_html=True)


csv_file_path = 'AddressesPhilly3.csv'
data = pd.read_csv(csv_file_path)


cuisine_options = data['Cuisine'].dropna().unique().tolist()
cuisine_input = st.sidebar.selectbox("Select Cuisine (Leave blank for random):", cuisine_options + [''])


cost_options = ['$', '$$', '$$$']
cost_input = st.sidebar.selectbox("Select Cost (Leave blank for random):", cost_options + [''])


def plot_points_on_map(data, cuisine_filter=None, cost_filter=None):
    data = data.dropna(subset=['Latitude', 'Longitude'])
    if cuisine_filter and cuisine_filter != '':
        data = data[data['Cuisine'].str.contains(cuisine_filter, case=False)]
    if cost_filter and cost_filter != '':
        data = data[data['Cost'] == cost_filter]

    if data.empty:
        return None, None

    restaurant = data.sample(1).iloc[0]
    m = folium.Map(location=[restaurant['Latitude'], restaurant['Longitude']], zoom_start=14)
    folium.Marker(
        location=[restaurant['Latitude'], restaurant['Longitude']],
        popup=f"{restaurant['Name']}<br>Cuisine: {restaurant['Cuisine']}<br>Cost: {restaurant['Cost']}<br>Address: {restaurant['Address']}",
        icon=folium.Icon(color='blue')
    ).add_to(m)
    return m, restaurant


gif_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExczI5aGY5dWpidWxtYjFjaGxieTgzcGoyeWo3NHlmZ3o3cnZkZDU4ciZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9dHM/39jMsjdFQ2BcHRXiBO/giphy.gif"
gif_placeholder = st.empty()
gif_placeholder.image(gif_url, width=600)


map_object, selected_restaurant = None, None

if st.sidebar.button('Reveal Surprise Location 🎀', key='reveal_button', help='Click to reveal a surprise location!'):
    map_object, selected_restaurant = plot_points_on_map(data, cuisine_filter=cuisine_input, cost_filter=cost_input)

    if selected_restaurant is None:
        st.sidebar.warning("No restaurants found, try again.")
    else:
        
        gif_placeholder.empty()  
        folium_static(map_object, width=800, height=500)  
        
        
        st.markdown(
            f"""
            <div style='text-align: center; border: 2px solid black; padding: 10px; border-radius: 5px; background-color: #ADD8E6;'>
                <h2 style='color: green;'>🎉 *Random Pick: {selected_restaurant['Name']}* 🎉</h2>
                <p><strong>Cuisine:</strong> {selected_restaurant['Cuisine']}</p>
                <p><strong>Cost:</strong> {selected_restaurant['Cost']}</p>
                <p><strong>Address:</strong> {selected_restaurant['Address']}</p>
                <p>Enjoy your meal! 🍽️</p>
            </div>
            """, unsafe_allow_html=True
        )



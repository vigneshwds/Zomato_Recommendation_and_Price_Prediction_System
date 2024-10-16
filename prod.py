import base64
import pandas as pd
import streamlit as st
import plotly.express as px

#-------------------------------------------------------------------------------------------

def main_file():
    zomato=pd.read_csv('new_decoded_df.csv')
    return zomato


def geograph(df):
    #st.subheader(f'Popular localities in and around {selected_country}')
    fig=px.scatter_mapbox(df, lon='Longitude', lat='Latitude',size='Aggregate_rating', color_continuous_scale='Rainbow', 
                          hover_name='Restaurant_name', range_color=(0,20), mapbox_style='open-street-map') #zoom=0.8
    fig.update_layout(width=1200,height=600,title=f'Popular localities in and around {selected_country}')
    st.plotly_chart(fig)

    st.markdown('**:red[Note :] Above Map shows our available restaurants across the country**')



def filter_on(df):
    unique_citys=df['City'].unique()
    unique_cuisines=df['Cuisines'].unique()

    col1,col2,col3=st.columns(3)
    with col1:
        selected_city=st.selectbox('**City**',options=unique_citys)
    with col2:
        selected_cuisines=st.selectbox('**Cuisines**',options=unique_cuisines)
    #with col4:
        #selected_price=st.selectbox('**Price Range**',[i for i in range(2, 5)])
    with col3:
        selected_rating=st.slider('**Rating**',3.0, 5.0)

    #filters
    f1=df['City']==selected_city
    f2=df['Cuisines']==selected_cuisines
    #f3=df['Price_range']==selected_price
    f3=df['Aggregate_rating']>=selected_rating

    filtered_df=df[f1 & f2 & f3]

    return filtered_df   



def top_restaurants(df,country):
    if not df.empty:
        st.subheader(f'Top Restaurant chains in {country}')
        num_columns = 2 
        num_rows = (len(df) + num_columns - 1) // num_columns  

        for row_index in range(num_rows):
            cols = st.columns(num_columns)  

            for col_index in range(num_columns):
                index = row_index * num_columns + col_index

                if index < len(df):  
                    row = df.iloc[index]  
                    with cols[col_index]:
                        st.subheader(row['Restaurant_name'])
                        st.markdown(f"[View More Info]({row['Photo_url']})") 
                        st.components.v1.html(f'<iframe src="{row["Photo_url"]}" width="400" height="400"></iframe>', height=300)
                        #st.markdown(f'**Ratings : {row['Aggregate_rating']}**')
                        display_rating(row['Aggregate_rating'])
                        st.markdown(f'**Average dinning Cost : {round(row['Average_cost_for_two'], 2)}**')
                        
    else:
        print('No Restaurants found for the selected critiria')
        st.markdown('**:red[Oops! there is no restaurants available for your request. Please try selecting other available options.]**')
        st.markdown(
    "<div style='text-align: center;'><img src='https://thumbs.dreamstime.com/b/oops-sign-18087812.jpg' width='300' /></div>",
    unsafe_allow_html=True)
        



def show_details(df, text):
    if not df.empty:
        st.subheader(text)
        num_columns = 2 
        num_rows = (len(df) + num_columns - 1) // num_columns  

        for row_index in range(num_rows):
            cols = st.columns(num_columns)  

            for col_index in range(num_columns):
                index = row_index * num_columns + col_index  

                if index < len(df):  
                    row = df.iloc[index]  
                    with cols[col_index]:
                        st.subheader(row['Restaurant_name'])
                        st.markdown(f"[View More Info]({row['Photo_url']})") 
                        st.components.v1.html(f'<iframe src="{row["Photo_url"]}" width="400" height="400"></iframe>', height=300)
                        display_rating(row['Aggregate_rating'])
                        #st.markdown(f'**Ratings : {row['Aggregate_rating']}**')
                        st.markdown(f'**Average dinning Cost : {round(row['Average_cost_for_two'], 2)}**')
    else:
        print('No Restaurants found for the selected critiria')  
        st.markdown('**:red[Oops! there is no restaurants available for your request. Please try selecting other available options.]**')
        st.markdown(
    "<div style='text-align: center;'><img src='https://thumbs.dreamstime.com/b/oops-sign-18087812.jpg' width='300' /></div>",
    unsafe_allow_html=True)      
        


def bar_chart(df):
    #Line chart - Price distribution
    line_graph=df[['City','Average_cost_for_two']]
    fig=px.line(line_graph, x='City', y='Average_cost_for_two', title='Price Trend')
    fig.update_traces(line=dict(color='grey'))
    st.plotly_chart(fig)

    #barChart
    fig=px.bar(df, x='City', y=['Is_delivering_now', 'Has_table_booking'], title='Delivery & Table Booking options',
               color_discrete_map={'Is_delivering_now': 'yellow', 'Has_table_booking': 'grey'})
    st.plotly_chart(fig)


def display_rating(rating):
    stars = "⭐" * int(rating) + "✰" * (5 - int(rating))
    return st.write(f"**:orange[Rating:] {stars} ({rating}/5)**")


def load_image(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


#--------------------------------------------------------------------------------------


#Main Program

if __name__=='__main__':

    # Load your local image file
    image_file = "home-banner3.jpg"  # Replace with your image filename
    image_data = load_image(image_file)

    # Load custom CSS to set the background image
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpg;base64,{image_data});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            height: 100vh;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )    


    sidebar_bg = """
    <style>
    [data-testid="stSidebar"] {
        background: url("https://github.com/andfanilo/social-media-tutorials/blob/master/20220817-streamlit_css_background/image.jpg?raw=true") no-repeat center center fixed;
        background-size: cover;
    }
    [data-testid="stSidebar"]::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }       
    </style>
    """

    # Apply the custom CSS to the sidebar
    st.markdown(sidebar_bg, unsafe_allow_html=True)

    st.title('Zomato Recommendation System')
    st.sidebar.title('**Zomato**')
    zom=main_file()
    unique_country=zom['Country'].unique()
    selected_country=st.sidebar.selectbox('**Country**',options=unique_country)
    st.markdown(
    f"<h3 style='text-align: center; color: red;'>Discover the best food & drinks in {selected_country}</h3>",
    unsafe_allow_html=True)
    filter1=zom[zom['Country']==selected_country]    

    st.subheader('Welcome to our Restaurant Locator!')

    #Location check box - Optional
    show_map=st.checkbox(':blue[Check the box to explore the localities.]')
    if show_map:
        country_map=geograph(filter1)    

    st.sidebar.markdown('**Staticstics**')
    show_stats=st.sidebar.button(':blue[Stats]')
    if show_stats:
        bar_chart(filter1)
        
    #Enable filters
    col1, col2=st.columns(2)
    with col1:
        st.markdown('Toggle on to enable restaurant filters')
        toggle_filter=st.toggle(':blue[Filter On]')
    with col2:    
        st.markdown('Online Table Bookings')
        online_book=st.button(':blue[Book your table!]')


    if toggle_filter:
        Met_conditions=filter_on(filter1)
        show_details(Met_conditions, 'Filtered Restaurants and Cuisines')

    elif online_book:
        table_df=filter1[filter1['Has_table_booking']==1]
        show_details(table_df, 'Restaurants with table Reservations options')

    else:    
        top_res=filter1[filter1['Aggregate_rating']>=4.0]
        top_res_sorted=top_res.sort_values(by='Aggregate_rating', ascending=False)
        top=top_restaurants(top_res_sorted, selected_country)

    



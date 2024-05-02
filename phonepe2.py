import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import plotly.express as px
import requests
import json

#sql_connection
mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        password = "rootroot",
                        database = "Phonepe_db",
                        port = "5432"
                        )
cursor = mydb.cursor()

#aggre_insurance
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table0=cursor.fetchall()

aggregated_insurance=pd.DataFrame(table0,columns=('states', 'year', 'quarter', 'transaction_type', 'transaction_count',
       'transaction_amount'))

#aggre_transaction
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table1=cursor.fetchall()

aggregated_transaction=pd.DataFrame(table1,columns=('states', 'year', 'quarter', 'transaction_type', 'transaction_count',
       'transaction_amount'))

# aggre_user
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table2=cursor.fetchall()

aggregated_user=pd.DataFrame(table2,columns=('states', 'year', 'quarter', 'brand', 'transaction_count',
       'transaction_percentage'))

# map_insurance
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table3=cursor.fetchall()

map_insurance=pd.DataFrame(table3,columns=('states', 'year', 'quarter', 'district', 'transaction_count',
       'transaction_amount'))

# map_transaction
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table4=cursor.fetchall()
map_transaction=pd.DataFrame(table4,columns=('states', 'year', 'quarter', 'district', 'transaction_count',
       'transaction_amount'))

# map_user
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table5=cursor.fetchall()

map_user=pd.DataFrame(table5,columns=('states', 'year', 'quarter', 'district', 'registeredUsers', 'appOpens'))

#top_insurance
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table6=cursor.fetchall()

top_insurance=pd.DataFrame(table6,columns=('states', 'year', 'quarter', 'pincodes', 'transaction_count',
       'transaction_amount'))

# top_transaction
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table7=cursor.fetchall()

top_transaction=pd.DataFrame(table7,columns=('states', 'year', 'quarter', 'pincodes', 'transaction_count',
       'transaction_amount'))

# map_user
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table8=cursor.fetchall()

top_user=pd.DataFrame(table8,columns=('states', 'year', 'quarter', 'pincodes', 'registeredUsers'))


#Function for Transaction amount and count  
def transaction_amount_count_Y(df, year):
    tacy = df[df["year"] == year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("states")[["transaction_count", "transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    # Create containers for layout with full width
    container1, container2 = st.columns(2)

    # Plot Transaction Amount in the first column
    with container1:
        st.header(f"{year} Transaction Amount")
        fig_amount = px.bar(tacyg, x="states", y="transaction_amount",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount, use_container_width=True)

    # Plot Transaction Count in the second column
    with container2:
        st.header(f"{year} Transaction Count")
        fig_count = px.bar(tacyg, x="states", y="transaction_count",
                           color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count, use_container_width=True)

    container1, container2 = st.columns(2)
    with container1:
            
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        st.header(f"{year} Transaction Amount on India Map")
        fig_india_1=px.choropleth(tacyg,geojson=data1,locations="states",featureidkey="properties.ST_NM",
                            color="transaction_amount",color_continuous_scale="Rainbow",
                            range_color=(tacyg["transaction_amount"].min(),tacyg["transaction_amount"].max()),
                            hover_name="states",title=f"{year} TRANSACTION COUNT",fitbounds="locations")
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1 ,use_container_width=True)

    with container2:
        st.header(f"{year} Transaction Count on India Map")
        fig_india_2=px.choropleth(tacyg,geojson=data1,locations="states",featureidkey="properties.ST_NM",
                            color="transaction_count",color_continuous_scale="Rainbow",
                            range_color=(tacyg["transaction_count"].min(),tacyg["transaction_count"].max()),
                            hover_name="states",title=f"{year} TRANSACTION COUNT",fitbounds="locations")
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2 ,use_container_width=True)

    return tacy

#Function to filter year based on quarter
def transaction_amount_count_YQ(df,quater):
    tacy=df[df["quarter"]==quater]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("states")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:           
        fig_amount=px.bar(tacyg,x="states",y="transaction_amount",
                        title=f"{tacy['year'].min()} YEAR {quater} QUARTER TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount,use_container_width=True)
    with col2:
        fig_count=px.bar(tacyg,x="states",y="transaction_count",
                        title=f"{tacy['year'].min()} YEAR {quater} QUARTER TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count,use_container_width=True)


    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson=data1,locations="states",featureidkey="properties.ST_NM",
                            color="transaction_amount",color_continuous_scale="Rainbow",
                            range_color=(tacyg["transaction_amount"].min(),tacyg["transaction_amount"].max()),
                            hover_name="states",title=f"{tacy['year'].min()} YEAR {quater} QUARTER TRANSACTION COUNT",fitbounds="locations")
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1,use_container_width=True)
    with col2:
        fig_india_2=px.choropleth(tacyg,geojson=data1,locations="states",featureidkey="properties.ST_NM",
                            color="transaction_count",color_continuous_scale="Rainbow",
                            range_color=(tacyg["transaction_count"].min(),tacyg["transaction_count"].max()),
                            hover_name="states",title=f"{tacy['year'].min()} YEAR {quater} QUARTER TRANSACTION COUNT",fitbounds="locations")
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2,use_container_width=True)

    return tacy


#transacation _type function in states
def transaction_type_amount_count_Y(df,state):
    tacy=df[df["states"]==state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("transaction_type")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_pie_1=px.pie(data_frame=tacyg,names="transaction_type",values="transaction_amount",width=600,
                        title=f"{state.upper()} TRANSACTION AMOUNT",hole=0.4)
        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2=px.pie(data_frame=tacyg,names="transaction_type",values="transaction_count",width=600,
                        title=f"{state.upper()} TRANSACTION COUNT",hole=0.4)
        st.plotly_chart(fig_pie_2)


#streamlit 

st.set_page_config(layout="wide",)
st.title("PHONEPE DATA EXPLORATION WITH VISUALIZATION")

with st.sidebar:
    
    select=option_menu('Main Menu',["HOME","DATA EXPLORATION","TOP CHARTS"])
    
if select=="HOME":
    pass

elif select=="DATA EXPLORATION":
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
    
    with tab1:

        method=st.radio("SELECT THE METHOD FOR AGGREGATED ANALYSIS",["INSURANCE ANALYSIS","TRANSACTION ANALYSIS","USER ANALYSIS"])
        if method=="INSURANCE ANALYSIS":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select the year",aggregated_insurance["year"].min(),aggregated_insurance["year"].max(),aggregated_insurance["year"].min())
            tac_y=transaction_amount_count_Y(aggregated_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the quarter",tac_y["quarter"].min(),tac_y["quarter"].max(),tac_y["quarter"].min())
            transaction_amount_count_YQ(tac_y,quarters)


        elif method=="TRANSACTION ANALYSIS":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select the year",aggregated_transaction["year"].min(),aggregated_transaction["year"].max(),aggregated_transaction["year"].min())
            ag_tr_tac_y=transaction_amount_count_Y(aggregated_transaction,years)

            col1,col2=st.columns(2)
            with col2:
                state=st.selectbox("Select the states",ag_tr_tac_y["states"].unique())
            transaction_type_amount_count_Y(ag_tr_tac_y,state)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the quarter",ag_tr_tac_y["quarter"].min(),ag_tr_tac_y["quarter"].max(),ag_tr_tac_y["quarter"].min())
            ag_tr_tac_yq=transaction_amount_count_YQ(ag_tr_tac_y,quarters)

            col1,col2=st.columns(2)
            with col2:
                state=st.selectbox("Select the states with transaction type",ag_tr_tac_yq["states"].unique())
            transaction_type_amount_count_Y(ag_tr_tac_yq,state)

        elif method=="USER ANALYSIS":
            pass

    with tab2:

        method=st.radio("SELECT THE METHOD FOR MAP ANALYSIS",["INSURANCE ANALYSIS","TRANSACTION ANALYSIS","USER ANALYSIS"])
        if method=="INSURANCE ANALYSIS":
            pass
        elif method=="TRANSACTION ANALYSIS":
            pass
        elif method=="USER ANALYSIS":
            pass

    with tab3:

        method==st.radio("SELECT THE METHOD FOR TOP ANALYSIS",["INSURANCE ANALYSIS","TRANSACTION ANALYSIS","USER ANALYSIS"])
        if method=="INSURANCE ANALYSIS":
            pass
        elif method=="TRANSACTION ANALYSIS":
            pass
        elif method=="USER ANALYSIS":
            pass

elif select=="TOP CHARTS":
    pass

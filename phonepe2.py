import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import plotly.express as px

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


# Transaction amount and count function
def transaction_amount_count_Y(df, year):
    tacy = df[df["year"] == year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("states")[["transaction_count", "transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    # Create columns for layout
    col1, col2 = st.columns(2)

    # Plot Transaction Amount in the first column
    with col1:
        fig_amount = px.bar(tacyg, x="states", y="transaction_amount",
                            title=f"{year} Transaction Amount",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount, use_container_width=True)

    # Plot Transaction Count in the second column
    with col2:
        fig_count = px.bar(tacyg, x="states", y="transaction_count",
                           title=f"{year} Transaction Count",
                           color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count, use_container_width=True)


#streamlit 

st.set_page_config(layout="wide")
st.title("PHONEPE DATA EXPLORATION WITH VISUALIZATION")

with st.sidebar:
    
    select=option_menu('Main Menu',["HOME","DATA EXPLORATION","TOP CHARTS"])
    
if select=="HOME":
    pass

elif select=="DATA EXPLORATION":
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
    
    with tab1:

        method=st.radio("SELECT THE METHOD FOR AGGREGATED ANALYSIS",["AGGREGATED INSURANCE","AGGREGATED TRANSACTION","AGGREGATED USER"])
        if method=="AGGREGATED INSURANCE":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select the year",aggregated_insurance["year"].min(),aggregated_insurance["year"].max(),aggregated_insurance["year"].min())
                transaction_amount_count_Y(aggregated_insurance,years)

        elif method=="AGGREGATED TRANSACTION":
            pass
        elif method=="AGGREGATED USER":
            pass

    with tab2:

        method=st.radio("SELECT THE METHOD FOR MAP ANALYSIS",["MAP INSURANCE","MAP TRANSACTION","MAP USER"])
        if method=="MAP INSURANCE":
            pass
        elif method=="MAP TRANSACTION":
            pass
        elif method=="MAP USER":
            pass

    with tab3:

        method==st.radio("SELECT THE METHOD FOR TOP ANALYSIS",["TOP INSURANCE","TOP TRANSACTION","TOP USER"])
        if method=="TOP INSURANCE":
            pass
        elif method=="TOP TRANSACTION":
            pass
        elif method=="TOP USER":
            pass

elif select=="TOP CHARTS":
    pass
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
def transaction_amount_count_YQ(df,quarter):
    tacy=df[df["quarter"]==quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("states")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:           
        fig_amount=px.bar(tacyg,x="states",y="transaction_amount",
                        title=f"{tacy['year'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount,use_container_width=True)
    with col2:
        fig_count=px.bar(tacyg,x="states",y="transaction_count",
                        title=f"{tacy['year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Bluered_r)
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
                            hover_name="states",title=f"{tacy['year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations")
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1,use_container_width=True)
    with col2:
        fig_india_2=px.choropleth(tacyg,geojson=data1,locations="states",featureidkey="properties.ST_NM",
                            color="transaction_count",color_continuous_scale="Rainbow",
                            range_color=(tacyg["transaction_count"].min(),tacyg["transaction_count"].max()),
                            hover_name="states",title=f"{tacy['year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations")
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

#aggre_user_analysis_1
def aggre_user_plot_1(df,year):
    aguy=df[df["year"]==year]
    aguy.reset_index(drop=True,inplace=True)
    aguyg=pd.DataFrame(aguy.groupby("brand")[["transaction_count","transaction_percentage"]].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg,x="brand",y="transaction_count",title=f"{year} BRAND AND TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Electric_r,hover_name="brand")
    st.plotly_chart(fig_bar_1)
    return aguy

#aggre_user_analysis_2
def aggre_user_plot_2(df,quarter):
    aguyq=df[df["quarter"]==quarter]
    aguyq.reset_index(drop=True,inplace=True)
    aguyqg=pd.DataFrame(aguyq.groupby("brand")["transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyqg,x="brand",y="transaction_count",title=f"{quarter} QUARTER ,BRAND AND TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Electric_r,hover_name="brand")
    st.plotly_chart(fig_bar_1)
    return aguyq

#aggre_user_analysis_3
def aggre_user_plot_3(df,states):
    auyqs=df[df["states"]==states]
    auyqs.reset_index(drop=True,inplace=True)

    fig_line_1=px.line(auyqs,x="brand",y="transaction_count",hover_data="transaction_percentage",
                       title=f"{states.upper()} BRANDS ,TRANSACTION COUNT ,PERCENTAGE",width=1000,markers=True)

    st.plotly_chart(fig_line_1)

#map_insurance district analysis
def map_insur_District(df,state):
    tacy=df[df["states"]==state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("district")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(tacyg,x="transaction_amount",y="district",orientation="h",
                        height=600,width=800,title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2=px.bar(tacyg,x="transaction_count",y="district",orientation="h",
                        height=600,width=800,title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.RdBu_r)
        st.plotly_chart(fig_bar_2)


#map_user_plot_1 analysis
def map_user_plot_1(df,year):
    muy=df[df["year"]==year]
    muy.reset_index(drop=True,inplace=True)
    muyg=pd.DataFrame(muy.groupby("states")[["registeredUsers","appOpens"]].sum())
    muyg.reset_index(inplace=True)

    fig_line_1=px.line(muyg,x="states",y=["registeredUsers","appOpens"],
                        title=f"{year} REGISTERED USERS AND APP OPENS",width=1000,height=800,markers=True)
    st.plotly_chart(fig_line_1)
    return muy

#map_user_plot_2 analysis
def map_user_plot_2(df,quarter):
    muyq=df[df["quarter"]==quarter]
    muyq.reset_index(drop=True,inplace=True)
    muyqg=pd.DataFrame(muyq.groupby("states")[["registeredUsers","appOpens"]].sum())
    muyqg.reset_index(inplace=True)

    fig_line_1=px.line(muyqg,x="states",y=["registeredUsers","appOpens"],
                        title=f"{df['year'].min()} YEAR {quarter} QUARTER REGISTERED USERS AND APP OPENS",width=1000,height=800,markers=True
                        ,color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)
    return muyq

#map_user_plot_3
def map_user_plot_3(df,state):
    muyqs=df[df["states"]==state]
    muyqs.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(muyqs,x="registeredUsers",y="district",orientation="h",
                        title=f"{state.upper()} REGISTERED USER",height=600,color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2=px.bar(muyqs,x="appOpens",y="district",orientation="h",
                        title=f"{state.upper()} APPOPENS",height=600,color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_bar_2)
    
#top_inusrance analysis plot1
def top_ins_plot_1(df,state):
    tiy=df[df["states"]==state]
    tiy.reset_index(drop=True,inplace=True)
    tiyg=pd.DataFrame(tiy.groupby("pincodes")[["transaction_count","transaction_amount"]].sum())
    tiyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(tiy,x="quarter",y="transaction_amount",hover_data="pincodes",
                        title="TRANSACTION AMOUNT",height=650,width=600,color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2=px.bar(tiy,x="quarter",y="transaction_count",hover_data="pincodes",
                        title="TRANSACTION COUNT",height=650,width=600,color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_bar_2)

def top_user_plot_1(df,year):
    tuy=df[df["year"]==year]
    tuy.reset_index(drop=True,inplace=True)
    tuyg=pd.DataFrame(tuy.groupby(["states","quarter"])["registeredUsers"].sum())
    tuyg.reset_index(inplace=True)
    fig_top_plot_1=px.bar(tuy,x="states",y="registeredUsers",color="quarter",width=1000,height=800,
                        color_discrete_sequence=px.colors.sequential.Rainbow_r,hover_name="states"
                        ,title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)
    return tuy

def top_user_plot_2(df,state):
    tuy=df[df["states"]==state]
    tuy.reset_index(drop=True,inplace=True)

    fig_top_plot_2=px.bar(tuy,x="quarter",y="registeredUsers",title="REGISTERED USERS , PINCODES , QUARTER",width=1000,height=800,color="registeredUsers",hover_data="pincodes"
                        ,color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)

#top chart 
def top_chart_transaction_amount(table_name):
        mydb = psycopg2.connect(host = "localhost",
                                user = "postgres",
                                password = "rootroot",
                                database = "Phonepe_db",
                                port = "5432"
                                )
        cursor = mydb.cursor()

        query1=f'''-- top 10
                SELECT states, sum(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''
        
        cursor.execute(query1)
        table=cursor.fetchall()
        mydb.commit()

        #plot1
        df=pd.DataFrame(table,columns=("states","transaction_amount"))

        col1,col2=st.columns(2)
        with col1:
            fig_amount=px.bar(df,x="states",y="transaction_amount",
                            title="TOP 10 OF TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=600,width=600
                            ,hover_name="states")
            st.plotly_chart(fig_amount)

        query2=f'''-- top 10
                SELECT states, sum(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount
                LIMIT 10;'''
        cursor.execute(query2)
        table1=cursor.fetchall()
        mydb.commit()

        #plot2
        df1=pd.DataFrame(table1,columns=("states","transaction_amount"))
        
        with col2:
            fig_amount1=px.bar(df1,x="states",y="transaction_amount",
                            title="LAST 10 OF TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=600,width=600
                            ,hover_name="states")
            st.plotly_chart(fig_amount1)

        query3=f'''-- average
                SELECT states, avg(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''
        cursor.execute(query3)
        table2=cursor.fetchall()
        mydb.commit()

        #plot3
        df2=pd.DataFrame(table2,columns=("states","transaction_amount"))

        fig_amount2=px.bar(df2,y="states",x="transaction_amount",
                        title="AVERAGE 10 OF TRANSACTION AMOUNT",color_discrete_sequence=
                        px.colors.sequential.YlOrBr,height=800,width=1000
                        ,hover_name="states",orientation="h")
        st.plotly_chart(fig_amount2)

#top chart count
def top_chart_transation_count(table_name):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            password="rootroot",
                            database="Phonepe_db",
                            port="5432")
    cursor = mydb.cursor()

    query1 = f'''
        SELECT states, sum(transaction_count) AS transaction_count
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_count DESC
        LIMIT 10;
    '''
    
    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()

    # Plot1
    df = pd.DataFrame(table, columns=("states", "transaction_count"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df, x="states", y="transaction_count",
                            title="TOP 10 OF TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            height=600, width=600, hover_name="states")
        st.plotly_chart(fig_amount)

    query2 = f'''
        SELECT states, sum(transaction_count) AS transaction_count
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_count
        LIMIT 10;
    '''
    cursor.execute(query2)
    table1 = cursor.fetchall()
    mydb.commit()

    # Plot2
    df1 = pd.DataFrame(table1, columns=("states", "transaction_count"))
    with col2:
        fig_amount1 = px.bar(df1, x="states", y="transaction_count",
                            title="LAST 10 OF TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            height=600, width=600, hover_name="states")
        st.plotly_chart(fig_amount1)

    query3 = f'''
        SELECT states, avg(transaction_count) AS transaction_count
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_count;
    '''
    cursor.execute(query3)
    table2 = cursor.fetchall()
    mydb.commit()

    # Plot3
    df2 = pd.DataFrame(table2, columns=("states", "transaction_count"))

    fig_amount2 = px.bar(df2, y="states", x="transaction_count",
                         title="AVERAGE 10 OF TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.YlOrBr,
                         height=800, width=1000, hover_name="states", orientation="h")
    st.plotly_chart(fig_amount2)

def top_chart_registeredusers_amount(table_name,states):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            password="rootroot",
                            database="Phonepe_db",
                            port="5432")
    cursor = mydb.cursor()

    query1 = f'''SELECT district, sum(registeredusers) as registeredusers
                        from {table_name}
                        where states='{states}'
                        group by district
                        order by registeredusers desc
                        limit 10;'''
    
    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()

    # Plot1
    df = pd.DataFrame(table, columns=("district", "registeredusers"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df, x="district", y="registeredusers",
                            title="TOP 10 OF REGISTERESUSERS", color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            height=600, width=600, hover_name="district")
        st.plotly_chart(fig_amount)

    query2 = f'''
                        SELECT district, sum(registeredusers) as registeredusers
                        from {table_name}
                        where states='{states}'
                        group by district
                        order by registeredusers 
                        limit 10;
    '''
    cursor.execute(query2)
    table1 = cursor.fetchall()
    mydb.commit()

    # Plot2
    df1 = pd.DataFrame(table1, columns=("district", "registeredusers"))
    with col2:

        fig_amount1 = px.bar(df1, x="district", y="registeredusers",
                            title="LAST 10 OF REGISTEREDUSERS", color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            height=600, width=600, hover_name="district")
        st.plotly_chart(fig_amount1)

    query3 = f'''
                    SELECT district, avg(registeredusers) as registeredusers
                    from {table_name}
                    where states='{states}'
                    group by district
                    order by registeredusers;'''
    
    cursor.execute(query3)
    table2 = cursor.fetchall()
    mydb.commit()

    # Plot3
    df2 = pd.DataFrame(table2, columns=("district", "registeredusers"))

    fig_amount2 = px.bar(df2, y="district", x="registeredusers",
                         title="AVG REGISTEREDUSERS", color_discrete_sequence=px.colors.sequential.Magenta,
                         height=800, width=1000, hover_name="district", orientation="h")
    st.plotly_chart(fig_amount2)

def top_chart_appopens_amount(table_name,states):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            password="rootroot",
                            database="Phonepe_db",
                            port="5432")
    cursor = mydb.cursor()

    query1 = f'''SELECT district, sum(appopens) as appopens
                        from {table_name}
                        where states='{states}'
                        group by district
                        order by appopens desc
                        limit 10;'''
    
    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()

    # Plot1
    df = pd.DataFrame(table, columns=("district", "appopens"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df, x="district", y="appopens",
                            title="TOP 10 OF APPOPENS", color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            height=600, width=600, hover_name="district")
        st.plotly_chart(fig_amount)

    query2 = f'''
                        SELECT district, sum(appopens) as appopens
                        from {table_name}
                        where states='{states}'
                        group by district
                        order by appopens 
                        limit 10;
    '''
    cursor.execute(query2)
    table1 = cursor.fetchall()
    mydb.commit()

    # Plot2
    df1 = pd.DataFrame(table1, columns=("district", "appopens"))
    with col2:
        fig_amount1 = px.bar(df1, x="district", y="appopens",
                            title="LAST 10 OF APPOPENS", color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            height=600, width=600, hover_name="district")
        st.plotly_chart(fig_amount1)

    query3 = f'''
                    SELECT district, avg(appopens) as appopens
                    from {table_name}
                    where states='{states}'
                    group by district
                    order by appopens;'''
    
    cursor.execute(query3)
    table2 = cursor.fetchall()
    mydb.commit()

    # Plot3
    df2 = pd.DataFrame(table2, columns=("district", "appopens"))

    fig_amount2 = px.bar(df2, y="district", x="appopens",
                         title="AVG APPOPENS", color_discrete_sequence=px.colors.sequential.Magenta,
                         height=800, width=1000, hover_name="district", orientation="h")
    st.plotly_chart(fig_amount2)

def top_chart_registeredusers(table_name):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            password="rootroot",
                            database="Phonepe_db",
                            port="5432")
    cursor = mydb.cursor()

    query1 = f'''SELECT states, sum(registeredusers) as registeredusers
                        from {table_name}
                        group by states
                        order by registeredusers desc
                        limit 10;'''
    
    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()

    # Plot1
    df = pd.DataFrame(table, columns=("states", "registeredusers"))
    col1,col2=st.columns(2)
    with col1:
            
        fig_amount = px.bar(df, x="states", y="registeredusers",
                            title="TOP 10 OF REGISTERESUSERS", color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            height=600, width=600, hover_name="states")
        st.plotly_chart(fig_amount)

    query2 = f'''
                        SELECT states, sum(registeredusers) as registeredusers
                        from {table_name}
                        group by states
                        order by registeredusers 
                        limit 10;
    '''
    cursor.execute(query2)
    table1 = cursor.fetchall()
    mydb.commit()

    # Plot2
    df1 = pd.DataFrame(table1, columns=("states", "registeredusers"))
    with col2:
            
        fig_amount1 = px.bar(df1, x="states", y="registeredusers",
                            title="LAST 10 OF REGISTEREDUSERS", color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            height=600, width=600, hover_name="states")
        st.plotly_chart(fig_amount1)

    query3 = f'''
                    SELECT states, avg(registeredusers) as registeredusers
                    from {table_name}
                    group by states
                    order by registeredusers;'''
    
    cursor.execute(query3)
    table2 = cursor.fetchall()
    mydb.commit()

    # Plot3
    df2 = pd.DataFrame(table2, columns=("states", "registeredusers"))

    fig_amount2 = px.bar(df2, y="states", x="registeredusers",
                         title="AVG REGISTEREDUSERS", color_discrete_sequence=px.colors.sequential.Magenta,
                         height=800, width=1000, hover_name="states", orientation="h")
    st.plotly_chart(fig_amount2)



#streamlit 
st.set_page_config(layout="wide",)
st.title("PHONEPE DATA EXPLORATION WITH VISUALIZATION")

with st.sidebar:
    
    select=option_menu('Main Menu',["HOME","DATA EXPLORATION","TOP CHARTS"])
    
if select=="HOME":
    pass

elif select=="DATA EXPLORATION":
    tab1,tab2,tab3 =st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
    
    with tab1:

        method_1=st.radio("SELECT THE METHOD FOR AGGREGATED ANALYSIS",["INSURANCE ANALYSIS","TRANSACTION ANALYSIS","USER ANALYSIS"])
        if method_1=="INSURANCE ANALYSIS":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select the year in aggregated insurance",aggregated_insurance["year"].min(),aggregated_insurance["year"].max(),aggregated_insurance["year"].min())
            tac_y=transaction_amount_count_Y(aggregated_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                quarter=st.slider("Select the quarter in aggregated insurance",tac_y["quarter"].min(),tac_y["quarter"].max(),tac_y["quarter"].min())
            transaction_amount_count_YQ(tac_y,quarter)


        elif method_1=="TRANSACTION ANALYSIS":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select the year in aggregated transaction",aggregated_transaction["year"].min(),aggregated_transaction["year"].max(),aggregated_transaction["year"].min())
            ag_tr_tac_y=transaction_amount_count_Y(aggregated_transaction,years)

            col1,col2=st.columns(2)
            with col2:
                state=st.selectbox("Select the states in aggregated transaction",ag_tr_tac_y["states"].unique())
            transaction_type_amount_count_Y(ag_tr_tac_y,state)

            col1,col2=st.columns(2)
            with col1:
                quarter=st.slider("Select the quarter in aggregated transaction",ag_tr_tac_y["quarter"].min(),ag_tr_tac_y["quarter"].max(),ag_tr_tac_y["quarter"].min())
            ag_tr_tac_yq=transaction_amount_count_YQ(ag_tr_tac_y,quarter)

            col1,col2=st.columns(2)
            with col2:
                state=st.selectbox("Select the states with transaction type",ag_tr_tac_yq["states"].unique())
            transaction_type_amount_count_Y(ag_tr_tac_yq,state)

        elif method_1=="USER ANALYSIS":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the year in aggregated user",aggregated_user["year"].min(),aggregated_user["year"].max(),aggregated_user["year"].min())
            ag_user_y=aggre_user_plot_1(aggregated_user,years)
            
            with col2:
                quarter=st.slider("Select the quarter in aggregated user",ag_user_y["quarter"].min(),ag_user_y["quarter"].max(),ag_user_y["quarter"].min())
            ag_user_yq=aggre_user_plot_2(ag_user_y,quarter)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states in aggregated user",ag_user_yq["states"].unique())
            aggre_user_plot_3(ag_user_yq,states)
        

    with tab2:

        method_2=st.radio("SELECT THE METHOD FOR MAP ANALYSIS",["MAP INSURANCE","MAP TRANSACTION","MAP USER"])
        if method_2=="MAP INSURANCE":
            
            col1,col2=st.columns(2)
            
            with col1:
                years=st.slider("Select the Year in map insurance",map_insurance["year"].min(),map_insurance["year"].max(),map_insurance["year"].min())
            map_ins_tac_y=transaction_amount_count_Y(map_insurance,years)

            col1,col2=st.columns(2)

            with col2:
                state=st.selectbox("Select the states_district in map insurance",map_ins_tac_y["states"].unique())
            map_insur_District(map_ins_tac_y,state)

            
            col1,col2=st.columns(2)
            with col1:
                quarter=st.slider("Select the quarter in map insurance",map_ins_tac_y["quarter"].min(),map_ins_tac_y["quarter"].max(),map_ins_tac_y["quarter"].min())
            map_ins_tac_yq=transaction_amount_count_YQ(map_ins_tac_y,quarter)

            col1,col2=st.columns(2)
            with col2:
                state=st.selectbox("Select the states_district with transaction type",map_ins_tac_yq["states"].unique())
            map_insur_District(map_ins_tac_yq,state)

        elif method_2=="MAP TRANSACTION":

            col1,col2=st.columns(2)
            
            with col1:
                years=st.slider("Select the Year in map transaction",map_transaction["year"].min(),map_transaction["year"].max(),map_transaction["year"].min())
            map_tran_tac_y=transaction_amount_count_Y(map_transaction,years)

            col1,col2=st.columns(2)

            with col2:
                state=st.selectbox("Select the states_district",map_tran_tac_y["states"].unique())
            map_insur_District(map_tran_tac_y,state)

            
            col1,col2=st.columns(2)
            with col1:
                quarter=st.slider("Select the quarters in map transaction",map_tran_tac_y["quarter"].min(),map_tran_tac_y["quarter"].max(),map_tran_tac_y["quarter"].min())
            map_tran_tac_yq=transaction_amount_count_YQ(map_tran_tac_y,quarter)

            col1,col2=st.columns(2)
            with col2:
                state=st.selectbox("Select the states_district with transaction type",map_tran_tac_yq["states"].unique())
            map_insur_District(map_tran_tac_yq,state)

        elif method_2=="MAP USER":
            col1,col2=st.columns(2)
            
            with col1:
                years=st.slider("Select the Year in map_user",map_user["year"].min(),map_user["year"].max(),map_user["year"].min())
            map_user_y=map_user_plot_1(map_user,years)

            col1,col2=st.columns(2)
            with col1:
                quarter=st.slider("Select the quarters in map_user",map_user_y["quarter"].min(),map_user_y["quarter"].max(),map_user_y["quarter"].min())
            map_tran_tac_yq=map_user_plot_2(map_user_y,quarter)

            col1,col2=st.columns(2)

            with col2:
                state=st.selectbox("Select the states_district in map_user",map_tran_tac_yq["states"].unique())
            map_user_plot_3(map_tran_tac_yq,state)


    with tab3:

        method = st.radio("SELECT THE METHOD FOR TOP ANALYSIS", ["TOP INSURANCE", "TOP TRANSACTION", "TOP USER"])
        if method == "TOP INSURANCE":
            col1, col2 = st.columns(2)
            
            with col1:
                years = st.slider("Select the Year in top insurance", top_insurance["year"].min(), top_insurance["year"].max(), top_insurance["year"].min())
            top_ins_tac_y = transaction_amount_count_Y(top_insurance, years)

            col1,col2=st.columns(2)

            with col2:
                state=st.selectbox("Select the states in top insurance",top_ins_tac_y["states"].unique())
            top_ins_plot_1(top_ins_tac_y,state)

            col1,col2=st.columns(2)

            with col1:
                quarter=st.slider("Select the quarters in top insurance",top_ins_tac_y["quarter"].min(),top_ins_tac_y["quarter"].max(),top_ins_tac_y["quarter"].min())
            top_ins_tac_yq=transaction_amount_count_YQ(top_ins_tac_y,quarter)


        elif method == "TOP TRANSACTION":

            col1, col2 = st.columns(2)
            
            with col1:
                years = st.slider("Select the Year in top transaction", top_transaction["year"].min(), top_transaction["year"].max(), top_transaction["year"].min())
            top_trans_tac_y = transaction_amount_count_Y(top_transaction, years)

            col1,col2=st.columns(2)

            with col2:
                state=st.selectbox("Select the states in top transaction",top_trans_tac_y["states"].unique())
            top_ins_plot_1(top_trans_tac_y,state)

            col1,col2=st.columns(2)
            
            with col1:
                quarter=st.slider("Select the quarters in top transaction",top_trans_tac_y["quarter"].min(),top_trans_tac_y["quarter"].max(),top_trans_tac_y["quarter"].min())
            top_ins_tac_yq=transaction_amount_count_YQ(top_trans_tac_y,quarter)

        elif method == "TOP USER":
            col1, col2 = st.columns(2)
            
            with col1:
                years = st.slider("Select the Year in top user", top_user["year"].min(), top_user["year"].max(), top_user["year"].min())
            top_user_y = top_user_plot_1(top_user, years)

            col1,col2=st.columns(2)

            with col2:
                state=st.selectbox("Select the states in top user",top_user_y["states"].unique())
            top_user_plot_2(top_user_y,state)

elif select=="TOP CHARTS":
    Question=st.selectbox("Select the Questions",["1.Transaction Amount and Count of Aggregated Insurance",
                                                   "2.Transaction Amount and Count of Map Insurance",
                                                   "3.Transaction Amount and Count of Top Insurance",
                                                   "4.Transaction Amount and Count of Aggregated Transaction",
                                                   "5.Transaction Amount and Count of Map Transaction",
                                                   "6.Transaction Amount and Count of Top Transaction",
                                                   "7.Transaction Amount and Count of Aggregated User",
                                                   "8.Transaction Count of Aggregated User",
                                                   "9.App opens of Map User",
                                                   "10.App opens of Top User"
                                                   ])

    if Question =="1.Transaction Amount and Count of Aggregated Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transation_count("aggregated_insurance")
    elif Question =="2.Transaction Amount and Count of Map Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transation_count("map_insurance")
    elif Question =="3.Transaction Amount and Count of Top Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transation_count("top_insurance")
    elif Question =="4.Transaction Amount and Count of Aggregated Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transation_count("aggregated_transaction")
    elif Question =="5.Transaction Amount and Count of Map Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transation_count("map_transaction")
    elif Question =="6.Transaction Amount and Count of Top Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transation_count("top_transaction")
    elif Question =="7.Transaction Amount and Count of Aggregated User":
        st.subheader("TRANSACTION COUNT")
        top_chart_transation_count("aggregated_user")
    elif Question=="8.Transaction Count of Aggregated User":
        states=st.selectbox("Select the states with registeredusers",map_user["states"].unique())  
        st.subheader("REGISTERED USERS")
        top_chart_registeredusers_amount("map_user",states)
    elif Question=="9.App opens of Map User":
        states=st.selectbox("Select the states with appopens in map_user",map_user["states"].unique())  
        st.subheader("APPOPENS")
        top_chart_appopens_amount("map_user",states)
    elif Question== "10.App opens of Top User":
        st.subheader("REGISTERED USERS")
        top_chart_registeredusers("top_user")

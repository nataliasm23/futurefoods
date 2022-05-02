
import streamlit as st
import pandas    as pd
import numpy     as np
import plotly.graph_objects as go
from datetime import datetime, time
import plotly.express as px 
import plotly.figure_factory as ff


# ------------------------------------------
# settings
# ------------------------------------------
st.set_page_config( layout='wide' )


# ------------------------------------------
# Helper Functions
# ------------------------------------------
@st.cache( allow_output_mutation=True )
def get_data(path):
    df = pd.read_csv(path)

    return df




#st.write(df.head())
#f_days = st.sidebar.multiselect( 'Enter days of week', df.day_of_week.unique() ) 
def filter_cuisine(df):
    f_cuisine = st.sidebar.multiselect( 'Enter cuisine', df.group.unique() ) 

    if f_cuisine == []:
        df = df.copy()
    else:
        df= df.loc[df['group'].isin(f_cuisine)] 
        
    return df




st.header('Future Foods Dash')  

def top_items_hour_of_day(df):
    #Top items by hour of day
    group_view = df[['name_en','date','hour','completed_orders_ofo_state']]
    view = group_view.groupby('hour').agg({'completed_orders_ofo_state':['sum', 'max'], 
                                        'name_en':'max',
                                        'name_en': (lambda x: x.value_counts().index[0])}).reset_index()
    view.columns = view.columns.droplevel()


    view = view.rename(columns={view.columns[0]: 'hour',
                        view.columns[1]: 'completed_orders_sum',
                        view.columns[2]: 'completed_orders_max',
                        view.columns[3]: 'name_mode'})
        
    fig = px.bar(view, x='hour', y='completed_orders_sum', color="name_mode",
                            labels={
                                "name_mode": "Top 1 item",
                                "completed_orders_sum": "Total oreders",
                                'hour': 'Hour'
                                
        
                            },
                            title="Top items by hour of day")
        #fig.show()
        # 
    st.plotly_chart( fig, use_container_width=True )
    return None

def top_items_day_of_week(df):
    #Top items by day of week
    group_view = df[['name_en','date','hour','completed_orders_ofo_state', 'day_of_week']].copy()
    view = group_view.groupby('day_of_week').agg({'completed_orders_ofo_state':['sum', 'max'], 
                                        'name_en':'max',
                                        'name_en': (lambda x: x.value_counts().index[0])}).reset_index()
    view.columns = view.columns.droplevel()


    view = view.rename(columns={view.columns[0]: 'day_of_week',
                                    view.columns[1]: 'completed_orders_sum',
                                    view.columns[2]: 'completed_orders_max',
                                    view.columns[3]: 'name_mode'})
            
    fig = px.bar(view, x='day_of_week', y='completed_orders_sum', color="name_mode",
                            labels={
                                "name_mode": "Top 1 item",
                                "completed_orders_sum": "Total orders",
                                'hour': 'Hour'},
                            category_orders={"day_of_week": ['Monday',   
                                                            'Tuesday',  
                                                            'Wednesday',
                                                            'Thursday' ,
                                                            'Friday'   ,
                                                            'Saturday' ,
                                                            'Sunday'   ]},
                                
                            title="Top items by day of week")

    st.plotly_chart( fig, use_container_width=True )
    return None

def sales (df):
    # Sales per date
    df['total_eater_spend__2'] = df.total_eater_spend - df.total_eater_spend__1
    date_view = df.groupby('date')[['total_eater_spend','total_eater_spend__1', 'total_eater_spend__2']].sum().reset_index()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=date_view.date,
            y=date_view.total_eater_spend,
            name="Spend ($)"
        ))

    fig.add_trace(
        go.Scatter(
            x=date_view.date,
            y= -date_view.total_eater_spend__1,
            name="Discount ($)"
        ))

    fig.add_trace(
        go.Scatter(
            x=date_view.date,
            y=date_view.total_eater_spend + date_view.total_eater_spend__1,
            name="Final Spend ($)"
        ))
    fig.update_layout(
        title="Sales per date - the avarage per day is $ 893.501 ",
        
        )
    st.plotly_chart( fig, use_container_width=True )
    return None

def returning(df):
    returning_view = df[['day_of_week', 'returning_orders', 'completed_orders_ofo_state',
           'returning_orders_promo', 'first_time_orders_promo', 'first_time_orders']]
    
    returning_view = df.groupby('day_of_week').agg({'returning_orders':'sum', 
                                                  'completed_orders_ofo_state':'sum',
                                                    'returning_orders_promo':'sum',
                                                    'first_time_orders_promo':'sum',
                                                    'first_time_orders':'sum'
    
                                                  }).reset_index()
    
    returning_view['returning_rate'] =round(returning_view.returning_orders / returning_view.completed_orders_ofo_state*100 )
    returning_view['first_time_orders_rate'] =round(returning_view.first_time_orders / returning_view.completed_orders_ofo_state*100 )
    returning_view['first_time_orders_rate_promo'] =round(returning_view.first_time_orders_promo / returning_view.completed_orders_ofo_state*100 )
    
    a = returning_view[[ 'day_of_week','returning_rate', 'first_time_orders_rate', 'first_time_orders_rate_promo']]
    
    
    
    
    st.dataframe(a)
    
    return None


if __name__ == "__main__":
    # ETL
    path = 'treated_data_ff_final.csv'
      
    # load data
    df = get_data(path)
    
    
    # transform data
    df = filter_cuisine(df)

    top_items_hour_of_day(df)

    top_items_day_of_week(df)

    sales(df)

    returning(df)





    



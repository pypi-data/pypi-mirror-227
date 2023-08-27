#!/usr/bin/env python3 
import pymssql 
import boto3 
import json
import os 
import logging 
import re 
import pandas as pd
from sklearn import metrics 
from eia.utils.constants import STATES_LOOKUP, INVERSE_STATES

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class OdinDBMSSQL(object): 

    def __init__(self, region_name: str = 'us-east-1'):
        
        self.secrets = boto3.client(service_name='secretsmanager',
                                    region_name=region_name, 
                                    aws_access_key_id=os.environ["DEV-KEY"],
                                    aws_secret_access_key=os.environ["DEV-VAL"]
                                   )
        self.user, self.password, self.server, self.db = list(json.loads(self.secrets.get_secret_value(SecretId='mssql_db_analysis').get('SecretString')).values())
        
        self.con: 'MSSQL' = pymssql.connect(user=self.user, password=self.password, server=self.server, database=self.db)
        self.con.autocommit(True)
        self.cursor = self.con.cursor() 


    def get_store_reviews(self, lat: float, lon: float) -> 'DataFrame':

        try: 
            return pd.read_sql(f"SELECT * FROM GetStoreReviews({lat}, {lon})", con=self.con)

        except ConnectionError as e:
            raise ConnectionError(f"[ ERROR ] Unable to retrieve store location at the following loc: ({lat},{lon})") from e 

            
    def get_live_gasprices(self, state: str) -> 'DataFrame':
        """
        Description: 
            - Helper function to return today's gasoline prices based on the given state
              and call the custom T-SQL gasoline prices GetTodayLiveGasPrices
        Params: 
            - @state: give a valid US State 
        
        """
        try: 
            state_name: str = STATES_LOOKUP.get(INVERSE_STATES.get(state, 'WA'))
            return pd.read_sql(f"SELECT * FROM GetTodayLiveGasPrices('{state_name}') ORDER BY timestamp ASC", con=self.con)

        except ConnectionError as e:
            raise ConnectionError(f"[ ERROR ] Unable to query the following state {state}") from e 


    def get_avg_price(self, station_name: str , state:str) -> 'DataFrame':

        try: 
            return pd.read_sql(f"SELECT g.gas_station, g.state, CAST(g.avg_price AS MONEY ) FROM GetGasolineAvgPrice( '{station_name}', '{state}') g",con=self.con)
        
        except ConnectionError as e:
            raise ConnectionError(f"[ ERROR ] Unable to retrieve gas_station average price for the given region {state_name}") from e 

    def get_gas_station_reviews(self, state_name: str) -> 'DataFrame': 

        try:

            return pd.read_sql(f"SELECT * FROM GetGasStationReviews('{state_name}')", con=self.con)
        
        except ConnectionError as e:
            raise ConnectionError(f"[ ERROR ] Unable to retrieve reviews for the given region '{state_name}' ") from e 


    def get_historical_gasprice(self, state_name: str): 

        try:
            return pd.read_sql(f"SELECT * FROM GetHistoricalGasolinePriceByState('{state_name}')", con=self.con)

        except ConnectionError as e:
            raise ConnectionError("[ ERROR ] Unable to retrieve historical price for the following state {state_name}") from e 


    def get_store_amenities(self, lat: float, lon: float) -> 'DataFrame':

        try:
            return pd.read_sql(f"SELECT * FROM GetStoreAmenities({lat}, {lon})", con=self.con)

        except ConnectionError as e: 
            raise ConnectionError(f"[ ERROR ] Unable to get the store amenities from the following location ({lat},{lon})") from e 


    def get_store_offers(self, lat: float, lon: float) -> 'DataFrame':

        if not isinstance(lat, float) and not isinstance(lon, float): 
            raise ValueError("[ ERROR ] lat,lon required type float.")
            
        try: 
            return pd.read_sql(f"SELECT *  FROM GetStoreOffers({lat}, {lon})", con=self.con)

        except ConnectionError as e:
            
            raise ConnectionError(f"[ ERROR ] Unable to get the store offers for the following location ({lat},{lon})") from e 

    def get_store_gasoline_types_offerings(self, state_name: str): 

        try:

            state_name: str = STATES_LOOKUP.get(state_name)
            return pd.read_sql(f"SELECT * FROM GetStoreFuelsOffering('{state_name}')" , con=self.con)

        except ConnectionError as e:
            raise ConnectionError(f"[ ERROR ] Unable to retrieve fuel grades for {state_name}") from e 

    def get_store_reivews(self, lat: float, lon: float):

        if not isinstance(lat, float) and not isinstance(lon, float):
            raise ValueError(f"[ ERROR ] (lat,lon) must be types of float not ({type(lat), type(lon)})")
        
        try: 
            query_result: 'DataFrame' =  pd.read_sql(f"SELECT * FROM GetStoreReviews({lat}, {lon})", con=self.con)
            return query_result            

        except ConnectionError as e:
            raise ConnectionError(f"[ ERROR ] Unable to find reviews for the following store location ({lat}, {lon})") from e 


    def get_store_location_by_state(self, state_name: str):

        if not INVERSE_STATES.get(state_name):
            raise ValueError(f"[ ERROR ] Unable to find the following US state: {state_name}") 
            
        query: str = """
        SELECT 
            sl.store_id,
            sl.gasstation_id,
            sl.country,
            sl.address,
            sl.zip_code,
            sl.region,
            sl.locality,
            sl.latitude,
            sl.longitude,
            sl.star_rating,
            sl.ratings_count

        FROM StoreLocation sl
        WHERE sl.region = '%s'  
        """ % (state_name)

        try:
            return pd.read_sql(query, con=self.con) 

        except ConnectionError as e: 
            raise ConnectionError(f"[ ERROR ] Unable to get store location for the following state: {state_name}") from e 


    def get_historical_gas_station_data(self, gas_station_name: str ):
        
        if not re.findall(r"[a-zA-Z]|\-|&|\/|\s|#|\+|.|’", gas_station_name): 
            raise ValueError(f"[ ERROR ] Illegal Chars inside gas_station_name {gas_station_name}")
 
        gasoline_df: 'DataFrame' = pd.read_sql(f"SELECT * FROM GasStation WHERE name = '{gas_station_name}' ", con=self.con)   
        
        if gasoline_df.shape[0] > 0: 
            gas_station_id: int = gasoline_df['gasstation_id'].tolist()[0]
            store_location_df: 'DataFrame' = pd.read_sql(f"SELECT * FROM StoreLocation sl WHERE sl.gasstation_id = {gas_station_id} " ,con=self.con).drop_duplicates() 
            store_id: str = ','.join( store_location_df['store_id'].astype(str).tolist())
            
            users_df: 'DataFrame' = pd.read_sql(f"SELECT * FROM Users WHERE store_id IN ({store_id})", con=self.con).drop_duplicates()  
            member_id: int = ','.join(users_df['member_id'].astype(str).apply(lambda row: "'%s'" % (row) ).tolist())
            reviews_df: 'DataFrame' = pd.read_sql(f"SELECT* FROM Reviews WHERE member_id IN ({member_id}) ", con=self.con).drop_duplicates()   
            
            cash_df: 'DataFrame' = pd.read_sql(f"SELECT * FROM CashPrices WHERE store_id IN ( {store_id})", con=self.con).drop_duplicates() 
            credit_df: 'DataFrame' = pd.read_sql(f"SELECT * FROM CreditPrices WHERE store_id IN ({store_id})", con=self.con).drop_duplicates() 
    
            df1: 'DataFrame' = pd.merge(left=gasoline_df[['gasstation_id','name', 'price_unit', 'pay_status' ]], right=store_location_df[[ 'gasstation_id', 'store_id', 'address', 'locality', 'zip_code', 'region' ]], on='gasstation_id', how='inner', suffixes=('_left', '') ).drop_duplicates()
            df2: 'DataFrame' = pd.merge(left=df1, right=users_df, on='store_id', how='inner', suffixes=('_left', '') ).drop_duplicates() 
            df3: 'DataFrame' = pd.merge(left=df2, right=reviews_df, on='member_id', how='inner' , suffixes=('_left', '') )
    
            payment_op_one: 'DataFrame' = pd.merge(left=df3, right=cash_df, on='store_id', how='inner', suffixes=('_left', '')  ).drop_duplicates() 
            payment_op_one['payment_type'] = ['cash'] * payment_op_one.shape[0] 
            
            payment_op_two: 'DataFrame' = pd.merge(left=df3, right=credit_df, on='store_id', how='inner', suffixes=('_left', '')  ).drop_duplicates()
            payment_op_two['payment_type'] = ['credit'] * payment_op_two.shape[0] 

            results: List = []
            results.extend(payment_op_one.to_dict(orient='records')) 
            results.extend(payment_op_two.to_dict(orient='records')) 
            
            return pd.DataFrame(results)

        return pd.DataFrame()

    def get_nearest_gas_station(self, state_name: str, lat: float, lon: float) :

        if not INVERSE_STATES.get(state_name):
            raise ValueError("[ ERROR ] Unable to find the give US state. Please try again !!!") 

        try:
            current_state_loc: 'DataFrame' = pd.read_sql(f"SELECT *  FROM StoreLocation WHERE region = '{state_name}'  ",con=self.con)
            current_store: 'DataFrame' = pd.DataFrame( [{'latitude':lat, 'longitude': lon} ] * current_state_loc.shape[0] )
            closest_stores: 'DataFrame' = pd.concat( [ current_state_loc, pd.Series(metrics.pairwise_distances(current_store, current_state_loc[['latitude', 'longitude']] )[0], name='distance' ).transpose() ], axis=1).sort_values(by='distance' )
            
            return closest_stores.query(f"latitude != {lat} and longitude != {lon} ") # diplay < 10 closests stores


        except ConnectionError as e:
            raise ConnectionError(f"[ ERROR ] Unable to find the nearest gas stations located at ({lat}, {lon})") from e
    
        
                

        


    























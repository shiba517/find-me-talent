import streamlit as st
# import kaggle
# from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import os.path
import pandas as pd

class FMT():
    def __init__(self):
        self.title = 'Find Me Talent'
        # self.kaggle_api = KaggleApi()
        # self.kaggle_api_auth = self.kaggle_api.authenticate()
        self.kaggle_ds_url = 'stefanoleone992/fifa-22-complete-player-dataset'
        self.kaggle_csv_name = 'players_22.csv'
        self.json_file_cleaned = 'players_22_cleaned.json'
        self.base_df = None
        self.df_columns_info = []

    def extract_and_unzip(self):
        if not os.path.isfile(self.kaggle_csv_name):
            self.kaggle_api.dataset_download_file(self.kaggle_ds_url,
                                                  file_name=self.kaggle_csv_name)
            with zipfile.ZipFile(self.kaggle_csv_name + '.zip', 'r') as zipref:
                zipref.extractall()

    def set_pandas_df(self):
        if os.path.isfile(self.kaggle_csv_name):
            self.base_df = pd.read_csv(self.kaggle_csv_name)

    def clean_pandas_df(self):
        if type(self.base_df) != "class 'pandas.core.frame.DataFrame'":
            # Cleaning player_positions column
            all_positions = []
            for key, value in self.base_df.iterrows():
                positions = value['player_positions'].split(',')
                positions_list = []
                for position in positions:
                    position_cleaned = position.replace(' ', '')
                    positions_list.append(position_cleaned)
                    if position_cleaned not in all_positions:
                        all_positions.append(position_cleaned)
                self.base_df.at[key, 'player_positions'] = ' '.join(positions_list)
            self.df_columns_info.append({'player_positions': all_positions})

    def create_for_pandas(self):
        def create_int_valued_columns():
            columns_list = []
            if type(self.base_df) != "class 'pandas.core.frame.DataFrame'":
                # Creating list of columns with an int value
                for column in self.base_df.columns:
                    for row in self.base_df[column]:
                        if isinstance(row, int):
                            columns_list.append(column)
                            break
                self.df_columns_info.append({'int_valued_columns': columns_list})

        # Running each function
        create_int_valued_columns()

    # Sets up base data for run_streamlit()
    def pre_run_streamlit(self):
        # self.extract_and_unzip()
        self.set_pandas_df()
        self.clean_pandas_df()
        self.create_for_pandas()


    # RUN THIS FUNCTION FOR STREAMLIT WEBSITE
    def run_streamlit(self):
        self.pre_run_streamlit()

        df = self.base_df

        st.title(self.title)

        st.sidebar.header('Filter options')
        # Collecting wanted data from user
        user_value_eur = st.sidebar.slider('Value', min_value=int(df['value_eur'].min()/1000000),
                                           max_value=int(df['value_eur'].max()/1000000),
                                           value=0,
                                           step=10)
        user_age = st.sidebar.slider('Age',
                                     min_value=int(df['age'].min()),
                                     max_value=int(df['age'].max()),
                                     value=int(df['age'].min()), step=1)
        user_player_positions = st.sidebar.selectbox('Position',
                                                     options=self.df_columns_info[0]['player_positions'])

        # Filtering the data based upon variables above
        def filtered_data():
            f_value_eur = user_value_eur * 1000000
            f_age = user_age
            f_player_positions = user_player_positions

            def make_query_statement():
                query_list = []
                query_statement = ''

                if f_value_eur != 0:
                    statement = 'value_eur < @f_value_eur'
                    if statement not in query_list:
                        query_list.append(statement)

                if f_age > 0:
                    statement = 'age < @f_age'
                    if statement not in query_list:
                        query_list.append(statement)

                if f_player_positions != 'ALL':
                    statement = '@f_player_positions in player_positions'
                    if statement not in query_list:
                        query_list.append(statement)

                # Now creating statement for querying
                for i in range(0, len(query_list)):
                    if i == 0:
                        query_statement += query_list[i]
                    else:
                        query_statement += ' & ' + query_list[i]

                return query_statement

            qdf = df.query(
                make_query_statement()
            )

            return qdf

        set_data = filtered_data()
        # DATABASE TO BE SHOWN
        st.dataframe(set_data)

        # Convert filtered database to a barchart
        bc_col_name = st.sidebar.multiselect(
            'Select category',
            options=self.df_columns_info[1]['int_valued_columns']
        )

        if st.sidebar.button('get bar chart'):
            filtered_by_col = pd.DataFrame(set_data[bc_col_name])
            st.subheader('Bar chart')
            st.bar_chart(filtered_by_col)




my_project = FMT()
my_project.run_streamlit()
# my_project.pre_run_streamlit()
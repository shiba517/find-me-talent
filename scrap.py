def filtered_info():
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
        # 'value_eur <= @f_value_eur & age < @f_age & player_positions in @f_player_positions'
        make_query_statement()
    )

    return qdf


# SHOW DATABASE
# if st.sidebar.button('filter'):
#     st.dataframe(filtered_info())
# else:
#     st.dataframe(filtered_info())

if st.sidebar.button('height'):
    x = df['age'].value_counts()
    st.bar_chart(x)
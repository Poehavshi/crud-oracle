import pandas as pd
import pyodbc
import streamlit as st

from config import CONNECTION_PARAMS


class MenuService:
    def __init__(self, cursor):
        self.cursor = cursor

    def read_whole_menu(self):
        self.cursor.execute("SELECT * FROM MENU")
        rows = []
        row = self.cursor.fetchone()
        while row:
            rows.append(list(row))
            row = self.cursor.fetchone()
        df = pd.DataFrame(rows, columns=['id', 'name', 'mass', 'calories', 'type', 'price', 'minutes']).set_index('id')
        return df

    def update_object(self, identifier, name, mass, calories, type, price, minutes):
        self.cursor.execute(f"UPDATE MENU"
                            f"  SET NAME = '{name}',"
                            f"      MASS = '{mass}',"
                            f"      CALORIES = '{calories}',"
                            f"      TYPE = '{type}',"
                            f"      PRICE = '{price}',"
                            f"      MINUTES = '{minutes}'"
                            f"WHERE ID = {identifier}; ")
        self.cursor.commit()

    def read_menu_composition(self):
        self.cursor.execute("SELECT MENU.NAME, COMPOSITION.COMPONENT, COMPOSITION.NUMB, COMPOSITION.UNIT "
                            "   FROM MENU, COMPOSITION "
                            "WHERE MENU.ID = COMPOSITION.ID")
        rows = []
        row = self.cursor.fetchone()
        while row:
            rows.append(list(row))
            row = self.cursor.fetchone()
        df = pd.DataFrame(rows, columns=['name', 'composition_name', 'numb', 'unit'])
        return df


def connect_to_db():
    connection_string = ';'.join([f"{key}={value}" for key, value in CONNECTION_PARAMS.items()])
    connection = pyodbc.connect(connection_string)
    return connection


def main():
    connection = connect_to_db()
    st.markdown("# Menu")
    service = MenuService(connection.cursor())
    st.dataframe(service.read_whole_menu())

    st.markdown("## Форма для модификации")
    st.text("Введите id объекта, который хотите поменять и введите новые значения для него")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        identifier = st.text_input("id")
    with col2:
        name = st.text_input("name")
    with col3:
        mass = st.text_input("mass")
    with col4:
        calories = st.text_input("calories")
    with col5:
        type = st.text_input("type")
    with col6:
        price = st.text_input("price")
    with col7:
        minutes = st.text_input("minutes")
    st.button("Модифицировать",
              on_click=lambda: service.update_object(identifier, name, mass, calories, type, price, minutes))
    # connection.close()
    st.markdown("## Состав блюд")
    st.dataframe(service.read_menu_composition())


if __name__ == '__main__':
    main()

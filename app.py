# # import streamlit as st
# # from dotenv import load_dotenv
# # import os
# # import pandas as pd
# # import snowflake.connector

# # load_dotenv()

# # st.title("🌍 Country Data Dashboard")

# # @st.cache_resource
# # def get_connection():
# #     return snowflake.connector.connect(
# #         user="snowtee6",
# #         password = os.getenv("SNOWFLAKE_PASSWORD"),
# #         account="QSAPKTH-CL67259",
# #         warehouse="COMPUTE_WH",
# #         database="COUNTRY_DB",
# #         schema="PUBLIC"
# #     )

# # conn = get_connection()

# # query = """
# # SELECT region, COUNT(*) AS total_countries, AVG(population) AS avg_population
# # FROM COUNTRIES_SILVER
# # GROUP BY region
# # """

# # df = pd.read_sql(query, conn)

# # st.subheader("📊 Countries by Region")
# # st.bar_chart(df.set_index("REGION")["TOTAL_COUNTRIES"])

# # st.subheader("📈 Average Population by Region")
# # st.dataframe(df)

# # st.metric("Total Regions", len(df))


# # import streamlit as st
# # import pandas as pd
# # import snowflake.connector
# # from dotenv import load_dotenv

# # load_dotenv()

# # @st.cache_resource
# # def get_connection():
# #     return snowflake.connector.connect(
# #         user=st.secrets["SNOWFLAKE_USER"],
# #         password=st.secrets["SNOWFLAKE_PASSWORD"],
# #         account=st.secrets["SNOWFLAKE_ACCOUNT"],
# #         warehouse="COMPUTE_WH",
# #         database="COUNTRY_DB",
# #         schema="PUBLIC"
# #     )

# # @st.cache_data
# # def load_data():
# #     conn = get_connection()
# #     query = "SELECT * FROM COUNTRIES_SILVER"
# #     return pd.read_sql(query, conn)

# # df = load_data()

# # st.title("🌍 Country Data Dashboard")

# # # ------------------------
# # # 🔹 Filters
# # # ------------------------
# # regions = st.multiselect(
# #     "Select Region",
# #     options=df["REGION"].dropna().unique(),
# #     default=df["REGION"].dropna().unique()
# # )

# # min_pop, max_pop = st.slider(
# #     "Population Range",
# #     int(df["POPULATION"].min()),
# #     int(df["POPULATION"].max()),
# #     (int(df["POPULATION"].min()), int(df["POPULATION"].max()))
# # )

# # filtered_df = df[
# #     (df["REGION"].isin(regions)) &
# #     (df["POPULATION"].between(min_pop, max_pop))
# # ]

# # # ------------------------
# # # 🔹 KPIs
# # # ------------------------
# # col1, col2, col3 = st.columns(3)

# # col1.metric("Total Countries", len(filtered_df))
# # col2.metric("Avg Population", int(filtered_df["POPULATION"].mean()))
# # col3.metric("Max Population", int(filtered_df["POPULATION"].max()))

# # # ------------------------
# # # 🔹 Charts
# # # ------------------------
# # st.subheader("Countries by Region")
# # st.bar_chart(filtered_df["REGION"].value_counts())

# # st.subheader("Population Distribution")
# # st.line_chart(filtered_df.sort_values("POPULATION")["POPULATION"])

# # # ------------------------
# # # 🔹 Table
# # # ------------------------
# # st.subheader("Data Preview")
# # st.dataframe(filtered_df)

# import streamlit as st
# import pandas as pd
# import snowflake.connector


# st.set_page_config(page_title="Country Data Dashboard", layout="wide")


# # -------------------------
# # CONNECTION (CACHED)
# # -------------------------
# @st.cache_resource
# def get_connection():
#     return snowflake.connector.connect(
#         user=st.secrets["SNOWFLAKE_USER"],
#         password=st.secrets["SNOWFLAKE_PASSWORD"],
#         account=st.secrets["SNOWFLAKE_ACCOUNT"],
#         warehouse="COMPUTE_WH",
#         database="COUNTRY_DB",
#         schema="PUBLIC"
#     )

# # -------------------------
# # LOAD DATA (CACHED)
# # -------------------------
# @st.cache_data(ttl=600)
# def load_data():
#     conn = get_connection()
#     query = """
#         SELECT country_name, region, population
#         FROM COUNTRIES_SILVER
#         WHERE population IS NOT NULL
#     """
#     return pd.read_sql(query, conn)

# df = load_data()


# ##############################
# # Last updated
# ##############################
# st.caption("Last refreshed: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"))



# # -------------------------
# # TITLE
# # -------------------------
# st.title("🌍 Country Analytics Dashboard")


# # -------------------------
# # SIDEBAR FILTERS
# # -------------------------
# st.sidebar.header("Filters")

# regions = st.sidebar.multiselect(
#     "Select Region",
#     options=df["REGION"].dropna().unique(),
#     default=df["REGION"].dropna().unique()
# )

# min_pop, max_pop = st.sidebar.slider(
#     "Population Range",
#     int(df["POPULATION"].min()),
#     int(df["POPULATION"].max()),
#     (int(df["POPULATION"].min()), int(df["POPULATION"].max()))
# )

# # # # ✅ SEARCH BOX IN SIDEBAR
# search_query = st.sidebar.text_input("🔍 Search country")

# # Sidebar search (autocomplete)
# country_list = sorted(df["COUNTRY_NAME"].dropna().unique())

# selected_country = st.sidebar.selectbox(
#     "🔎 Search country",
#     options=["All"] + country_list
# )


# # Apply filters
# filtered_df = df[
#     (df["REGION"].isin(regions)) &
#     (df["POPULATION"].between(min_pop, max_pop))
# ]

# st.caption(f"Showing {len(filtered_df)} countries")

# # Apply search filter
# if search_query:
#     filtered_df = filtered_df[
#         filtered_df["COUNTRY_NAME"]
#         .str.lower()
#         .str.contains(search_query.lower(), na=False)
# ]

# if filtered_df.empty:
#     st.warning("No data for selected filters")
#     st.stop()

# st.divider()

# # Apply selectbox filter    
# if selected_country != "All":
#     filtered_df = filtered_df[
#     filtered_df["COUNTRY_NAME"] == selected_country
# ]

# # -------------------------
# # KPIs
# # -------------------------
# col1, col2, col3 = st.columns(3)

# col1.metric("🌎 Total Countries", len(filtered_df))
# col2.metric("👥 Avg Population", f"{int(filtered_df['POPULATION'].mean()):,}")
# col3.metric("🏙 Max Population", f"{int(filtered_df['POPULATION'].max()):,}")


# # -------------------------
# # CHARTS
# # -------------------------
# st.subheader("Countries by Region")

# region_counts = filtered_df["REGION"].value_counts()
# st.bar_chart(region_counts)

# top10 = filtered_df.nlargest(10, "POPULATION")
# st.bar_chart(top10.set_index("COUNTRY_NAME")["POPULATION"])

# # add line chart for population distribution
# st.subheader("🔍 Country Drill-Down")

# selected = st.selectbox(
#     "Select a country to explore",
#     options=filtered_df["COUNTRY_NAME"].unique()
# )

# country_df = filtered_df[
#     filtered_df["COUNTRY_NAME"] == selected
# ]


# # -------------------------
# # DATA TABLE
# # -------------------------
# st.subheader("Data Preview")
# st.dataframe(filtered_df, use_container_width=True)


import streamlit as st
import pandas as pd
import snowflake.connector

st.set_page_config(page_title="Country Data Dashboard", layout="wide")

# -------------------------
# CONNECTION (CACHED)
# -------------------------
@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        user=st.secrets["SNOWFLAKE_USER"],
        password=st.secrets["SNOWFLAKE_PASSWORD"],
        account=st.secrets["SNOWFLAKE_ACCOUNT"],
        warehouse="COMPUTE_WH",
        database="COUNTRY_DB",
        schema="PUBLIC"
    )

# -------------------------
# LOAD DATA (CACHED)
# -------------------------
@st.cache_data(ttl=600)
def load_data():
    conn = get_connection()
    query = """
        SELECT country_name, region, population
        FROM COUNTRIES_SILVER
        WHERE population IS NOT NULL
    """
    return pd.read_sql(query, conn)

df = load_data()

# -------------------------
# HEADER
# -------------------------
st.title("🌍 Country Analytics Dashboard")
st.caption("Last refreshed: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"))

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=df["REGION"].dropna().unique(),
    default=df["REGION"].dropna().unique()
)

min_pop, max_pop = st.sidebar.slider(
    "Population Range",
    int(df["POPULATION"].min()),
    int(df["POPULATION"].max()),
    (int(df["POPULATION"].min()), int(df["POPULATION"].max()))
)

# ✅ Autocomplete dropdown
country_list = sorted(df["COUNTRY_NAME"].dropna().unique())
selected_country = st.sidebar.selectbox(
    "🔎 Search country",
    options=["All"] + country_list
)

# -------------------------
# APPLY FILTERS (CORRECT ORDER)
# -------------------------
filtered_df = df[
    (df["REGION"].isin(regions)) &
    (df["POPULATION"].between(min_pop, max_pop))
]

if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["COUNTRY_NAME"] == selected_country
    ]

# Stop if empty
if filtered_df.empty:
    st.warning("No data for selected filters")
    st.stop()

st.caption(f"Showing {len(filtered_df)} countries")
st.divider()

# -------------------------
# KPIs
# -------------------------
col1, col2, col3 = st.columns(3)

col1.metric("🌎 Total Countries", len(filtered_df))
col2.metric("👥 Avg Population", f"{int(filtered_df['POPULATION'].mean()):,}")
col3.metric("🏙 Max Population", f"{int(filtered_df['POPULATION'].max()):,}")

# -------------------------
# CHARTS
# -------------------------
st.subheader("Countries by Region")
st.bar_chart(filtered_df["REGION"].value_counts())

st.subheader("Top 10 Most Populated Countries")
top10 = filtered_df.nlargest(10, "POPULATION")
st.bar_chart(top10.set_index("COUNTRY_NAME")["POPULATION"])

# -------------------------
# DRILL-DOWN
# -------------------------
st.subheader("🔍 Country Drill-Down")

selected = st.selectbox(
    "Select a country to explore",
    options=filtered_df["COUNTRY_NAME"].unique()
)

country_df = filtered_df[
    filtered_df["COUNTRY_NAME"] == selected
]

if not country_df.empty:
    c1, c2, c3 = st.columns(3)

    c1.metric("🌎 Country", selected)
    c2.metric("👥 Population", f"{int(country_df['POPULATION'].values[0]):,}")
    c3.metric("🌍 Region", country_df["REGION"].values[0])

# -------------------------
# MAP (OPTIONAL)
# -------------------------
if "LATITUDE" in filtered_df.columns and "LONGITUDE" in filtered_df.columns:
    st.subheader("🗺 Country Map")
    st.map(filtered_df[["LATITUDE", "LONGITUDE"]].dropna())

# -------------------------
# DATA TABLE
# -------------------------
st.subheader("Data Preview")
st.dataframe(filtered_df, use_container_width=True)
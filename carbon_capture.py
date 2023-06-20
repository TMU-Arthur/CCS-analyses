import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
st.set_page_config(layout="centered")
st.title("Carbon capture information data visualization")

st.markdown("## Introduction to Carbon Capture and Storage(CCS)")
st.markdown('''**Carbon Capture and Storage (CCS)** is an innovative technology 
            that aims to tackle the pressing issue of climate change by reducing 
            greenhouse gas emissions from various industrial processes and power generation. 
            This approach involves capturing carbon dioxide (CO2) from large-scale emission sources, 
            such as power plants and industrial facilities, before it is released into the atmosphere. 
            The captured CO2 is then transported and stored deep underground in geological formations, 
            preventing its release into the air. CCS offers a promising solution to mitigate the impact of CO2 emissions, 
            as it enables the continued use of fossil fuels while significantly reducing their environmental footprint. 
            By preventing substantial amounts of CO2 from entering the atmosphere, 
            CCS has the potential to play a crucial role in achieving global climate goals and transitioning to a more sustainable and low-carbon future.''')
st.markdown("Therefore, in this project, we will analyze CCS projects around the globe and deliver our analyses.")
df = pd.read_csv("ccs.csv")


# st.dataframe(df)
search_df = df.astype(str)
search_by = st.selectbox("Search by", df.columns)
searchbox = st.text_input("Search for projects")
if searchbox:
    display_df = search_df[search_df[search_by].str.contains(searchbox, case=False)]
    if display_df.empty:
        st.warning("No projects found")
    else:
        st.dataframe(display_df)

company_df = df["Company"]
company_count = {}
for i in company_df.values:
    company_count[i] = company_count.get(i, 0)+1
company_sorted = sorted(company_count.items(), reverse = True, key = lambda x:x[1])

company_df = pd.DataFrame(company_sorted, columns = ["Company", "Projects"])
# company_df["Projects"].apply(lambda x: int(x))
company_df = company_df.astype({"Projects":int})

#Top CCS project companies
st.markdown("## Top CCS project companies")
top_companies = st.slider("Select the number of top companies", 5, 17, 5)
company_df = company_df.head(top_companies)

fig, ax = plt.subplots(figsize=(20, 8))
fig.set_tight_layout(True)
my_cmap = plt.get_cmap("Wistia")
plt.rcParams.update({'font.size': 8})
rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
ax.set_xlim(0,10)
barh = ax.barh(company_df['Company'], company_df['Projects'], color = my_cmap(rescale(company_df['Projects'])), align = "center")
ax.bar_label(barh, fontsize = 20)
plt.xlabel("Company count", fontsize = 20)
plt.ylabel("Project counts", fontsize = 20)
plt.title("Top %s companies in CCS"%(top_companies), fontsize = 30)
plt.grid(False)
plt.savefig("company_bar.png", transparent = True, dpi = 200, pad_inches = 0.5)
st.image("company_bar.png", caption="Top %s companies in CCS"%(top_companies))
st.markdown('''The organizations holding the most Carbon Capture and Storage (CCS) projects worldwide are predominantly academic institutions or government research organizations, 
            including Illinois State Geological Survey and the University of North Dakota, among others. 
            Not until the eighth position do we encounter a private corporation, E.ON, 
            which is responsible for a significant portion of Europe's infrastructure. 
            From this data, we can deduce that a majority of the carbon capture projects are still supported by government or academic entities, 
            with private companies making up a minor proportion of the market.''')
with open("company_bar.png", "rb") as file:
    btn = st.download_button(
            label="Download image",
            data=file,
            file_name="company_bar.png",
            mime="image/png"
          )


# Project types
st.markdown("## Project types")
type_df = df["Storage and/or Capture"]
type_count = {}
for i in type_df.values:
    type_count[i] = type_count.get(i, 0)+1
type_df = pd.DataFrame(list(type_count.items()), columns = ["Project types", "Projects"])
type_df = type_df.astype({"Projects":int})
st.dataframe(type_df)
fig, ax = plt.subplots(figsize=(20, 8))
fig.set_tight_layout(True)
ax.pie(type_df["Projects"],labels = type_df["Project types"])
plt.rcParams.update({'font.size': 20})
plt.savefig("type_pie.png", transparent = True, dpi = 200, pad_inches = 0.5)
st.image("type_pie.png", caption="Project types")
with open("type_pie.png", "rb") as file:
    btn = st.download_button(
            label="Download image",
            data=file,
            file_name="type_pie.png",
            mime="image/png"
          )

# Project location
st.markdown("## Project location")
location_df = df["Country Location"]
location_count = {}
for i in location_df.values:
    location_count[i] = location_count.get(i, 0)+1
location_sorted = sorted(location_count.items(), reverse = True, key = lambda x:x[1])

location_df = pd.DataFrame(location_sorted, columns = ["Country", "Projects"])
location_df = location_df.astype({"Projects":int})

top_location = st.slider("Select the number of top locations", 5, 11, 5)
location_df =location_df.head(top_location)

fig, ax = plt.subplots(figsize=(20, 8))
fig.set_tight_layout(True)
my_cmap = plt.get_cmap("Wistia")
plt.rcParams.update({'font.size': 8})
rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
ax.set_xlim(0,200)
barh = ax.barh(location_df['Country'], location_df['Projects'], color = my_cmap(rescale(location_df['Projects'])), align = "center")
ax.bar_label(barh, fontsize = 20)
plt.xlabel("Location count", fontsize = 20)
plt.ylabel("Project counts", fontsize = 20)
plt.title("Top %s Project locations"%(top_location), fontsize = 30)
plt.grid(False)
plt.savefig("location_bar.png", transparent = True, dpi = 200, pad_inches = 0.5)
st.image("location_bar.png", caption="Top %s Project locations"%(top_location))
with open("location_bar.png", "rb") as file:
    btn = st.download_button(
            label="Download image",
            data=file,
            file_name="location_bar.png",
            mime="image/png"
          )

#Project date
st.markdown("## Project initiated by years")
selected_year = st.slider("Select range of years", 1978, 2022, (2000, 2020))
year_lower = selected_year[0]
year_upper = selected_year[1]
year_range = [int(i) for i in range(year_lower, year_upper+1)]

year_df = df["Project Date"].dropna()
year_df = year_df.apply(lambda x: x[-4:])
year_df.apply(lambda x: int(x))
year_count = {}
for i in year_df:
    year_count[i] = year_count.get(i, 0)+1
year_sorted = sorted(year_count.items(), key = lambda x:x[0])
year_sorted = [i for i in year_sorted if int(i[0]) in range(year_lower, year_upper+1)]

year_df = pd.DataFrame(year_sorted, columns = ["Year", "Projects"])
# year_df = year_df.astype({"Year":str, "Projects":int})

fig, ax = plt.subplots(figsize=(20, 8))
fig.set_tight_layout(True)
my_cmap = plt.get_cmap("Wistia")
plt.rcParams.update({'font.size': 15})
rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
ax.bar(year_df['Year'], year_df['Projects'], color = my_cmap(rescale(year_df['Projects'])), align = "center")
plt.xlabel("Year", fontsize = 20)
plt.ylabel("Project counts", fontsize = 20)
plt.title("Projects initiated by years, from %s to %s"%(year_lower, year_upper), fontsize = 30)
plt.grid(False)
plt.savefig("year_bar.png", transparent = True, dpi = 200, pad_inches = 0.5)
st.image("year_bar.png", caption="Projects initiated by years, from %s to %s"%(year_lower, year_upper))
with open("year_bar.png", "rb") as file:
    btn = st.download_button(
            label="Download image",
            data=file,
            file_name="year_bar.png",
            mime="image/png"
          )

#Most common technology
st.markdown("## Most used technology in CCS")
top_tech = st.slider("Select the number of top technologies", 5, 17, 5)


tech_df = df["Capture Technology"].dropna()
tech_count = {}
for i in tech_df.values:
    tech_count[i] = tech_count.get(i, 0)+1
tech_sorted = sorted(tech_count.items(), reverse = True, key = lambda x:x[1])

tech_df = pd.DataFrame(tech_sorted, columns = ["Capture Technology", "Projects"])
tech_df = tech_df.astype({"Projects":int})
tech_df = tech_df.head(top_tech)

fig, ax = plt.subplots(figsize=(20, 8))
fig.set_tight_layout(True)
my_cmap = plt.get_cmap("Wistia")
plt.rcParams.update({'font.size': 8})
rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
ax.set_xlim(0,60)
barh = ax.barh(tech_df["Capture Technology"].astype('str'), tech_df['Projects'], color = my_cmap(rescale(tech_df['Projects'])), align = "center")
ax.bar_label(barh, fontsize = 20)
plt.xlabel("Projects", fontsize = 20)
plt.ylabel("Capture Technology", fontsize = 20)
plt.title("Top %s technology of CCS"%(top_tech), fontsize = 30)
plt.grid(False)
plt.savefig("tech_bar.png", transparent = True, dpi = 200, pad_inches = 0.5)
st.image("tech_bar.png", caption="Top %s technology of CCS"%(top_tech))
with open("tech_bar.png", "rb") as file:
    btn = st.download_button(
            label="Download image",
            data=file,
            file_name="tech_bar.png",
            mime="image/png"
          )

#Status
st.markdown("## Project status")
status_df = df["Overall Status"]
status_count = {}
for i in status_df.values:
    status_count[i] = status_count.get(i, 0)+1
status_sorted = sorted(status_count.items(), reverse = True, key = lambda x:x[1])

status_df = pd.DataFrame(status_sorted, columns = ["Status", "Projects"])
status_df = status_df.astype({"Projects":int})

fig, ax = plt.subplots(figsize=(20, 8))
fig.set_tight_layout(True)
my_cmap = plt.get_cmap("Wistia")
plt.rcParams.update({'font.size': 8})
rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
ax.set_xlim(0,170)
barh = ax.barh(status_df["Status"].astype('str'), status_df['Projects'], color = my_cmap(rescale(status_df['Projects'])), align = "center")
ax.bar_label(barh, fontsize = 20)
plt.xlabel("Projects", fontsize = 20)
plt.ylabel("Status", fontsize = 20)
plt.title("Project status", fontsize = 30)
plt.grid(False)
plt.savefig("status_bar.png", transparent = True, dpi = 200, pad_inches = 0.5)
st.image("status_bar.png", caption="Project status")
with open("status_bar.png", "rb") as file:
    btn = st.download_button(
            label="Download image",
            data=file,
            file_name="status_bar.png",
            mime="image/png"
          )

#Combustion/Separation
st.markdown("## Combustion/Separation")
comb_sep_df = df["Combustion / Separation"]
comb_sep_count = {}
for i in comb_sep_df.values:
    comb_sep_count[i] = comb_sep_count.get(i, 0)+1
comb_sep_sorted = sorted(comb_sep_count.items(), reverse = True, key = lambda x:x[1])

comb_sep_df = pd.DataFrame(comb_sep_sorted, columns = ["Combustion/Separation", "Projects"])
comb_sep_df = comb_sep_df.astype({"Projects":int})

fig, ax = plt.subplots(figsize=(20, 8))
fig.set_tight_layout(True)
my_cmap = plt.get_cmap("Wistia")
plt.rcParams.update({'font.size': 8})
rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
ax.set_xlim(0,200)
barh = ax.barh(comb_sep_df["Combustion/Separation"].astype('str'), comb_sep_df['Projects'], color = my_cmap(rescale(comb_sep_df['Projects'])), align = "center")
ax.bar_label(barh, fontsize = 20)
plt.xlabel("Projects", fontsize = 20)
plt.ylabel("Combustion/Separation", fontsize = 20)
plt.title("Combustion/Separation", fontsize = 30)
plt.grid(False)
plt.savefig("comb_sep_bar.png", transparent = True, dpi = 200, pad_inches = 0.5)
st.image("comb_sep_bar.png", caption="Combustion/Separation")
with open("comb_sep_bar.png", "rb") as file:
    btn = st.download_button(
            label="Download image",
            data=file,
            file_name="comb_sep_bar.png",
            mime="image/png"
          )







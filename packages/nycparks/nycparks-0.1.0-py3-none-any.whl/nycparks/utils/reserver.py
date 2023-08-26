
import requests
import pandas as pd
import os
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from nycparks.utils.times import search_times, weekday_number_to_day

class TennisReserver:

    def __init__(self,) -> None:

        self.base_url = "https://www.nycgovparks.org"
        self.reservation_url = os.path.join(self.base_url, "tennisreservation")

    def reserve(self, locations: list) -> dict:

        courts = self.get_courts(self.fetch(self.reservation_url))

        availability = pd.DataFrame()
        for location in locations: 
            location_link = courts[courts["Location"].str.lower().str.contains(location)]["link"].values[0]

            temp_df =  self.get_availability(self.fetch(location_link)).rename(columns = {"Location": location})
            if availability.empty == True:
                availability = temp_df

            elif temp_df.empty == True:
                continue
            else:
                availability = availability.merge(temp_df, on=["Day", "Time"], how="outer")

        return availability.sort_values(by=["Day", "Time"]).reset_index(drop=True)


    def fetch(self, link: str):
        
        headers = {
                'user-agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            }

        session = requests.Session()
        response = session.get(link, headers=headers)
        
        assert response.status_code == 200

        return response


    def get_courts(self, response) -> pd.DataFrame:

        soup = BeautifulSoup(response.content, parser='lxml')
        table = soup.find("table", { 'class' : 'table table-bordered'})

        rows = []
        
        trs = table.find_all('tr')
        headerow = self._get_row(trs[0], 'th') + ["link"]
        
        if headerow: # if there is a header row include first
            rows.append(headerow)
            trs = trs[1:]
        
        for tr in trs: # for every table row
            rows.append(self._get_row(tr, 'td') ) # data row    


        return pd.DataFrame(rows[1:], columns=rows[0])



    def _get_row(self, tr, coltag: str) -> list:   
    
        if coltag == "th":
            return [td.get_text(strip=True) for td in tr.find_all(coltag)]  
    
        elif coltag == "td":
            row_data = []
            for td in tr.find_all('td'):
                text = td.get_text(strip=True)
                text = text.rstrip("View Availability/Reserve")
                row_data.append(text)
            for link in tr.find_all('a', href=True):
                row_data.append(
                    self.base_url + link["href"]
                )
            return row_data


    def get_availability(self, response) -> pd.DataFrame:
    
        tables = pd.read_html(response.content)
        availability = []
    
        start_idx = None
        
        for i in range(len(tables)):
    
            if "court" in "".join(tables[i]).lower():
    
                if start_idx == None:
                    start_idx = i
                    
                day = (datetime.now() + timedelta(days=i-start_idx+1)).date()
                times = search_times[weekday_number_to_day[day.weekday()]]
    
                temp_table = tables[i].rename(columns={"Unnamed: 0": "Times"})
                temp_table = temp_table[temp_table["Times"].isin(times)].set_index("Times")
                
                for i, row in temp_table.replace("Not Available", None).dropna(how="all").iterrows():

                    availability.append({
                        "Day": str(day),
                        "Time": i,
                        "Location": row.dropna().index.tolist(),
                    })
    
        return pd.DataFrame(availability)
    


    def make_bool_df(self, df: pd.DataFrame, label: str, locations: list) -> pd.DataFrame:

        df = df.copy()
        
        for i in locations:
            if i in df.columns:
                df[i] = df[i].map(lambda x: True if x else False)
            else: 
                df[i] = False

        df["Label"] = label
        df = df.melt(id_vars=["Day", "Time", "Label"], value_vars=locations, var_name="Location", value_name="Courts",) \
                .query("Courts==True")
        
        return df


    def find_new(self, new: pd.DataFrame, old: pd.DataFrame, locations: list) -> pd.DataFrame:

        new_bool = self.make_bool_df(new, label="new", locations=locations)
        old_bool = self.make_bool_df(old, label="old", locations=locations)
        
        return pd.concat([new_bool, old_bool]) \
                        .drop_duplicates(subset=[i for i in new_bool.columns if i != "Label"] , keep=False) \
                        .query("Label == 'new'")
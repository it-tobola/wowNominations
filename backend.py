import pandas as pd
import notion_df as nd
nd.pandas()

# Notion connection information
notion_token = "secret_omL8nzIdOZySUeAtSOCHm0bUNh2ydXdohuePKPBXkxm"
# employee df
ee_db_id = "03764697bdf74f2b938313815cf62069"
ee_url = "https://www.notion.so/03764697bdf74f2b938313815cf62069?v=e856d446c1a44cfcb8857b014f591284"
ee_df = pd.DataFrame(nd.download(ee_db_id, api_key=notion_token, resolve_relation_values=True))

# wow award df
wow_db_id = "96c47cd2ff3941829267a40b6223b5c9"
wow_url = "https://www.notion.so/96c47cd2ff3941829267a40b6223b5c9?v=36f63746938544a0b941d14f94b2ec21&pvs=4"
wow_df = pd.DataFrame(nd.download(wow_db_id, api_key=notion_token, resolve_relation_values=True))

# Create a dataframe of active employees for nomination
active_ee = ee_df[["EE Code", "Full Name", "Home Base"]][ee_df["Status"] == "Active"].reset_index()
## Remove the previous index column from df
active_ee = active_ee[["EE Code", "Full Name", "Home Base"]]

# Create a list of departments/programs available
programs = active_ee["Home Base"].unique().tolist()


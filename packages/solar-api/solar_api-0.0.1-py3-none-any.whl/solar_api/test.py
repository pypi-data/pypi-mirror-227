from solar_api.api import SolarApi

solar = SolarApi("http://localhost:9002","s35ZfmYJfnhgaxAVHAKLdZPcJMmo0bkGhLBqTfe5qE64PQMlQlxuooL5tndhgdNq")
#ds = solar.get_dataset("def")
#ds.num_rows_per_request = 2
#df = ds.fetch_all_df()
#print(df)
ds = solar.get_dataset("new_dataset1")
ds.describe()
with open('C:\\Users\\AdamKamor\\Repos\\solar\\python_sdk\\solar_api\\promt-response.csv','r') as f:
    solar.upload_file(f, 'blah.csv')

with open('C:\\Users\\AdamKamor\\Repos\\solar\\python_sdk\\solar_api\\promt-response.csv','r') as f:    
    ds.upload_then_add_file("blah2.csv", f)

all_files = solar.get_files()
ds.add_file(all_files[0].id)

ds.describe()
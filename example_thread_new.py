'''
pip install futures

Thread call to census using summary module.
'''
 
import pandas as pd
 
from census import summary
 
from concurrent.futures import ThreadPoolExecutor, as_completed
   
cnt = 0
for df1 in pd.read_csv('tornado_data_no_zeroes.csv', iterator=True, chunksize=1000):
 
    print(f'Record: {cnt * 1000}', end='\r')
 
    cnt+=1
  
    df1['income'] = ""
    df1['population_density'] = ""
 
    def write_file(index, lat, lon):
        # try:
            print(index)
  
            results = summary(lat, lon)
            return index, results
 
        # except:
        #     return "error"
 
    def runner():
        threads= []
        with ThreadPoolExecutor(max_workers=20) as executor:
            for index, row in df1.iterrows():
                lat = row['Starting_Lat']
                lon = row['Starting_Lon']
              
                threads.append(executor.submit(write_file, index, lat, lon))
               
            for task in as_completed(threads):
                index = task.result()[0]
                results = task.result()[1]
                if results['Status'] == 'Ok':

                    df1.loc[index, 'income'] = results['income']
                    df1.loc[index, 'population_density'] = str(round(results['population_density'],2))
    
                    print(task.result()[0])
       
    runner()
 
    #-------------------------------------------------------------------------
  
    if cnt == 1:
        df1.to_csv("tornado_data_census.csv", index=False)
    else:
        df1.to_csv("tornado_data_census.csv", index=False, header=False, mode='a')
 
 
# print(df1.head())
 
import pandas as pd
import os, glob, re, json


path = os.getcwd()
if not os.path.exists('bicams.xlsx'):
    bicams_df = pd.DataFrame(columns=['Identifier', 'Name', 'Age', 'DateOfBirth', 'Male', 'StudentYears', 'CVLT_fin', 'RVP_avg', 'RT_avg', 'SDMT', 'TestDate'])

try:
    bicams_df = pd.read_excel('/Users/szabi/Desktop/bicams/bicams.xlsx', dtype='object')
    bicams_df.pop('Unnamed: 0')
except FileNotFoundError:
    pass

identifiers = [str(i) for i in bicams_df["Identifier"]]
patient_dirs = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) ]
# tests = ['CVLT-II', 'RVP', 'RT', 'SDMT']
for pat_dir in patient_dirs:
    tests = os.listdir(f"{pat_dir}/Tests")
    patient = pd.read_json(f"{pat_dir}/info.json", orient="index").T
    ident = patient["Identifier"][0]
    name = patient["Name"][0]
    dob = patient['DateOfBirth'][0]
    age = patient['Age'][0]
    stud_yrs = patient['StudentYears'][0]
    male = patient['Male'][0]
    if not ident in identifiers:
        test_results = []
        for test_name in tests:
            test_files = os.listdir(f'{pat_dir}/Tests/{test_name}/1')[-1]
            # print(f"{patient}/Tests/{test_name}/{test_files}")
            with open(f"{pat_dir}/Tests/{test_name}/1/{test_files}") as jsonFile:
                jsonObject = json.load(jsonFile)
                if "FinalScore" in jsonObject:
                    cvlt_score = jsonObject["FinalScore"]
                    test_dt = jsonObject["CreateDate"]
                    test_results.append({'CVLT_fin': cvlt_score, 'TestDate': test_dt})
                    # print(f"{test_name}-{jsonObject['FinalScore']}")
                elif "Results" in jsonObject:
                    if test_name == "RVP":
                        if jsonObject["Results"]:
                            rvp_score = sum(jsonObject['Results'])/len(jsonObject['Results'])
                        else:
                            rvp_score = 0
                        # print(f"{patient}{test_name}-{jsonObject['Results']}")
                        test_results.append({'RVP_avg':rvp_score})

                    else:
                        if jsonObject["Results"]:
                            rt_score = sum(jsonObject['Results'])/len(jsonObject['Results'])
                        else:
                            rt_score = 0
                        # print(f"{test_name}-{jsonObject['Results']}")
                        test_results.append({'RT_avg':rt_score})

                elif "Result" in jsonObject:
                    sdmt_score = jsonObject['Result']
                    # print(f"{test_name}-{jsonObject['Result']}")
                    test_results.append({'SDMT':sdmt_score})
        bicams_df = bicams_df.append({'Name':name, 'Age':age, 'DateOfBirth':dob, 'Identifier':ident, 'StudentYears':stud_yrs, 'Male':male, 'TestDate':test_results[0]['TestDate'], 'CVLT_fin':test_results[0]['CVLT_fin'], 'RVP_avg':test_results[1]['RVP_avg'], 'RT_avg':test_results[2]['RT_avg'], 'SDMT':test_results[3]['SDMT'],}, ignore_index=True).drop_duplicates(subset=['Identifier'])
        # print(test_results)
bicams_df.to_excel('bicams.xlsx')
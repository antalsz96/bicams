import pandas as pd
import os, glob, json

# Kiszedi minden új beteg tesztadatait, azonosítóit és hozzáadja a bicams.xlsx excelhez
# Az új betegeknek a script mappájában kell lenniük

bicams_df = pd.read_excel('/Users/szabi/Desktop/bicams/bicams.xlsx', dtype='object')
bicams_df.pop('Unnamed: 0')
identifiers = [str(i) for i in bicams_df["Identifier"]]
path = os.getcwd()
patient_dirs = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) ]
tests = ['CVLT-II', 'RVP', 'RT', 'SDMT']
for dir in patient_dirs:
    patient = pd.read_json(f"{dir}/info.json", orient="index").T
    ident = patient["Identifier"][0]
    name = patient["Name"][0]
    dob = patient['DateOfBirth'][0]
    age = patient['Age'][0]
    stud_yrs = patient['StudentYears'][0]
    male = patient['Male'][0]
    if not ident in identifiers:
        for test in tests:
            test_data = glob.glob(f"{dir}/Tests/{test}/1/*.json")
            if test_data:   # if it's not an empty list
                for test_fil in test_data:
                    # print(test_fil)
                    # data = pd.read_json(test_fil, lines=True, orient="index")
                    with open(test_fil) as jsonFile:
                        jsonObject = json.load(jsonFile)
                        jsonObject["Identifier"] = ident        # adds Identifier to patient json (not to testData.json!)
                    # print(jsonObject["PatientId"])
                    # print(jsonObject["Identifier"])
                    # df = df.append(jsonObject, ignore_index=True)
                    # print(jsonObject)
                    if test == 'CVLT-II':
                        cvlt_score = jsonObject['FinalScore']
                        p_id = jsonObject['Identifier']
                        test_dt = jsonObject['CreateDate']
                        # print(f"CVLT_fin: {cvlt_score}, {p_id}")
                        # cvlt = {'CVLT_fin':[cvlt_score], 'Identifier':p_id}
                        # cvlt_df = pd.DataFrame(data=[cvlt_score], index=[p_id], columns=['CVLT_fin'])
                        # appendix = appendix.append({'Identifier':p_id, 'CVLT_fin':cvlt_score}, ignore_index=True)
                    elif test == 'RVP':
                        rvp_res = jsonObject['Results']
                        p_id = jsonObject['Identifier']
                        if rvp_res:
                            rvp_score = sum(rvp_res)/len(rvp_res)
                            # print(f"RVP_avg: {rvp_score}, {p_id}")
                            # rvp = {'RVP_avg':[rvp_score], 'Identifier':p_id}
                            # rvp_df = pd.DataFrame(data=[rvp_score], index=[p_id], columns=['RVP_avg'])
                            # appendix = appendix.append({'Identifier':p_id, 'RVP_avg':rvp_score}, ignore_index=True)
                    elif test == 'RT':
                        rt_res = jsonObject['Results']
                        p_id = jsonObject['Identifier']
                        if rt_res:
                            rt_score = sum(rt_res)/len(rt_res)
                            # print(f"RT_avg: {rt_score}, {p_id}")
                            # rt = {'RT_avg':[rt_score], 'Identifier':p_id}
                            # rt_df = pd.DataFrame(data=[rt_score], index=[p_id], columns=['RT_avg'])
                            # appendix = appendix.append({'Identifier':p_id, 'RT_avg':rt_score}, ignore_index=True)
                    else:
                        sdmt_score = jsonObject['Result']
                        p_id = jsonObject['Identifier']
                        # print(f"SDMT: {sdmt_score}, {p_id}")
                        # sdmt = {'SDMT':[sdmt_score], 'Identifier':p_id}
                        # sdmt_df = pd.DataFrame(data=[sdmt_score], index=[p_id], columns=['SDMT'])
                        # appendix = appendix.append({'Identifier':p_id, 'SDMT':sdmt_score}, ignore_index=True)
                    bicams_df = bicams_df.append({'Name':name, 'Age':age, 'DateOfBirth':dob, 'Identifier':p_id, 'StudentYears':stud_yrs, 'Male':male, 'TestDate':test_dt, 'CVLT_fin':cvlt_score, 'RVP_avg':rvp_score, 'RT_avg':rt_score, 'SDMT':sdmt_score,}, ignore_index=True).drop_duplicates(subset=['Identifier'])
                    
bicams_df.to_excel('bicams.xlsx')
import pandas
import glob
import re
import gzip
import os 

def as_string(x):
    try:
        return str(int(x))
    except:
        return x

def clean_commune_code(row):
    if "SN" in row["CODE_COMMUNE"]:
        return as_string(row["CODE_COMMUNE"].split("SN")[0])
    elif "056AR" in row["CODE_COMMUNE"]: #paris
        return str(int(row["CODE_COMMUNE"].split("AR")[1]) + 100)
    elif "123SR" in row["CODE_COMMUNE"]: #lyon
        return str(int(row["CODE_COMMUNE"].split("SR")[1]) + 380)
    elif "SR" in row["CODE_COMMUNE"]:
        return as_string(row["CODE_COMMUNE"].split("SR")[0])
    elif "055AR" in row["CODE_COMMUNE"]: #marseilles
        return str(int(row["CODE_COMMUNE"].split("AR")[1]) + 200)
    else:
        return as_string(row["CODE_COMMUNE"])

def clean_dept_name(x):
    if x in set(["ZA", "ZB", "ZC", "ZD", "ZS"]): #guadeloupe, martinique, guyanne, reunion, St pierre et miquelon
        return "97"
    elif x in set(["ZP", "ZN"]): #polynesie, nouvelle caledonie
    	return "98"
    else:
        return as_string(x)



# these are all the files that concern communes with less than 3500 inhabitants
files = glob.glob("data/election_data/municipales_2008_part_[12]/*.csv.gz")

all_data =  pandas.DataFrame(columns=["CODE_DEPARTEMENT", "CODE_COMMUNE", "NOMBRE_INSCRITS", "NOMBRE_ABSTENTION"])

for filename in files:

	data = pandas.read_csv(filename, sep=",", compression="gzip")
	# we keep only what we are interested in and since there is a row per member of the list we remove duplicates
	data = data[["CODE_DEPARTEMENT", "CODE_COMMUNE", "NOMBRE_INSCRITS","NOMBRE_ABSTENTION"]].drop_duplicates(["CODE_DEPARTEMENT", "CODE_COMMUNE"])
	data["CODE_COMMUNE"] = data.apply(clean_commune_code, axis = 1)
	data["CODE_DEPARTEMENT"] = data["CODE_DEPARTEMENT"].apply(clean_dept_name)
	all_data = all_data.append(data)

# files concerning communes with more than 3500 inhabitants
filename = "data/election_data/municipales_2008_part_3/Tour 1-Table 1.csv.gz"
data = pandas.read_csv(filename, sep=",", compression="gzip")
data = data[["CODE_DU_DEPARTEMENT","CODE_DE_LA_COMMUNE","INSCRITS","ABSTENTIONS"]]
data.columns = ["CODE_DEPARTEMENT", "CODE_COMMUNE", "NOMBRE_INSCRITS","NOMBRE_ABSTENTION"]
data["CODE_COMMUNE"] = data.apply(clean_commune_code, axis = 1)
data["CODE_DEPARTEMENT"] = data["CODE_DEPARTEMENT"].apply(clean_dept_name)
all_data = all_data.append(data)

#aggregate on the mapping
mapping = pandas.read_csv("data/raw_data/correspondance-code-insee-code-postal.csv.gz", sep=";", compression="gzip")
mapping["CODE_COMMUNE"] = mapping["code_comm"].apply(as_string)
mapping["CODE_DEPARTEMENT"] = mapping["code_dept"].apply(as_string)

final = pandas.merge(mapping, all_data, how="inner", on=["CODE_DEPARTEMENT", "CODE_COMMUNE"])
final = final.drop(["CODE_DEPARTEMENT", "CODE_COMMUNE"], axis = 1)

# replace columns"names
final = final.drop(["id_geofla", "code_comm", "code_cant", "code_arr", "code_dept", "code_reg"], axis = 1)
final.columns = ["INSEE_CODE", "POSTAL_CODE", "COMMUNE_NAME", "DEPARTEMENT_NAME", "REGION_NAME", "STATUS", "ALTITUDE", "AREA", "POPULATION", "CENTER", "SHAPE", "REGISTERED", "ABSTENTION"]

# normalize abstention by registered
final["REGISTERED"] = final["REGISTERED"].apply(float)
final["ABSTENTION"] = final["ABSTENTION"].apply(float)
final = final[final["REGISTERED"] > 0]
final["ABSTENTION"] = final["ABSTENTION"]/final["REGISTERED"]
final["ABSTENTION"] = (final["ABSTENTION"] - final["ABSTENTION"].min()) / (final["ABSTENTION"].max() - final["ABSTENTION"].min())

final.to_csv("data/elections.csv", index = False)

# compress output
f_in = open("data/elections.csv", "rb")
f_out = gzip.open("data/elections.csv.gz", "wb")
f_out.writelines(f_in)
f_out.close()
f_in.close()
os.remove("data/elections.csv")

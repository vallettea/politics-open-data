import pandas
import glob
import re
import gzip
import os 

def clean_header(filename, sep):
	lines = gzip.open(filename, "rb").readlines()
	headers = lines[0].split(sep)
	headers = map(lambda x: re.sub("[^a-zA-Z0-9\s]", "", x).upper(), headers)

	lines[0] = sep.join(headers)	
	out_file = gzip.open(filename, "wb")
	for line in lines: 
		out_file.write(line)
	out_file.close()

def as_string(x):
    try:
        return str(int(x))
    except:
        return x

def clean_commune_code(row):
    if "SN" in row["CODE COMMUNE"]:
        return as_string(row["CODE COMMUNE"].split("SN")[0])
    elif "056AR" in row["CODE COMMUNE"]: #paris
        return str(int(row["CODE COMMUNE"].split("AR")[1]) + 100)
    elif "123SR" in row["CODE COMMUNE"]: #lyon
        return str(int(row["CODE COMMUNE"].split("SR")[1]) + 380)
    elif "SR" in row["CODE COMMUNE"]:
        return as_string(row["CODE COMMUNE"].split("SR")[0])
    elif "055AR" in row["CODE COMMUNE"]: #marseilles
        return str(int(row["CODE COMMUNE"].split("AR")[1]) + 200)
    else:
        return as_string(row["CODE COMMUNE"])

def clean_dept_name(x):
    if x in set(["ZA", "ZB", "ZC", "ZD", "ZS"]): #guadeloupe, martinique, guyanne, reunion, St pierre et miquelon
        return "97"
    elif x in set(["ZP", "ZN"]): #polynesie, nouvelle caledonie
    	return "98"
    else:
        return as_string(x)



# these are all the files that concern communes with less than 3500 inhabitants
files = glob.glob("data/election_data/municipales_2008_part_[12]/*.csv.gz")

all_data =  pandas.DataFrame(columns=["CODE DPARTEMENT", "CODE COMMUNE", "NOMBRE INSCRITS", "NOMBRE ABSTENTION"])

for filename in files:
	# replace the headers so it has no accents
	clean_header(filename, sep=",")

	data = pandas.read_csv(filename, sep=",", compression="gzip")
	# we keep only what we are interested in and since there is a row per member of the list we remove duplicates
	data = data[["CODE DPARTEMENT", "CODE COMMUNE", "NOMBRE INSCRITS","NOMBRE ABSTENTION"]].drop_duplicates(["CODE DPARTEMENT", "CODE COMMUNE"])
	data["CODE COMMUNE"] = data.apply(clean_commune_code, axis = 1)
	data["CODE DPARTEMENT"] = data["CODE DPARTEMENT"].apply(clean_dept_name)
	all_data = all_data.append(data)

# files concerning communes with more than 3500 inhabitants
filename = "data/election_data/municipales_2008_part_3/Tour 1-Table 1.csv.gz"
clean_header(filename, sep=",")
data = pandas.read_csv(filename, sep=",", compression="gzip")
data = data[["CODE DU DPARTEMENT","CODE DE LA COMMUNE","INSCRITS","ABSTENTIONS"]]
data.columns = ["CODE DPARTEMENT", "CODE COMMUNE", "NOMBRE INSCRITS","NOMBRE ABSTENTION"]
data["CODE COMMUNE"] = data.apply(clean_commune_code, axis = 1)
data["CODE DPARTEMENT"] = data["CODE DPARTEMENT"].apply(clean_dept_name)
all_data = all_data.append(data)

#aggregate on the mapping
mapping = pandas.read_csv("raw_data/correspondance-code-insee-code-postal.csv.gz", sep=";", compression="gzip")
mapping["CODE COMMUNE"] = mapping["code_comm"].apply(as_string)
mapping["CODE DPARTEMENT"] = mapping["code_dept"].apply(as_string)

final = pandas.merge(mapping, all_data, how="inner", on=["CODE DPARTEMENT", "CODE COMMUNE"])
final = final.drop(["CODE DPARTEMENT", "CODE COMMUNE"], axis = 1)

# replace columns"names
final = final.drop(["id_geofla", "code_comm", "code_cant", "code_arr", "code_dept", "code_reg"], axis = 1)
final.columns = ["INSEE_CODE", "POSTAL_CODE", "COMMUNE_NAME", "DEPARTEMENT_NAME", "REGION_NAME", "STATUS", "ALTITUDE", "AREA", "POPULATION", "CENTER", "SHAPE", "REGISTERED", "ABSTENTION"]

final.to_csv("cleaned_data/elections.csv", sep=";", index = False)

# compress output
f_in = open("cleaned_data/elections.csv", "rb")
f_out = gzip.open("cleaned_data/elections.csv.gz", "wb")
f_out.writelines(f_in)
f_out.close()
f_in.close()
os.remove("cleaned_data/elections.csv")

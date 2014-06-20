import pandas
import re
import numpy as np
import gzip
import os

data = pandas.read_csv("data/elections.csv.gz", sep=",", compression="gzip")

partial = False

# retail
# http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/equip-serv-commerce/equip-serv-commerce-com-12.zip
retails = pandas.read_csv("data/raw_data/insee/equip-serv-commerce-com.csv.gz", sep=";", compression="gzip")
retails["INSEE_CODE"] = retails["CODGEO"].apply(str)
retails = retails.drop(["CODGEO","LIBGEO","REG","DEP","ARR","CV","ZE2010","UU12010","Pop_2010", "Unnamed: 32"], axis=1)
if partial: retails = retails[["HYPERMARCHE", "SUPERMARCHE", "SUPERETTE", "EPICERIE", "BOULANGERIE", "BOUCHERIE_CHARCUTERIE", "POISSONNERIE", "LIBRAIRIE_PAPETERIE_JOURNAUX", "MAGASIN_DE_VETEMENTS", "INSEE_CODE"]]
data = pandas.merge(data, retails, how="left", on="INSEE_CODE")

# habitat
# http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/rp2010/chiffres-cles/base-cc-logement-2010/base-cc-logement-2010.zip
habitat = pandas.read_csv("data/raw_data/insee/base-cc-logement-2010.csv.gz", sep=";", compression="gzip")
habitat["INSEE_CODE"] = habitat["CODGEO"].apply(str)
habitat = habitat.drop(["CODGEO","REG","DEP","ARR","CV","ZE2010","ID_MODIF_GEO","LIBGEO"], axis=1)
columns_to_keep = filter(lambda x: len(habitat[x].dropna()) > 10000, habitat.columns)
habitat = habitat[columns_to_keep]
if partial: habitat = habitat[["LOGEMENTS_EN_2010","RESIDENCES_PRINCIPALES_EN_2010","RES_SECONDAIRES_ET_LOGTS_OCCASIONNELS_EN_2010","LOGEMENTS_VACANTS_EN_2010", "INSEE_CODE"]]
data = pandas.merge(data, habitat, how="left", on="INSEE_CODE")

# entertainement
# http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/equip-sport-loisir-socio/equip-sport-loisir-socio-com-12.zip
entertainement = pandas.read_csv("data/raw_data/insee/entertainement.csv.gz", sep=",", compression="gzip")
entertainement["INSEE_CODE"] = entertainement["CODGEO"].apply(str)
entertainement = entertainement.drop(["CODGEO","LIBGEO","REG","DEP","ARR","CV","UNITE_URBAINE","POPULATION_MUNICIPALE_2010"], axis=1)
if partial: entertainement = entertainement[["BASSIN_DE_NATATION","BOULODROME","TENNIS","DOMAINE_SKIABLE","CENTRE_EQUESTRE","ATHLETISME","TERRAIN_DE_GOLF","PLATEAU_EXTERIEUR_OU_SALLE_MULTISPORTS","SALLE_DE_COMBAT","SPORTS_NAUTIQUES","PORT_DE_PLAISANCE_MOUILLAGE","CINEMA_","THEATRE", "INSEE_CODE"]]
data = pandas.merge(data, entertainement, how="left", on="INSEE_CODE")

# companies
# http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/base-cc-demo-entreprises/base-cc-demo-entreprises-12.zip
companies = pandas.read_csv("data/raw_data/insee/base-cc-demo-entreprises-12.csv.gz", sep=";", compression="gzip")
companies["INSEE_CODE"] = companies["CODGEO"].apply(str)
companies = companies.drop(["CODGEO","LIBGEO"], axis=1)
if partial: companies = companies[["CREATIONS_D_ENTR_EN_2012","ENTREPRISES_EN_2012","DONT_ETS_DU_COMMERCE_EN_2012", "INSEE_CODE"]]
data = pandas.merge(data, companies, how="left", on="INSEE_CODE")

#population
# http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/rp2010/chiffres-cles/base-cc-evol-struct-pop-2010/base-cc-evol-struct-pop-2010.zip
population = pandas.read_csv("data/raw_data/insee/base-cc-evol-struct-pop-2010.csv.gz", sep=";", compression="gzip")
population["INSEE_CODE"] = population["CODGEO"].apply(str)
population = population.drop(["CODGEO","REG","DEP","ARR","CV","ZE2010","ID_MODIF_GEO","LIBGEO"], axis=1)
if partial: population = population[["POPULATION_EN_2010","NAISSANCES_1999-2010","DECES_1999-2010","POP_0-14_ANS_EN_2010","POP_15-29_ANS_EN_2010","POP_30-44_ANS_EN_2010","POP_45-59_ANS_EN_2010","POP_60-74_ANS_EN_2010","POP_75_ANS_OU_PLUS_EN_2010","INSEE_CODE"]]
data = pandas.merge(data, population, how="left", on="INSEE_CODE")

# families
# http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/rp2010/chiffres-cles/base-cc-couples-familles-menages-2010/base-cc-couples-familles-menages-2010.zip
families = pandas.read_csv("data/raw_data/insee/base-cc-coupl-fam-men-2010.csv.gz", sep=",", compression="gzip")
families["INSEE_CODE"] = families["CODGEO"].apply(str)
families = families.drop(["CODGEO","REG","DEP","ARR","CV","ZE2010","ID_MODIF_GEO","LIBGEO"], axis=1)
if partial: families = families[["MENAGES_1_PERSONNE_EN_2010_", "MENAGES_EN_2010_", "FAM_COUPLE_AVEC_ENFANT_EN_2010_", "FAM_MONOPARENTALES_EN_2010_", "INSEE_CODE"]]
data = pandas.merge(data, families, how="left", on="INSEE_CODE")

# salaries (only 50k)
# http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/base-cc-salaire-net-horaire-moyen/base-cc-salaire-net-horaire-moyen-10.zip
salaries = pandas.read_csv("data/raw_data/insee/base-cc-salaire-net-horaire-moyen-10.csv.gz", sep=";", compression="gzip")
salaries["INSEE_CODE"] = salaries["CODGEO"].apply(str)
salaries = salaries.drop(["CODGEO", "REG","DEP","ARR","CV","ZE2010","EPCI","LIBGEO"], axis=1)
if partial: salaries = salaries[["SALAIRE_NET_HORAIRE_MOYEN_EN_2010","SALAIRE_NET_HOR_MOY_CADRES_EN_2010","SALAIRE_NET_HOR_MOYEN_PROF_INTER_EN_2010","SALAIRE_NET_HOR_MOYEN_EMPLOYES_EN_2010","SALAIRE_NET_HOR_MOYEN_OUVRIERS_QUALIFIES_EN_2010","SALAIRE_NET_HOR_MOYEN_OUVRIERS_NON_QUALIFIES_EN_2010","INSEE_CODE"]]
data = pandas.merge(data, salaries, how="left", on="INSEE_CODE")

# revenues
# http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/base-cc-rev-fisc-loc-menage/base-cc-rev-fisc-loc-menage-10.zip
revenues = pandas.read_csv("data/raw_data/insee/REVME_COM-Table 1.csv.gz", sep=",", compression="gzip")
revenues["INSEE_CODE"] = revenues["CODGEO"].apply(str)
revenues = revenues.drop(["CODGEO", "REG","DEP","ARR","CV","ZE2010","EPCI","LIBGEO"], axis=1)
revenues = revenues.fillna(0) 
if partial: revenues = revenues[["RFM_2010_NOMBRE_DE_MENAGES_FISCAUX", "RFM_2010_NOMBRE_PERSONNES_DES_MENAGES_FISCAUX", "RFM_2010_2EME_QUARTILE_PAR_UC_", "INSEE_CODE"]]
data = pandas.merge(data, revenues, how="left", on="INSEE_CODE")


# medical employments
# http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/equip-serv-medical-para/equip-serv-medical-para-com.zip
medical = pandas.read_csv("data/raw_data/insee/equip-serv-medical-para-com.csv.gz", sep=";", compression="gzip")
medical["INSEE_CODE"] = medical["CODGEO"].apply(str)
medical = medical.drop(["CODGEO","LIBGEO","REG","DEP","ARR","CV","ZE2010","UU2010","POP_2010", "Unnamed: 32"], axis=1)
if partial: medical = medical[["MEDECIN_OMNIPRATICIEN", "CHIRURGIEN_DENTISTE", "SAGE-FEMME", "INFIRMIER", "INSEE_CODE"]]
data = pandas.merge(data, medical, how="left", on="INSEE_CODE")

# unemployment
# http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/base-cc-chomage/base-cc-chomage-t3-2012.zip
unemployment = pandas.read_csv("data/raw_data/insee/base-cc-chomage-t3-2012.csv.gz", sep=";", compression="gzip")
unemployment["INSEE_CODE"] = unemployment["CODGEO"].apply(str)
unemployment = unemployment.drop(["CODGEO","REG","DEP","ARR","CV","ZE2010","EPCI","LIBGEO"], axis=1)
unemployment = unemployment.fillna(0) 
if partial: unemployment = unemployment[["DEFM_CAT_ABC_DE_LONGUE_DUREE_AU_31_DECEMBRE_2010", "INSEE_CODE"]]
data = pandas.merge(data, unemployment, how="left", on="INSEE_CODE")

# categories socio prof
socioprof = pandas.read_csv("data/raw_data/insee/effectifs_par groupes_socioprof.csv.gz", sep=";", compression="gzip")
socioprof["INSEE_CODE"] = socioprof["COM"].apply(str)
socioprof = socioprof.drop(["COM","LIBGEO"], axis=1)
data = pandas.merge(data, socioprof, how="left", on="INSEE_CODE")

# tourism
# http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/base-cc-tourisme/base-cc-tourisme-13.zip
tourism = pandas.read_csv("data/raw_data/insee/TOURM_COM-Table 1.csv.gz", sep=",", compression="gzip")
tourism["INSEE_CODE"] = tourism["CODGEO"].apply(str)
tourism = tourism.drop(["CODGEO","IDENTIFIANT_DES_MODIFICATIONS_GEOGRAPHIQUES","LIBELLE_GEOGRAPHIQUE"], axis=1)
if partial: tourism = tourism[[ "HOTELS_EN_2009", "CAMPINGS_CLASSES_EN_2009", "RESIDENCES_SECONDAIRES_EN_2010", "INSEE_CODE"]]
data = pandas.merge(data, tourism, how="left", on="INSEE_CODE")

# services
# http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/equip-serv-particuliers/equip-serv-particuliers-com-12.zip
services = pandas.read_csv("data/raw_data/insee/services.csv.gz", sep=",", compression="gzip")
services["INSEE_CODE"] = services["CODGEO"].apply(str)
services = services.drop(["CODGEO","LIBGEO","REG","DEP","ARR","CV","ZONE_D_EMPLOI","UNITE_URBAINE","POPULATION_2010","AGENCE_DE_TRAVAIL_TEMPORAIRE", "RESTAURANT","AGENCE_IMMOBILIERE","BLANCHISSERIE-TEINTURERIE","SOINS_DE_BEAUTE"], axis=1)
if partial: services = services[["POLICE","TRESORERIE","GENDARMERIE","BANQUE","BUREAU_DE_POSTE", "INSEE_CODE"]]
data = pandas.merge(data, services, how="left", on="INSEE_CODE")



# education
# http://www.data.gouv.fr/fr/dataset/effectifs-d-etudiants-inscrits-dans-les-etablissements-et-les-formations-de-l-enseignement-superieur
education = pandas.read_csv("data/raw_data/atlastES_R01_R11.csv.gz", sep=",", compression= "gzip")
education = education[education["RENTREE"] == 2008]
education = education[education["NIVEAU_GEO"] == "COMMUNE"]
education = education[["GEO_ID","REGROUPEMENT","SECTEUR","SEXE","EFFECTIF"]]
education = education[education["REGROUPEMENT"] != "TOTAL"]

def mergeCats(cols):
    if cols["SEXE"] == 1 : sexe = "M"
    else: sexe = "F"
    return "%s_%s_" % (cols["REGROUPEMENT"], cols["SECTEUR"]) + sexe

education["CATEGORIE"] = education.apply(mergeCats, axis=1)
education = education.drop(["REGROUPEMENT","SECTEUR","SEXE"], axis=1)
p = education.pivot(index="GEO_ID", columns="CATEGORIE", values="EFFECTIF")
p["INSEE_CODE"] = map(str, p.index)
p = p.fillna(0)
if partial: p = p[["CPGE_PU_F","CPGE_PU_M","EC_ART_PU_F","EC_ART_PU_M","EC_JUR_PU_F","EC_JUR_PU_M","EC_PARAM_PU_F","EC_PARAM_PU_M","STS_PU_F","STS_PU_M","UNIV_PU_F","UNIV_PU_M","INSEE_CODE"]]
data = pandas.merge(data, p, how="left", on="INSEE_CODE")


# taxes
# http://www.data.gouv.fr/fr/dataset/impot-de-solidarite-sur-la-fortune
taxes = pandas.read_csv("data/raw_data/ISF 2011-Table 1.csv.gz", sep=",", compression="gzip")
taxes = taxes[["INSEE_CODE","NB_ISF","MEAN_PATRIMOINE","MEAN_ISF"]]
taxes["INSEE_CODE"] = taxes["INSEE_CODE"].apply(lambda x : re.sub("[^\d]+", "", x))
taxes["NB_ISF"] = taxes["NB_ISF"].apply(lambda x : int(re.sub("[^\d]+", "", x)))
taxes["MEAN_ISF"] = taxes["MEAN_ISF"].apply(lambda x : int(re.sub("[^\d]+", "", x)))
taxes["MEAN_PATRIMOINE"] = taxes["MEAN_PATRIMOINE"].apply(lambda x : int(re.sub("[^\d]+", "", x)))
taxes = taxes.fillna(0)
data = pandas.merge(data, taxes, how="left", on="INSEE_CODE")


# help agriculture
# http://www.data.gouv.fr/fr/dataset/aides-percues-par-les-personnes-morales-au-titre-de-la-politique-agricole-commune
agriculture = pandas.read_csv("data/raw_data/pac.csv.gz", sep=";", compression="gzip")
agriculture["PAC"] = agriculture["MONTANT_TOTAL"].apply(lambda x: float(x.replace(",", ".")))
agriculture["POSTAL_CODE"] = agriculture["CODE_POSTAL_DE_LA_COMMUNE_DE_RESIDENCE"].apply(lambda x: "%05d" % int(x))
agriculture = agriculture[["POSTAL_CODE", "PAC"]]
aggregated = agriculture.groupby("POSTAL_CODE").sum()
aggregated["POSTAL_CODE"] = aggregated.index
data = pandas.merge(data, aggregated, how="left", on="POSTAL_CODE")


# AOC
aoc = pandas.read_csv("data/raw_data/AOC.csv.gz", sep=";", compression="gzip")
aoc["AOC"] = aoc["Aire geographique"]
def cleanAOC(x):
    try:    
        return "%05d" % int(x)
    except:
        return np.NaN

aoc["INSEE_CODE"] = aoc["CI"].apply(cleanAOC)
aoc = aoc.dropna(subset=["INSEE_CODE"], axis=0)
aoc = aoc[["INSEE_CODE", "AOC"]]
aggregated = aoc.groupby("INSEE_CODE").count()
aggregated["INSEE_CODE"] = aggregated.index
data = pandas.merge(data, aggregated, how="left", on="INSEE_CODE")

# finally get longitude and latitude 
def mkLat(x):
	try:
		return x.split(",")[0]
	except:
		return np.NaN
def mkLon(x):
	try:
		return x.split(",")[1]
	except:
		return np.NaN
data["LATITUDE"] = data["CENTER"].apply(mkLat)
data["LONGITUDE"] = data["CENTER"].apply(mkLon)

########################
data = data.fillna(0) 
########################

data.to_csv("data/communes.csv", sep=",", index=False)

if not partial:
	# compress output
	f_in = open("data/communes.csv", "rb")
	f_out = gzip.open("data/communes.csv.gz", "wb")
	f_out.writelines(f_in)
	f_out.close()
	f_in.close()
	os.remove("data/communes.csv")


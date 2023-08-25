import pandas as pd

"""
Leer del Excel/Base de datos
Construir un dicconario groups
Escribir resultados en Excel/Base de datos
Pisamos los resultados viejos?
Deberiamos llevar algun tipo de registro por las dudas?

groups va a tener la pinta:
{id_grupo:{
    auto-refresh: a,
    lazy-load: l,
    impressions_percentage: ip,
    score: B/M/R
    }
}

techo
piso
cuanto varia para mejor
cuanto varia para peor
R se mantiene igual
"""

#Todos estos numeros son %

cantidad_grupos = 100

def calculate_new_group_percentages(groups_dict,positive_variation,negative_variation,max_points,min_points):

    #en esta funcion vamos a ver como moidificamos los % de los grupos    
    for group in groups_dict.values():        
        actual_group_points = group["impressions-percentage"]

        if group["score"] == "B":
            group["impressions-percentage"] = min(max_points, actual_group_points + positive_variation)
        if group["score"] == "M":
            group["impressions-percentage"] =  max(min_points,actual_group_points - negative_variation)

    modified_percentages = groups_dict

    return modified_percentages



def build_groups_dict(groups_excel):

    groups_dict = {}

    for i in range(cantidad_grupos):

        auto_refresh = groups_excel.loc[i].at["Auto-refresh"]
        lazy_load = groups_excel.loc[i].at["Lazy-Load"]
        impressions_percentage = groups_excel.loc[i].at["Percentage of Impressions"]
        score = groups_excel.loc[i].at["Score"]

        groups_dict[i] = {"auto-refresh":auto_refresh,"lazy-load":lazy_load,"impressions-percentage":impressions_percentage,"score":score}

    return groups_dict


def update_groups(groups_dict):
    
    #crear el dataframe

    df = pd.DataFrame(columns=['Auto-refresh','Lazy-Load','Percentage of Impressions','Score'])
    row_list = []

    for i in range(cantidad_grupos):
        auto_refresh = groups_dict[i]["auto-refresh"]
        lazy_load = groups_dict[i]["lazy-load"]
        impressions_percentage = groups_dict[i]["impressions-percentage"]
        score = groups_dict[i]["score"]

        row_list.append([auto_refresh,lazy_load,impressions_percentage,score])

    # create extension
    df_extended = pd.DataFrame(row_list, columns=df.columns)

    # concatenate to original
    complete_df = pd.concat([df, df_extended])

    #pasarlo al excel

    complete_df.to_excel('groups.xlsx', index=False)

    return complete_df


groups_dataframe = pd.read_excel('groups.xlsx')

groups_dict = build_groups_dict(groups_dataframe)
groups_dict_updated = calculate_new_group_percentages(groups_dict,3,3,200,10)
update_groups(groups_dict_updated)
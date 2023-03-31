# Create your views here.
from django.shortcuts import render
from .forms import JsonFileUploadForm
from .models import MyModel
from sqlalchemy import create_engine

# Import standard libraries
import json
import pandas as pd
from toolz import interleave
import numpy as np
import re


# Import local libraries
from .codes import (
    publication_type_output,
    level_of_assignment_output,
    student_gender_output,
    admin_strand_output,
    edu_setting_output,
    outcome_type_codes,
    countries,
)
from .funcs import(
    get_data,
    get_metadata,
    get_outcome_data_lvl1,
    get_outcome_data_lvl2
)

from django.shortcuts import render
from .models import MyModel

def toolkit_prim_out_data(data):
    """ Get toolkit primary uotcome data """
    smd_df = get_outcome_data_lvl1(data=data, attribute_text="SMD", column_prefix="smd_")
    sesmd_df = get_outcome_data_lvl1(data=data, attribute_text="SESMD", column_prefix="se_")

    outcometype_df = get_outcome_data_lvl2(data=data, attribute_codes=outcome_type_codes, column_prefix="out_type_")

    df = pd.concat([outcometype_df, smd_df, sesmd_df], axis=1)[list(interleave([outcometype_df, smd_df, sesmd_df]))]

    col_list = df.filter(regex = 'out_type').columns.tolist()

    for c in col_list:
        #df.loc[df[c].str[0] == 'Toolkit primary outcome', 'outcol'] = c
        dft = df[df[c].notnull()][c].apply(lambda x: x if 'Toolkit primary outcome' in x else None) 
        indexlist = dft[dft.notnull()].index 
        df.loc[df.index.isin(indexlist), 'outcol'] = c 
    
    df['smdcol'] = df['outcol'].str.replace('out_type','smd')
    df['sesmdcol'] = df['outcol'].str.replace('out_type','se')

    df['out_type'] = df.apply(lambda x: df.at[x.name, x['outcol']] if pd.notnull(x['outcol']) else 'NA', axis=1)
    df['smd_value'] = df.apply(lambda x: df.at[x.name, x['smdcol']] if pd.notnull(x['outcol']) else 'NA', axis=1)
    df['sesmd_value'] = df.apply(lambda x: df.at[x.name, x['sesmdcol']] if pd.notnull(x['outcol']) else 'NA', axis=1)

    tool_smd = df['smd_value']
    tool_se = df['sesmd_value']

    return tool_smd, tool_se


def reading_prim_out_data(data):
    """ Get Reading primary uotcome data """
    smd_df = get_outcome_data_lvl1(data=data, attribute_text="SMD", column_prefix="smd_")
    sesmd_df = get_outcome_data_lvl1(data=data, attribute_text="SESMD", column_prefix="se_")

    outcometype_df = get_outcome_data_lvl2(data=data, attribute_codes=outcome_type_codes, column_prefix="out_type_")

    df = pd.concat([outcometype_df, smd_df, sesmd_df], axis=1)[list(interleave([outcometype_df, smd_df, sesmd_df]))]

    col_list = df.filter(regex = 'out_type').columns.tolist()

    for c in col_list:
        dft = df[df[c].notnull()][c].apply(lambda x: x if 'Reading primary outcome' in x else None) 
        indexlist = dft[dft.notnull()].index 
        df.loc[df.index.isin(indexlist), 'outcol'] = c 
    
    df['smdcol'] = df['outcol'].str.replace('out_type','smd')
    df['sesmdcol'] = df['outcol'].str.replace('out_type','se')

    df['out_type'] = df.apply(lambda x: df.at[x.name, x['outcol']] if pd.notnull(x['outcol']) else 'NA', axis=1)
    df['smd_red_value'] = df.apply(lambda x: df.at[x.name, x['smdcol']] if pd.notnull(x['outcol']) else 'NA', axis=1)
    df['sesmd_red_value'] = df.apply(lambda x: df.at[x.name, x['sesmdcol']] if pd.notnull(x['outcol']) else 'NA', axis=1)

    red_smd = df['smd_red_value']
    red_se = df['sesmd_red_value']

    return red_smd, red_se


def science_prim_out_data(data):
    """ Get Science primary uotcome data """
    smd_df = get_outcome_data_lvl1(data=data, attribute_text="SMD", column_prefix="smd_")
    sesmd_df = get_outcome_data_lvl1(data=data, attribute_text="SESMD", column_prefix="se_")

    outcometype_df = get_outcome_data_lvl2(data=data, attribute_codes=outcome_type_codes, column_prefix="out_type_")

    df = pd.concat([outcometype_df, smd_df, sesmd_df], axis=1)[list(interleave([outcometype_df, smd_df, sesmd_df]))]

    col_list = df.filter(regex = 'out_type').columns.tolist()

    for c in col_list:
        dft = df[df[c].notnull()][c].apply(lambda x: x if 'Science primary outcome' in x else None) 
        indexlist = dft[dft.notnull()].index 
        df.loc[df.index.isin(indexlist), 'outcol'] = c 
    
    
    df['smdcol'] = df['outcol'].str.replace('out_type','smd')
    df['sesmdcol'] = df['outcol'].str.replace('out_type','se')

    df['out_type'] = df.apply(lambda x: df.at[x.name, x['outcol']] if pd.notnull(x['outcol']) else 'NA', axis=1)
    df['smd_sci_value'] = df.apply(lambda x: df.at[x.name, x['smdcol']] if pd.notnull(x['outcol']) else 'NA', axis=1)
    df['sesmd_sci_value'] = df.apply(lambda x: df.at[x.name, x['sesmdcol']] if pd.notnull(x['outcol']) else 'NA', axis=1)

    sci_smd = df['smd_sci_value']
    sci_se = df['sesmd_sci_value']

    return sci_smd, sci_se


def upload_json(request):

    if request.method == 'POST' and 'upload_button' in request.POST:
        form = JsonFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # load the file data from the TemporaryUploadedFile object
            data = json.load(request.FILES['json_file'])

            # Get toolkit primary outcome data
            tool_smd, tool_se = toolkit_prim_out_data(data)

            # Get Reading primary outcome data
            red_smd, red_se = reading_prim_out_data(data)

            # Get Science primary outcome data
            sci_smd, sci_se = science_prim_out_data(data)

            # Get individual level data frames
            processed_data = get_data(data, publication_type_output, "text_field")
            level_assign = get_data(data, level_of_assignment_output, "level_assign")
            student_gender = get_data(data, student_gender_output, "student_gender")
            eppi_id = get_metadata(data, "ItemId", "eppi_id")
            author_df = get_metadata(data, "ShortTitle", "short_title")
            year_df = get_metadata(data, "Year", "year")
            admin_strand_data = get_data(data, admin_strand_output, "admin_strand_data")
            edu_setting_data = get_data(data, edu_setting_output, "edu_setting_data")
            title_df = get_metadata(data, "Title", "main_title")
            url_df = get_metadata(data, "URL", "url")
            abstract_df = get_metadata(data, "Abstract", "abstract")
            country_df = get_data(data, countries, "loc_country_raw")

            # THESE WORK TO RETAIN SQUARE BRACKETS BUT I CAN'T THEN PLOT THEM WITH D3 (NEED {})
            # Retain square brackets where originally presented
            """ country_df['loc_country_raw'] = country_df['loc_country_raw'].astype(str)
            country_df['loc_country_raw'] = country_df['loc_country_raw'].str.replace("[", "[")

            admin_strand_data['admin_strand_data'] = admin_strand_data['admin_strand_data'].astype(str)
            admin_strand_data['admin_strand_data'] = admin_strand_data['admin_strand_data'].str.replace("[", "[") """

            # Replace these values with your actual PostgreSQL credentials
            db_url = 'postgresql://jonathanreardon:jonpass@localhost/linux'

            # Create an SQLAlchemy engine
            engine = create_engine(db_url)

            # Concatenate all data into one large pd.dataframe
            merged_data = pd.concat([
                eppi_id, 
                url_df,
                country_df,
                author_df,
                title_df,
                year_df,
                abstract_df,
                tool_smd,
                tool_se,
                red_smd,
                red_se,
                sci_smd,
                sci_se,
                admin_strand_data, 
                edu_setting_data,
                processed_data, 
                level_assign, 
                student_gender], axis=1)

            # Replace 'your_table_name' with the actual table name you want to use
            merged_data.to_sql(MyModel._meta.db_table, engine, if_exists='replace')

            # Fetch all rows from the table
            all_data = MyModel.objects.all()
            has_data = all_data.exists()

            #########################################
            #/ GET LEVEL OF ASSIGNMENT DATA FOR D3 /#
            #########################################
            
            # Convert from pandas dataframe to json for d3
            json_str1 = level_assign.to_json(orient ='index')
            data_dict1 = json.loads(json_str1)
            level_assign_list = [v['level_assign'][0] for v in data_dict1.values()]

            data1 = {}
            for level in set(level_assign_list):
                data1[level] = level_assign_list.count(level)

            # Convert the dictionary to JSON string
            assign_levels = json.dumps(list(data1.items()))

            ######################################
            #/ GET PUBLICATION TYPE DATA FOR D3 /#
            ######################################

            # Convert from pandas dataframe to json for d3
            json_str2 = edu_setting_data.to_json(orient ='index')
            data_dict2 = json.loads(json_str2)
            edu_setting_data_list = [v['edu_setting_data'][0] for v in data_dict2.values()]

            data2 = {}
            for type in set(edu_setting_data_list):
                data2[type] = edu_setting_data_list.count(type)

            # Convert the dictionary to JSON string
            edu_setting_levels = json.dumps(list(data2.items()))

            ##############################
            #/ GET SMD TYPE DATA FOR D3 /#
            ##############################

            # Concatenate the two dataframes along axis=1 to create a new dataframe with two columns
            combined_df = pd.concat([tool_smd, tool_se], axis=1)
            smd_combined_csv = combined_df.to_csv(index=False)

            #######################
            #/ GET STUDY NUMBERS /#
            #######################

            study_num = len(eppi_id)

            ####################################
            #/ GET STUDENT GENDER DATA FOR D3 /#
            ####################################

            student_gender = student_gender.astype(str).groupby('student_gender').size().reset_index(name='value')
            student_gender = student_gender.rename(columns={'student_gender': 'name'})
            student_gender = student_gender.rename(columns={'value': 'count'})
            total_count = student_gender['count'].sum()
            student_gender['value'] = (student_gender['count'] / total_count) * 100
            student_gender['value'] = round(student_gender['value'], 2)
            student_gender = student_gender.drop('count', axis=1)
            student_gender['name'] = student_gender['name'].str.strip('[]')
            student_gender['name'] = student_gender['name'].str.replace("'", '"')

            # Use the modified data dictionary
            print(student_gender)
            student_gender['name'] = student_gender['name'].str.replace(r'"', '')

            student_gender = student_gender.to_json(orient='records')

            print(student_gender)

            # Pass contentx to template for rendering
            context = {'form': form, 
                       'data': all_data, 
                       'has_data': has_data, 
                       'assign_levels': assign_levels, 
                       'edu_setting_levels': edu_setting_levels,
                       'smd_combined_csv': smd_combined_csv,
                       'student_gender': student_gender,
                       'study_num': study_num}

            return render(request, 'upload_json.html', context)

    else:
        form = JsonFileUploadForm()
        context = {'form': form}

    return render(request, 'upload_json.html', context)


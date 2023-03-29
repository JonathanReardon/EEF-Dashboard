import pandas as pd

def clean_up(df):
    df.replace('\r', ' ', regex=True, inplace=True)
    df.replace('\n', ' ', regex=True, inplace=True)
    df.replace(':', ' ',  regex=True, inplace=True)
    df.replace(';', ' ',  regex=True, inplace=True)
    return df


def get_data(data, codes, colname):
    df = []
    for var in range(len(codes)):
        holder = []
        for section in range(len(data["References"])):
            if "Codes" in data["References"][section]:
                holderfind = []
                for study in range(len(data["References"][section]["Codes"])):
                    for key, value in codes[var].items():
                        if key == data["References"][section]["Codes"][study]["AttributeId"]:
                            holderfind.append(value)
                if len(holderfind) == 0:
                    holderfind = "NA"
                holder.append(holderfind)
        df.append(holder)

    df = pd.DataFrame(df)
    df = df.T
    df.replace('\r', ' ', regex=True, inplace=True)
    df.replace('\n', ' ', regex=True, inplace=True)
    df.replace(':', ' ',  regex=True, inplace=True)
    df.replace(';', ' ',  regex=True, inplace=True)
    df.columns = [colname]
    return df


def get_metadata(data, var, colname):
    varlist = []
    for section in range(len(data["References"])):
        if data["References"][section][var]:
            varlist.append(data["References"][section][var])
        else:
            varlist.append("NA")

    for i in varlist:
        i=str(i)
    varlist = [[i] for i in varlist]
    

    df = pd.DataFrame(varlist)
    df.replace('\r', ' ', regex=True, inplace=True)
    df.replace('\n', ' ', regex=True, inplace=True)
    df.replace(':', ' ',  regex=True, inplace=True)
    df.replace(';', ' ',  regex=True, inplace=True)
    df.columns = [colname]
    return df


def get_outcome_lvl1(data, var):
    outcome_number=[]
    for study in range(len(data["References"])):
        if "Outcomes" in data["References"][study]:
            outcome_number.append(len(data["References"][study]["Outcomes"]))
    varlist = []
    for section in range(len(data["References"])):
        holder = []
        if "Outcomes" in data["References"][section]:
            for subsection in range(max(outcome_number)):
                if subsection < len(data["References"][section]["Outcomes"]):
                    holder.append(data["References"][section]["Outcomes"][subsection][var])
                else:
                    holder.append("NA")
            varlist.append(holder)
        else:
            for i in range(max(outcome_number)):
                holder.append("NA")
            varlist.append(holder)
    return varlist


def get_outcome_lvl2(data, var):
    varlist = []
    for variable in range(len(var)):
        for study in range(len(data["References"])):
            if "Codes" in data["References"][study]:
                if "Outcomes" in data["References"][study]:
                    outerholder = []
                    for item in range(len(data["References"][study]["Outcomes"])):
                        innerholderholder = []
                        if "OutcomeCodes" in data["References"][study]["Outcomes"][item]:
                            for subsection in range(len(data["References"][study]["Outcomes"][item]["OutcomeCodes"]["OutcomeItemAttributesList"])):
                                for key, value in var[variable].items():
                                    if key == data["References"][study]["Outcomes"][item]["OutcomeCodes"]["OutcomeItemAttributesList"][subsection]["AttributeId"]:
                                        innerholderholder.append(
                                            data["References"][study]["Outcomes"][item]["OutcomeCodes"]["OutcomeItemAttributesList"][subsection]["AttributeName"])
                        else:
                            innerholderholder = "NA"
                        if len(innerholderholder) == 0:
                            innerholderholder = "NA"
                        outerholder.append(innerholderholder)
                else:
                    outerholder = "NA"
            varlist.append(outerholder)
    return varlist


def get_outcome_data_lvl1(data, attribute_text, column_prefix):
    outcome_data = get_outcome_lvl1(data, attribute_text)
    outcome_df = pd.DataFrame(outcome_data)
    # round data to 4 decimal places
    outcome_df = outcome_df.applymap(lambda x: round(x, 4) if isinstance(x, (int, float)) else x)
    # name each column (number depends on outcome number)
    outcome_df.columns = [column_prefix+'{}'.format(column+1) for column in outcome_df.columns]
    # Clean up data frame
    outcome_df = clean_up(outcome_df)
    return outcome_df



def get_outcome_data_lvl2(data, attribute_codes, column_prefix):
    # get outcome data
    outcome_data = get_outcome_lvl2(data, attribute_codes)
    outcome_df = pd.DataFrame(outcome_data)
    # name each column (number depends on outcome number)
    outcome_df.columns = [column_prefix+'{}'.format(column+1) for column in outcome_df.columns]
    # fill blanks with NA
    outcome_df.fillna("NA", inplace=True)
    return outcome_df
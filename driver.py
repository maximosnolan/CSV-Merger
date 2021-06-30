import csv
import math as m
import random as rand
from numpy import NaN
import pandas as pd
import time

support_1_DF = pd.read_csv("Logicalis-Genentech.csv")
support_2_DF = pd.read_csv("Logicalis-Roche.csv")


sheet_list = {}



def search_sheet(dataframe, current_serial):
    row_count = 0
    for x in dataframe["Serial Number"]:
        if(x == current_serial):
            #Match is found, pull data from aux sheet to main sheet
            print("Found:" , current_serial, "")
            #Items to copy:
            #Iteration Order: Part Description, Machine Type, Model/Feature, Price, Date, Serial
            return dataframe.iloc[row_count]["Part Description"], NaN, dataframe.iloc[row_count]["Part Number"], dataframe.iloc[row_count]["Customer Price"],  dataframe.iloc[row_count]["Start Date"], x
        row_count+=1

    return False


def pull_serial(main_sheet):
    row_count = 0
    with open(main_sheet, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            current_serial = row["Order/Serial"]
            found = False
            if(current_serial == 'x'):
                continue
            print("Searching aux sheets for:" , current_serial)
           
            for sheet_name, df in sheet_list.items():
                if(found == True): continue
                print("Search for", current_serial, "in", sheet_name)
                if(search_sheet(df, current_serial) != False):
                    disc, mach_type, mod_feat, price, date, serial = search_sheet(df, current_serial)
                    found = True
                    if not (pd.isna(row["Description"])): #if there is already information in here we don't need to process
                        print("Pre process:",  row)
                        row["Description"] = disc
                        row["Model/ Feature"] = mod_feat
                        row["Machine Type"] = mach_type
                        row["Annual Price HWMA"] = price
                        row["Period 1 A"] = date
                        row["Service Level Code"] = serial
                        print("Post Process:" ,row)
            if(found == False):
                print("Could not find the serial number:" , current_serial, " In either of the aux sheets provided. Will fill values with NULL for later augentation.")
                row["Description"] = NaN
                row["Model/ Feature"] = NaN
                row["Machine Type"] = NaN
                row["Annual Price HWMA"] = NaN
                row["Period 1 A"] = NaN
                row["Service Level Code"] = NaN
    return

def main():
    start_time = time.time()
    print("Welcome US Maintenance-Inventory Automation Script!")
    print("Be sure that you are pulling from a CSV sheet (you can save the XLSX sheet as a CSV. Make sure the first row is the name of the data and that there is no other information in the sheet besides that and the datapoints")
    print("Make sure you are running this script in a folder with all the xlsx files you want to pull from. Specify their names in the next prompt")
    #add support prompt for sheet name
    #main_sheet = input("Please enter the name of the master sheet. Example: 'US-Maintenance-InventoryV4.csv'")
    #num_sheets = input("How many support sheets do you have?")
    """for x in range(num_sheets):
        victim_sheet = input("What is the name of sheet #", x , "? Example: Logicalis-Genentech.csv'")
        sheet_list[victim_sheet] = pd.read_csv(victim_sheet) """
    print("Pulling data from:")
    sheet_list['Logicalis-Genentech.csv'] = pd.read_csv('Logicalis-Genentech.csv')
    #print(sheet_list["Logicalis-Genentech.csv"])
    sheet_list['Logicalis-Roche.csv'] = pd.read_csv('Logicalis-Roche.csv')
    #print(sheet_list["Logicalis-Roche.csv"])
    main_sheet = 'US-MatV4.csv'
    print("Into", main_sheet)
    main_sheet = 'US-MatV4.csv'
    pull_serial(main_sheet = main_sheet)
    main_df = pd.read_csv("US-MatV4.csv")
    #print(main_df.loc[100]["Description"])
    """if(pd.isna(main_df.loc[13]["Description"])):
        print("SUCSESS")"""
    print("Scripting completed. See Main CSV sheet for reflected Changes.")
    print("Completed in:", time.time() - start_time)
    return


if __name__ == "__main__":
    main()
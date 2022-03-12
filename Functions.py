import time,requests,csv,pandas as pd
    ################################################################################
class script:
    def __init__(self,script_Name,api,data_section,assign_columns=["humidity","visibility","air_pressure","wind_speed","applicable_date"]):
        self.api = api
        self.script_Name = script_Name
        self.data_section = data_section
        self.assign_columns = assign_columns
        self.covied = requests.get(api)
        self.data_json = self.covied.json
        self.data_filter = self.data_json
        self.count_of_column = 1
        self.empty_count = 0
        self.full_info_count = 0
        self.temp_dict = {}
        self.temp_dict_empty_column = {}
        self.date  = ""
        self.count_date_list = []
        self.filename=""
    ################################################################################
    def Get_Script_Name(self):
        print("Script name is: " , self.script_Name)
    def show_api(self):
        return self.data_filter()[self.data_section]
    ################################################################################
    def assign_columns_Func(self):
        how_many_columns = input(f"Enter, count of api columns data?  database has {self.count_of_column -1 } column ")
        if how_many_columns.isdigit:
            temp = self.count_of_column + int(how_many_columns)
            while self.count_of_column < temp:
                column_value = input(f"Enter Column {self.count_of_column} name:  ")
                self.assign_columns.append(column_value)
                print(f"Column {self.count_of_column} assigned to {column_value}")
                self.count_of_column +=1
            else:
                temp = input("do you need add another column ?  press y to add.....")
                if temp.lower() == "y":
                    self.assign_columns_Func()
        else:
            print("sorry, the columns count requirement only needs numbers")
    ################################################################################
    def show_columns_list(self):
        for id , elements in enumerate(self.assign_columns,1):
            print(f"column no.:  {id} | column name: {elements} ")
    ################################################################################
    def View_data_as_a_print(self):
        for row in self.data_json()[self.data_section]:
            for i in range(len(self.assign_columns)):
                print(row[self.assign_columns[i]],end="    |    " )
            print(end="\n")
    ################################################################################
    def create_date(self):
        user_date = [int(input("Enter Day: ")),int(input("Enter month: ")),int(input("Enter year: "))]
        if user_date[0]<=30 and user_date[0] >=1  and user_date[1]<=12 and user_date[1]>=1 and user_date[2] == 2022:
            self.date = (f"{user_date[2]}-0{user_date[1]}-{user_date[0]}")
        else:
            print("Please Enter valid date")
    
    def get_column_date(self):
        for row in self.data_json()[self.data_section]:
            if  row[self.assign_columns[4]] == self.date:
                 self.count_date_list.append(row[self.assign_columns[4]])

    ################################################################################
    def Save_To_Csv_file(self):
        self.create_date()
        self.get_column_date()
        self.full_info_count = 0
        self.filename=self.script_Name+"_File_"+self.date+".csv"
        with open(self.filename,"w",newline="") as f:
            writer = csv.DictWriter(f,fieldnames=self.assign_columns)
            writer.writeheader()
            for row in self.data_json()[self.data_section]:         
                for i in range(len(self.assign_columns)):
                        if self.date in row[self.assign_columns[4]]:
                            self.temp_dict[self.assign_columns[i]] = row[self.assign_columns[i]]
                            self.full_info_count +=1
                if len(self.count_date_list) <= self.full_info_count:
                    writer.writerow(self.temp_dict)
                    break
        print(f"Done , Exported file to {self.filename} including {len(self.count_date_list)} results" )
        self.count_date_list = []
        data = pd.read_csv(self.filename) 
        return data
    
    
    ################################################################################

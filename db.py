import json
from os.path import exists

class load_data_base():

    def __init__(self):
        self.file = "data_base.json";
        self.base = '{"By" : "Shadowy", "users" : [] }'


        if(exists(self.file)):
            with open(self.file) as file: self.data = json.load(file)
        else:
            self.data = json.loads(self.base)
            self.save()

        #print(self.data);

    def save(self):
        with open(self.file, 'w') as aq:
            json.dump(self.data, aq, indent=4)

    def _get_data(self):
        with open(self.file,'r') as file:
            # First we load existing data into a dict.
            return json.load(file);

    def compare_has(self, dump, data):
        users_list = dump["users"]
        for i in users_list:
            if (i['User'] == data["User"]):
                print('User ID has already in use')
                print(i)
                print(data)
                return 1
            if (i['Email'] == data["Email"]):
                print('User EMAIL has already in use')
                print(i)
                print(data)
                return 2
        
        return 0

    def _update_data(self, changes):
        with open(self.file,'r+') as file:
            file.seek(0)
            json.dump(changes, file, indent = 4)
            return 0;

    def change_pass(self, step, user = None, email = None, new_pass = None, backup = None ):
        data = self._get_data()
        if step == 0:
            for i in data["users"]:
                if( user == i['User'] and email == i['Email']):
                    self.last_found = i;
                    return i;
            return 0;
        if step == 1:
            for i in data["users"]:
                if( i == self.last_found ):
                    i['Password'] = new_pass;
                    i['Backup_senha'] = backup;

            print(data);        
            return self._update_data(data);
            

    def compare_data(self, user_email, senha):
        with open(self.file,'r') as file:
            # First we load existing data into a dict.
            file_data = json.load(file);
            file_data = file_data["users"];
            for i in file_data:
                if (user_email == i['User'] or user_email == i['Email']) and senha == i['Password']:
                    self.user = i;
                    return 0;
        
        return 1;


    def write_json(self, new_data):
        with open(self.file,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)

            ret_ = self.compare_has(file_data, new_data)
            if (ret_ != 0):
                return ret_;

            # Join new_data with file_data inside emp_details
            file_data["users"].append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
            return 0;

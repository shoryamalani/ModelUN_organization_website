import dbs_worker
class User:
    data = {}
    user_id = 0
    def __init__(self,name,email,token):
        userData = dbs_worker.get_user_by_email(email)
        if userData == None:
            userData = dbs_worker.create_user(name,email,token)
            print("User created")
            userCount = dbs_worker.get_user_count()
            if(userCount == 1):
                dbs_worker.set_user_role(userData[0],1)
            else:
                dbs_worker.set_user_role(userData[0],2)
        
        self.data = userData
        print(self.data)
    @classmethod
    def from_data(cls,data):
        return cls(data[1],data[2],data[3])
    def get_role(self):
        return dbs_worker.get_users_role(self.data[0]).convertRoleDataToDictionary()
    def convertUserDataToDictionary(self):
        return {'name': self.data[1],'email': self.data[2],'user_token': self.data[3],'date_created': self.data[4],'last_login': self.data[5],'role_id': self.data[6],'user_id': self.data[0],'user_data': self.data[7],'role': self.get_role()}

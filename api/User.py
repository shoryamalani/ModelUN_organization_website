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
        
        self.data = userData
        print(self.data)
    def convertUserDataToDictionary(self):
        return {'name': self.data[1],'email': self.data[2],'userToken': self.data[3],'dateCreated': self.data[4],'last_login': self.data[5],'role_id': self.data[6],'user_id': self.data[0],'user_data': self.data[7]}

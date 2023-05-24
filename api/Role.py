import dbs_worker
class Role:
    data = []
    role_id = 0
    
    def __init__(self,role_data,role_id):
        self.data = role_data
        self.role_id = role_id
    @classmethod
    def instantiate_without_id(cls,name, data):
        
        role_id = dbs_worker.get_role_by_name(name)
        if role_id == None:
            role_id =dbs_worker.add_role(name, data)
        return cls(data,role_id)
    def convertRoleDataToDictionary(self):
        return {'role_id': self.data[0],'name': self.data[1],'data': self.data[2]}
    
    # def __init__(self,role_id):
    #     self.role_id = role_id
    #     self.data = dbs_worker.get_role_by_id(role_id)
        
    


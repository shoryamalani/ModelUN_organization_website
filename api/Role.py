import dbs_worker
class Role:
    data = {}
    role_id = 0
    def __init__(self,name, data):
        self.data = data
        self.role_id = dbs_worker.get_role_by_name(name)
        if self.role_id == None:
            self.role_id =dbs_worker.add_role(name, data)
    # def __init__(self,role_id):
    #     self.role_id = role_id
    #     self.data = dbs_worker.get_role_by_id(role_id)
        
    


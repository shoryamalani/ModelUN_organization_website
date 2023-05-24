import dbs_worker
def create_committee_data():
    return {
        "backgroundGuideLink": "",
        "plannedCommittee": False,
        "backgroundGuideCompleted": True,
    }
class Committee:
    data = []
    def __init__ (self, id):
        self.data = dbs_worker.get_committee_by_id(id)

    @classmethod
    def create_committee(cls, name,email,type, data=create_committee_data()):
        committee_id = dbs_worker.add_committee(name,email,type, data)
        return cls(committee_id)
    def convertUserDataToDictionary(self):
        return {'id': self.data[0],'name': self.data[1],'email': self.data[4],'type': self.data[3],'data': self.data[2]}
    @classmethod
    def from_data(cls,data):
        return cls(data[0])
    def update_committee_type(self, type):
        print(self.data)
        dbs_worker.update_committee_type(self.data[0], type)
    def update_committee_background_guide(self, background_guide):
        # dbs_worker.update_committee_background_guide(self.data[0], background_guide)
        pass
    


    
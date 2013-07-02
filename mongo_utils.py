from pymongo.son_manipulator import SONManipulator

class Transform(SONManipulator):
    def transform_incoming(self, son, collection):
        for (key, value) in son.items():
            if isinstance(value, Custom):
                son[key] = encode_custom(value)
            elif isinstance(value, dict): # Make sure we recurse into sub-docs
                 son[key] = self.transform_incoming(value, collection)
        return son

    def transform_outgoing(self, son, collection):
        for (key, value) in son.items():
            if isinstance(value, dict):
                if "_type" in value and value["_type"] == "custom":
                    son[key] = decode_custom(value)
                else: # Again, make sure to recurse into sub-docs
                    son[key] = self.transform_outgoing(value, collection)
        return son

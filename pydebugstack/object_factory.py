
def object_factory(obj_type, attr):
    """ Generates a generic python object """

    obj = obj_type()

    for k, v in attr.items():
        setattr(obj, k, v)

    return obj

        

    


import jsonpickle


def object_factory(obj_type, attr):
    """ Generates a generic python object """

    attr['py/object'] = obj_type

    attr_in = """{"py/object": "samples.Thing", "name": "A String", "child": null}"""
    
    attr_in = str(attr)

    print "Setting attr = {}".format(attr_in)

    obj = jsonpickle.decode(attr_in)
    #obj = obj_type()

    for k, v in attr.items():
        setattr(obj, k, v)

    return obj

        

    


import jsonpickle


def object_factory(attr_in):
    """ Generates a generic python object """

    return jsonpickle.decode(attr_in)

        

    


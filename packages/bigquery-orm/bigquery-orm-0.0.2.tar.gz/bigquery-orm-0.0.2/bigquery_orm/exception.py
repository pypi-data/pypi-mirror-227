class ExceptionInvalidModel(Exception):

    def __init__(self):
        message = " Invalid DataClass for the context of this package. "
        super(ExceptionInvalidModel, self).__init__(message)

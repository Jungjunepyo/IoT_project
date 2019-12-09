from coapthon import defines

from coapthon.resources.resource import Resource

class AdvancedResource(Resource):
    def __init__(self, name="Advanced"):
        super(AdvancedResource, self).__init__(name)
        self.payload = "Advanced resource"

    def render_GET_advanced(self, request, response):
        fp = open("dustDat.txt", "r")
        line = fp.readline()
        line_tmp = line

        while True:
            line = fp.readline()
            
            if not line:    # payload is last line
                self.payload = line_tmp
                break
            
            line_tmp = line
        response.payload = self.payload
		#response.max_age = 20
        response.code = defines.Codes.CONTENT.number

        fp.close
        return self, response

    def render_POST_advanced(self, request, response):
        self.payload = request.payload
        from coapthon.messages.response import Response
        assert(isinstance(response, Response))
        response.payload = "Response changed through POST"
        response.code = defines.Codes.CREATED.number
        return self, response

    def render_PUT_advanced(self, request, response):  # Save dust data here
        self.payload = request.payload

        fp = open("dustDat.txt", 'a')
        #intVal = int(self.payload)
        data = self.payload + "\n"
        fp.write(data)   # Append new dust value data
        fp.close

        from coapthon.messages.response import Response
        assert(isinstance(response, Response))
        response.payload = self.payload
        response.code = defines.Codes.CHANGED.number
        return self, response

    def render_DELETE_advanced(self, request, response):
        response.payload = "Response deleted"
        response.code = defines.Codes.DELETED.number
        return True, response

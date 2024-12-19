from concurrent import futures
import grpc
import parser_pb2
import parser_pb2_grpc

class ParserServiceServicer(parser_pb2_grpc.ProtoServiceServicer):
    def Predict(self, request, context):
        text = request.original_text
        category = 'gratitude' # todo сделать получение категории парсером/нейронкой
        return parser_pb2.Response(category)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    parser_pb2_grpc.add_ProtoServiceServicer_to_server(ParserServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

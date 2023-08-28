from _qwak_proto.qwak.vectors.v1.vector_service_pb2_grpc import VectorServiceServicer


class VectorServingServiceMock(VectorServiceServicer):
    def SearchSimilarVectors(self, request, context):
        return super().SearchSimilarVectors(request, context)

    def UpsertVectors(self, request, context):
        return super().UpsertVectors(request, context)

    def DeleteVectors(self, request, context):
        return super().DeleteVectors(request, context)

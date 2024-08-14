from google.maps import routing_v2
from google.type.latlng_pb2 import LatLng
from google.protobuf.json_format import MessageToJson


async def sample_compute_routes() -> str:
    # Create a client
    client = routing_v2.RoutesAsyncClient()

    # Initialize request argument(s)
    request = routing_v2.ComputeRoutesRequest(
        origin=routing_v2.Waypoint(
            location=routing_v2.Location(
                lat_lng=LatLng(latitude=36.0192418, longitude=129.3242741)
            )
        ),
        destination=routing_v2.Waypoint(
            location=routing_v2.Location(
                lat_lng=LatLng(latitude=36.0214277, longitude=129.3370694)
            )
        ),
        travel_mode=routing_v2.RouteTravelMode.TRANSIT,
    )

    # Make the request
    response = await client.compute_routes(
        request=request, metadata=[("x-goog-fieldmask", "*")]
    )

    resultJson = MessageToJson(response._pb)
    return resultJson

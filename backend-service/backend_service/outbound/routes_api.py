# type: ignore
from google.maps import routing_v2
from google.type.latlng_pb2 import LatLng
from google.protobuf.json_format import MessageToJson
from google.api_core.client_options import ClientOptions
from pydantic_extra_types.coordinate import Coordinate
from ..env import env


async def sample_compute_routes() -> str:
    return await compute_routes(
        origin=Coordinate(latitude=36.0192418, longitude=129.3242741),
        destination=Coordinate(latitude=36.0214277, longitude=129.3370694),
    )


async def compute_routes(origin: Coordinate, destination: Coordinate) -> str:
    # Create a client
    client = routing_v2.RoutesAsyncClient(
        client_options=ClientOptions(api_key=env.GCP_API_KEY)
    )

    # Initialize request argument(s)
    request = routing_v2.ComputeRoutesRequest(
        origin=routing_v2.Waypoint(
            location=routing_v2.Location(
                lat_lng=LatLng(latitude=origin.latitude, longitude=origin.longitude)
            )
        ),
        destination=routing_v2.Waypoint(
            location=routing_v2.Location(
                lat_lng=LatLng(
                    latitude=destination.latitude, longitude=destination.longitude
                )
            )
        ),
        travel_mode=routing_v2.RouteTravelMode.TRANSIT,
    )

    # Make the request
    response = await client.compute_routes(
        request=request,
        metadata=[("x-goog-fieldmask", "*")],
    )

    resultJson = MessageToJson(response._pb)
    return resultJson

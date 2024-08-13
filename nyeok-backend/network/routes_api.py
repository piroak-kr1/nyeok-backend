from google.maps import routing_v2
from google.type.latlng_pb2 import LatLng
from google.protobuf.field_mask_pb2 import FieldMask


async def sample_compute_routes():
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

    # Handle the response
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(sample_compute_routes())

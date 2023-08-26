import json
import tum_esm_utils
import tum_esm_lowcost_metadata.types as types
import pendulum
import typing


class Interface:
    """Query interface for the metadata."""

    def __init__(
        self,
        samples: types.SampleDocument,
        sensors: types.SensorDocument,
        sites: types.SiteDocument,
    ):
        self.samples, self.sensors, self.sites = samples, sensors, sites

    def get(
        self, sensor_id: types.SensorIdentifier, timestamp: pendulum.DateTime
    ) -> types.MetaData:
        """Returns the metadata for the given sensor that was active at the given timestamp."""
        sensor = self.sensors.get(sensor_id)
        assert sensor is not None, f"Sensor {sensor_id} not found"
        # Find the sample that was active at the given timestamp
        sample = None
        for element in self.samples:
            if (
                (sensor_id == "all" or sensor_id in element['sensor_ids'])
                and element['sampling_start'] <= timestamp
                and (element['sampling_end'] is None or timestamp < element['sampling_end'])
            ):
                # Don't break out of the loop here, because we want the last sample that matches
                # this could be a problem, since the samples don't need to be ordered in the samples file
                sample = element
                  
        assert sample is not None, f"No sample found for sensor {sensor_id} at {timestamp}"
        # Find the corresponding site
        site = self.sites.get(sample.site_id)
        assert site is not None, f"Site {sample.site_id} not found"
        # Join the sample, sensor, and site and return
        return types.MetaData(
            site_id=sample.site_id,
            site_type=site.site_type,
            site_lat=site.site_lat,
            site_lon=site.site_lon,
            elevation=site.elevation,
            site_comment=site.comment,
            sensor_id=sensor_id,
            sensor_type=sensor.sensor_type,
            sensor_make=sensor.sensor_make,
            sensor_model=sensor.sensor_model,
            start_up_date=sensor.start_up_date,
            shut_down_date=sensor.shut_down_date,
            sensor_comment=sensor.comment,
            orientation=sample.orientation,
            elevation_ag=sample.elevation_ag,
            sampling_comment=sample.comment,
        )


def load_from_github(
    github_repository: str,
    access_token: typing.Optional[str] = None,
) -> Interface:
    """Downloads metadata from GitHub and provides a query interface."""
    _req: typing.Callable[[str], list[Any]] = lambda t: json.loads(
        tum_esm_utils.github.request_github_file(
            github_repository=github_repository,
            filepath=f"data/{t}.json",
            access_token=access_token,
        )
    )
    # Instantiate and return the interface
    return Interface(samples=_req("SAMPLING"), sensors=_req("SENSORS"), sites=_req("SITES"))

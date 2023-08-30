from pandas import DataFrame
from typing import Optional, List, Any, Dict, Union

from . import _decorator
from .data_type import PeerGroupMethodology, Order
from .._base import _logger
from ._config import _Config
from ._data_objects import Investments, DataPoints
from ._investment._peer_group_data import PeerGroupProvider

_config = _Config()
peer_group_provider = PeerGroupProvider()


@_decorator.typechecked
@_decorator.log_usage
def get_peer_group_breakpoints(
    investments: Union[List[str], str],
    data_points: Union[List[Dict[str, Any]], DataFrame],
    order: Order = Order.ASC,
    percentiles: Optional[List[int]] = list(range(1, 101)),
    methodology: Optional[PeerGroupMethodology] = None,
) -> DataFrame:

    """Gets peer group breakpoints for the specified list of investments and specified list of datapoints.

    The investments can be provided in one of the following ways:

    * Investment IDs - a list of strings, where each string is the SecId of the investment.
    * List ID - a GUID that represents a saved list id.
    * Search Criteria ID - a numeric string that represents a saved search criteria.
    * Category ID - a string that represents the secId of the category, the format is 'secId;universe'.

    The data_points can be provided in one of the following ways. The API only support calculation data points. At the
      same time, it only supports the same calculation data point with different settings within a request.

    * Data Point IDs - a list of dicts, where each dict contains the property `datapointId` and `alias`. Data will be
      returned for this data point with its default parameters. If you would like to override some of those defaults,
      they can be added to the object.
      For instance:

      * `{ "datapointId": "41", "alias": "Z1"}` - this would return breakpoints of standard deviation for the last 3
        years (the default behavior).
      * `{ "datapointId": "41", "alias": "Z2", "startDate": "2015-01-01", "endDate": "2017-12-31"}` - this would return
        breakpoints of standard deviation for the time period between Jan 1, 2015 and Dec 31, 2017.

    * Data Point Settings - a DataFrame of data points with all defined settings. Each row represents a data point.
      Each column is a configurable setting and should contains `datapointId` and `alias`.

    Args:
        investments (:obj:`Investments`, `required`): An object which can be one of the following:

            * 1. A list of investment codes (:obj:`list`, `optional`): Use this for an ad hoc approach to
              selecting investments, rather than using a list or a search. The investment code format is secid;universe or just secid.
              For example: ["F00000YOOK;FO","FOUSA00CFV;FO"] or ["F00000YOOK","FOUSA00CFV"].
            * 2. A list ID (:obj:`str`, `optional`): The unique identifier of the saved investment list from the Workspace module
              in Morningstar Direct. The format is GUID. For example, "EBE416A3-03E0-4215-9B83-8D098D2A9C0D".
            * 3. Search Criteria  ID (:obj:`str`, `optional`): The unique identifier of a saved search criteria from Morningstar
              Direct. The id string is numeric. For example, "9009".
            * 4. Category ID (:obj:`str`, `optional`): The secid of the category, the format is 'secId;universe'. For
              example, "EUCA000564;FO".

        data_points (:obj:`DataPoints`, `required`): An object which can be one of the following:

            * 1. Data point IDs (:obj:`list`, `optional`): A list of unique identifiers for data points. The format is an array
              of data points with (optionally) associated settings. Each data point should contains `datapointId` and
              `alias`.
              For example::

                [
                    {
                        "datapointId": "41",
                        "alias": "Z1"
                    },
                    {
                        "datapointId": "41",
                        "alias": "Z2",
                        "startDate": "2021-07-01",
                        "endDate": "2021-12-31",
                        "windowType": "2",
                        "windowSize": "3",
                        "stepSize": "2"
                    }
                ]

            * 2. Data point settings (:obj:`DataFrame`, `optional`): A DataFrame of data points and their associated
              setting values. Each data point should contains `datapointId` and `alias`.

        order (:obj:`Order`, `optional`): The order of peer group breakpoint. Enumeration `md.direct.Order.DESC` or
            `md.direct.Order.ASC` is available. Default `md.direct.Order.ASC` if empty.
        percentiles (:obj:`list`, `optional`): Default [1,2,3,...,100] if empty and its values range from 1 to 100.
        methodology (:obj:`PeerGroupMethodology`, `optional`): The methodology to calculation breakpoints. Enumeration
            `md.direct.PeerGroupMethodology.MORNINGSTAR` or `md.direct.PeerGroupMethodology.SIMPLE` is available.
            Based on global setting `Custom Peer Group Ranking` if empty.

    Returns:
        DataFrame: A DataFrame object with peer group breakpoint data. The DataFrame column includes alias that user
        input in parameter data_point_ids.

    :Examples:

    Get peer group breakpoint data for standard deviation datapoint.

    ::

        import morningstar_data as md

        df = md.direct.get_peer_group_breakpoints(
                investments='740284aa-fcd3-43f6-99d1-8f3d4a179fcc',
                data_points=[
                    {"datapointId": "41", "alias": "Z1"},
                    {"datapointId": "41", "alias": "Z2", "startDate": "2021-07-01", "endDate": "2021-12-31", "windowType": "2", "windowSize": "3", "stepSize": "2"}
                ],
                order=md.direct.Order.ASC,
                percentiles=[25, 50, 75, 100]
            )
        df

    :Output:
        ======  ===========  ==========  ==========  ==========  ==========  ==========
        Alias   StartDate    EndDate     25          50          75          100
        ======  ===========  ==========  ==========  ==========  ==========  ==========
        Z1      2019-04-01   2022-03-31  17.301437   12.720889   7.055372    -3.460187
        Z2      2021-07-01   2021-09-30  1.827371    -0.804269   -4.899745   -52.143678
        Z2      2021-09-01   2021-11-30  -0.030321   -4.336051   -10.618009  -40.980480
        ======  ===========  ==========  ==========  ==========  ==========  ==========

    Errors:
        AccessDeniedError: Raised when user lacks permission or not authorized to access the resource.

        BadRequestException: Raised due to multiple reasons including invalid/incorrect request, malformed request syntax, or deceptive request routing.

        NetworkExceptionError: Raised when there is an issue with the internet connection or if the request is made from an unsecure network.

        ResourceNotFoundError: Raised when the requested resource does not exist in Direct.

    """
    investment_param = Investments(investments)
    data_point_param = DataPoints(data_points)

    peer_group_req = peer_group_provider.build_request(investment_param, data_point_param, order=order, percentiles=percentiles, methodology=methodology)
    peer_group_resp = peer_group_provider.run_request(peer_group_req)
    return peer_group_provider.build_data_frame(peer_group_resp)

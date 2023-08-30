from operator import inv
import warnings
from pandas import DataFrame
from typing import Optional, List, Dict, Any, Union

from . import _decorator
from .._base import _logger
from ._data_objects import Investments, InvestmentType, DataPoints, DataPointsType

from ._investment._asset_flow_data import AssetFlowProvider
from ._investment._normal_data import NormalDataProvider
from ._investment._common import _get_data_points, _get_data_point_col_names


@_decorator.typechecked
def investment_data(
    investments: Union[List[str], str, Dict[str, Any]],
    datapoints: Union[List[Dict[str, Any]], str, DataFrame],
) -> DataFrame:
    warnings.warn(
        "The investment_data function will be deprecated in the next version, use get_investment_data instead",
        FutureWarning,
        stacklevel=2,
    )
    return _get_investment_data(investments, datapoints)


# FIXME: In https://msjira.morningstar.com/browse/AL2-92, the error_handler decorator was removed from some methods
# to trigger QueryLimitException.
# There are multiple methods where the decorator was removed to trigger certain exceptions back to the caller:
#   - save_investment_list
#   - investment_data
#   - holding_dates
#   - asset_flow
# For the time being, we will leave this as-is to keep things working. Moving forward, we must re-design the
# exception handling so that we don't have these types of special cases where error_handler is only allowed on some
# methods but not others.
@_decorator.typechecked
@_decorator.log_usage
def get_investment_data(
    investments: Union[List[str], str, Dict[str, Any]],
    data_points: Optional[Union[List[Dict[str, Any]], str, DataFrame, List[Any]]] = None,
    display_name: bool = False,
) -> DataFrame:
    """Get data for the given list of investments and data points.

    The investments can be provided in one of the following ways:

    * Investment IDs - a list of strings, where each string is the SecId of the investment.
    * List ID - a GUID that represents a saved list id.  This method will fetch the contents of the list first, and
      then get the data points for all investments in that list.
    * Search Criteria ID - a numeric string that represents a saved search criteria. This method will get all investments
      matching the criteria in the search criteria, and then get data for all provided data points for those investments.
    * Search Criteria Condition - a dictionary describing the detailed search criteria. The dictionary must include
      `universeId` and `criteria`.

    The data points can be provided in one of 4 ways:

    * Data Point IDs - a list of dicts, where each dict contains the property `datapointId`. Data will be returned for
      this data point with its default parameters.  If you would like to override some of those defaults, they can be
      added to the object.
      For instance:

      * `{ "datapointId": "HP010"}` - this would return Monthly Returns for the last 3 years (the default behavior).
      * `{ "datapointId": "HP010", "startDate": "2015-01-01", "endDate": "2017-12-31"}` - this would return Monthly Returns
        for the time period between Jan 1, 2015 and Dec 31, 2017.

    * Data Point Settings - a DataFrame of data points with all defined settings.  Each row represents a data point. Each
      column is a configurable setting. The Dataframe can be retrieved from a data set.

    * Data Set ID - an string that represents a saved data set.  The function will get data for all data points in this
      data set, using the settings defined in the data set.

    Args:
        investments (:obj:`Union`, `required`): An object which can be one of the following:

            * 1. A list of investment codes (:obj:`list`, `optional`): Use this for an ad hoc approach to
              selecting investments, rather than using a list or a search. The investment code format is secid;universe or just secid.
              For example: ["F00000YOOK;FO","FOUSA00CFV;FO"] or ["F00000YOOK","FOUSA00CFV"].
            * 2. A list ID (:obj:`str`, `optional`): The unique identifier of the saved investment list from the Workspace module
              in Morningstar Direct. The format is GUID. For example, "EBE416A3-03E0-4215-9B83-8D098D2A9C0D".
            * 3. Search Criteria  ID (:obj:`str`, `optional`): The unique identifier of a saved search criteria from Morningstar
              Direct. The id string is numeric. For example, "9009".
            * 4. Search Criteria Condition (:obj:`dict`, `optional`): The detailed search criteria. The dictionary must include the keys
              `universeId` and `criteria`.
              For example::

                SEARCH_CRITERIA_CONDITION = {"universeId": "cz",
                        "subUniverseId": "",
                        "subUniverseName": "",
                        "securityStatus": "activeonly",
                        "useDefinedPrimary": False,
                        "criteria": [{"relation": "", "field": "HU338", "operator": "=", "value": "1"},
                                        {"relation": "AND", "field": "HU863", "operator": "=", "value": "1"}]}

        data_points (:obj:`Union`, `optional`): An object which can be one of the following, if no value is provided and
        there is a list ID or search criteria ID, the API will get the corresponding bound dataset by default.

            * 1. Data point IDs (:obj:`list`, `optional`): A list of unique identifiers for data points. The format is an array
              of data points with (optionally) associated settings.
              For example::

                [
                    {
                        "datapointId": "OS01W"
                    },
                    {
                        "datapointId": "HP010",
                        "isTsdp": True,
                        "currency": "CNY",
                        "startDate": "2021-03-01",
                        "endDate": "2021-08-31"
                    }
                ]

            * 2. Data Set ID (:obj:`str`, `optional`): The unique identifier of a Morningstar data set or user created data set saved
              in Morningstar Direct. The id string is numeric. For example: "6102286".
            * 3. Data point Settings (:obj:`DataFrame`, `optional`): A DataFrame of data points and their associated setting values.

        display_name: bool: This argument determines if the investment_data should have displayName as the column names for datasets

    Returns:
        DataFrame: A DataFrame object with investment data. The DataFrame columns include data point name that user input
        in parameter data_points.

    :Examples:

    Get investment data based on investment list id and data point list id.

    ::

        import morningstar_data as md

        df = md.direct.get_investment_data(
            investments=["F0AUS05U7H", "F000010NJ5"],
            data_points=[
                {"datapointId": "OS01W", "isTsdp": False},
                {"datapointId": "LS05M", "isTsdp": False},
            ],
        )
        df

    :Output:
        =================  ===================================  =================  ============================
        Id                 Name                                 Base Currency      Base Currency - display text
        =================  ===================================  =================  ============================
        F0AUS05U7H         Walter Scott Global Equity           AUD                Australian Dollar
        F000010NJ5         Vontobel Emerging Markets Eq U1 USD  USD                US Dollar
        =================  ===================================  =================  ============================

    Get investment data based on investment list id and datapoint id list.

    ::

        import morningstar_data as md

        df = md.direct.get_investment_data(
            investments="a727113a-9557-4378-924f-5d2ba553f687",
            data_points=[{"datapointId": "HS793", "isTsdp": True}],
        )
        df

    :Output:
        ==============  =================================  =============================  =============================  =============================
        Id              Name                               Daily Return Index 2021-09-23  Daily Return Index 2021-09-24  Daily Return Index 2021-09-25
        ==============  =================================  =============================  =============================  =============================
        FOUSA00DFS;FO   BlackRock Global Allocation Inv A  129.92672                      129.56781                      129.56781
        ==============  =================================  =============================  =============================  =============================

    Get investment data based on search criteria id and datapoint id list.

    ::

        import morningstar_data as md

        df = md.direct.get_investment_data(
            investments="4216254", data_points=[{"datapointId": "12", "isTsdp": True}]
        )
        df

    :Output:
        ==============  =======================  =============================
        Id              Name                     Beta 2018-10-01 to 2021-09-30
        ==============  =======================  =============================
        FOUSA06JNH;FO   DWS RREEF Real Assets A    0.654343
        ==============  =======================  =============================

    Get investment data based on search criteria id and data point id list.

    ::

        import morningstar_data as md

        SEARCH_CRITERIA_CONDITION = {
            "universeId": "cz",
            "subUniverseId": "",
            "subUniverseName": "",
            "securityStatus": "activeonly",
            "useDefinedPrimary": False,
            "criteria": [
                {"relation": "", "field": "HU338", "operator": "=", "value": "1"},
                {"relation": "AND", "field": "HU863", "operator": "=", "value": "1"},
            ],
        }

        df = md.direct.get_investment_data(
            investments=SEARCH_CRITERIA_CONDITION,
            data_points=[{"datapointId": "HS793", "isTsdp": True}],
        )
        df

    :Output:
        =  ===============  =====================================  =============================  ===  =============================
        #  Id               Name                                   Daily Return Index 2022-02-18  ...  Daily Return Index 2022-03-17
        =  ===============  =====================================  =============================  ===  =============================
        0  FOUSA06UOR;CZ    Columbia Trust Stable Government Fund  None                           ...  None
        1  FOUSA06UWL;CZ    Columbia Trust Stable Income Fund      88.8333                        ...  90.7781
        =  ===============  =====================================  =============================  ===  =============================


    """
    result = _get_investment_data(investments=investments, data_points=data_points, display_name=display_name)
    return result


def _get_investment_data(investments: InvestmentType, data_points: DataPointsType, display_name: bool = False) -> DataFrame:
    investment_param = Investments(investments)
    data_point_param = DataPoints(data_points)

    # Get asset flow data
    asset_flow_req = AssetFlowProvider.build_request(investment_param, data_point_param, display_name)
    asset_flow_result = AssetFlowProvider.run_request(asset_flow_req)

    # Get normal data
    normal_data_req = NormalDataProvider.build_request(investment_param, data_point_param, display_name)
    normal_data_result = NormalDataProvider.run_request(normal_data_req)

    # Combine data
    merged_result = asset_flow_result.merge_with(normal_data_result)

    # Build data frame, re-order columns
    data_points = _get_data_points(investment_param, data_point_param)
    data_point_cols = _get_data_point_col_names(data_points, merged_result.get_data_point_alias_to_col_dict())
    return merged_result.as_data_frame(order_cols_by=data_point_cols)

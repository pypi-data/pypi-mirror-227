import pandas as pd
import numpy as np
import warnings
from typing import List, Optional, Union, List, Dict, Any

from . import _decorator, lookup
from ..direct import investment
from ._exceptions import BadRequestException, ResourceNotFoundError
from . import _error_messages
from .data_type import Frequency
from ._config_key import FORMAT_DATE


@_decorator.typechecked
def returns(
    investments: Union[List[str], str, Dict[str, Any]],
    start_date: str = "2020-01-01",
    end_date: Optional[str] = None,
    freq: Union[Frequency, str] = Frequency.monthly,
    currency: Optional[str] = None,
) -> pd.DataFrame:
    warnings.warn(
        "The returns function will be deprecated in the next version, use get_returns instead",
        FutureWarning,
        stacklevel=2,
    )
    return get_returns(investments, start_date, end_date, freq, currency)


@_decorator.typechecked
@_decorator.log_usage
def get_returns(
    investments: Union[List[str], str, Dict[str, Any]],
    start_date: str = "2020-01-01",
    end_date: Optional[str] = None,
    freq: Union[Frequency, str] = Frequency.monthly,
    currency: Optional[str] = None,
) -> pd.DataFrame:
    """A shortcut function to fetch return data for the specified investments.

    Args:
        investments (:obj:`Union`, `required`): Can be provided in one of the following ways:

            * Investment IDs (:obj:`list`, `optional`): An array of investment codes. Use this for an ad hoc approach to
              selecting investments, rather than using a list or a search. The investment code format is secid;universe or just secid.
              For example: ["F00000YOOK;FO","FOUSA00CFV;FO"] or ["F00000YOOK","FOUSA00CFV"].
            * List ID (:obj:`str`, `optional`): The unique identifier of the saved investment list from the Workspace module
              in Morningstar Direct. The format is GUID. For example, "EBE416A3-03E0-4215-9B83-8D098D2A9C0D".
            * Search Criteria ID (:obj:`str`, `optional`): The unique identifier of a saved search criteria from Morningstar
              Direct. The id string is numeric. For example, "9009".
            * Search Criteria Condition (:obj:`dict`, `optional`): The detailed search criteria. The dictionary must include the keys
              `universeId` and `criteria`.
              For example::

                    SEARCH_CRITERIA_CONDITION = {"universeId": "cz",
                            "subUniverseId": "",
                            "subUniverseName": "",
                            "securityStatus": "activeonly",
                            "useDefinedPrimary": False,
                            "criteria": [{"relation": "", "field": "HU338", "operator": "=", "value": "1"},
                                            {"relation": "AND", "field": "HU863", "operator": "=", "value": "1"}]}

        start_date (:obj:`str`): The beginning date of a data range for retrieving data. The format is
            YYYY-MM-DD. For example, "2020-01-01".
        end_date (:obj:`str`, `optional`): The end date of data range for retrieving data. If no value is provided for
            end_date, current date will be used. The format is YYYY-MM-DD. For example, "2020-01-01".
        freq (:obj:`Frequency`): Return frequency, the possible enum values are:

         * daily
         * weekly
         * monthly
         * quarterly
         * yearly

        currency (:obj:`str`, `optional`): Three character code for the desired currency of returns.

    Returns:
        DataFrame: The DataFrame columns include Name and the investment name for each investment id in the investments argument.

    Examples:
        Get monthly return.

    ::

        import morningstar_data as md


        df = md.direct.get_returns(
            investments=["F00000VKPI", "F000014B1Y"], start_date="2020-10-01", freq=md.direct.Frequency.monthly
        )
        df

    :Output:
        ==========  =================================  ===================================
        Name Date   (LF) FoF Bal Blnd US Priv Banking  (LF) High Yield A List Priv Banking
        ==========  =================================  ===================================
        2020-10-31  -2.121865                          -0.686248
        2020-11-30  6.337255                           5.682299
        2020-12-31  1.464777                           3.011518
        ...
        ==========  =================================  ===================================

    Errors:
        AccessDeniedError: Raised when user lacks authentication.

        BadRequestError: Raised when the user does not provide a properly formatted request.

        ForbiddenError: Triggered when user lacks permission to access a resource.

        InternalServerError: Raised when the server encounters an error it does not know how to handle.

        NetworkExceptionError: Raised when the request fails to reach the server due to a network error.

        ResourceNotFoundError: Raised when the requested resource does not exist in Direct.

    """

    if not isinstance(freq, Frequency):
        warnings.warn(
            "The use of string values for the 'freq' parameter will be deprecated, use Frequency enum values instead",
            FutureWarning,
            stacklevel=2,
        )

    freq = Frequency[freq]
    assert isinstance(freq, Frequency)

    start_date = pd.to_datetime(start_date).strftime(FORMAT_DATE)
    data_point_details = lookup.get_data_point_settings(data_point_ids=[freq.data_point_id, "OS01W"])
    if data_point_details.empty:
        raise BadRequestException("Failed to retrieve datapoint details.")

    # Remove single period timeseries data (due to id collision)
    data_point_details = data_point_details.loc[(data_point_details["datapointId"].isin(["OS01W"])) | (data_point_details["isTsdp"])]
    data_point_details["startDate"] = start_date

    data_point_details["currency"] = currency
    if end_date:
        end_date = pd.to_datetime(end_date).strftime(FORMAT_DATE)
        data_point_details["endDate"] = end_date

    return_value = investment.get_investment_data(investments=investments, data_points=data_point_details)

    if return_value is None or return_value.empty:
        raise ResourceNotFoundError(_error_messages.RESOURCE_NOT_FOUND_ERROR_NO_RETURNS_RETRIEVED)
    if "Id" in return_value.columns:
        return_value = return_value.drop(["Id"], axis=1)
    return_value = return_value.replace(r"^\s*$", None, regex=True)

    if return_value.empty:
        raise ResourceNotFoundError(_error_messages.RESOURCE_NOT_FOUND_ERROR_NO_RETURNS_RETRIEVED_FOR_INVESTMENT_LIST)

    df = return_value.T
    df.columns = df.iloc[-1]
    df.drop(df.tail(1).index, inplace=True)
    new_index = {x: pd.to_datetime(x[-10:]) for x in df.index}
    df = df.rename(index=new_index)
    return df


@_decorator.typechecked
def excess_returns(
    investments: Union[List, str, Dict[str, Any]],
    benchmark_sec_id: str,
    start_date: str = "2020-01-01",
    end_date: Optional[str] = None,
    freq: Union[Frequency, str] = Frequency.monthly,
    currency: Optional[str] = None,
) -> pd.DataFrame:
    warnings.warn(
        "The excess_returns function will be deprecated in the next version, use get_excess_returns instead",
        FutureWarning,
        stacklevel=2,
    )
    return get_excess_returns(investments, benchmark_sec_id, start_date, end_date, freq, currency)


@_decorator.typechecked
@_decorator.log_usage
def get_excess_returns(
    investments: Union[List, str, Dict[str, Any]],
    benchmark_sec_id: str,
    start_date: str = "2020-01-01",
    end_date: Optional[str] = None,
    freq: Union[Frequency, str] = Frequency.monthly,
    currency: Optional[str] = None,
) -> pd.DataFrame:
    """A shortcut function to fetch excess return data for the specified investments.

    Args:
        investments (:obj:`Union`, `required`): Can be provided in one of the following ways:

            * Investment IDs (:obj:`list`, `optional`): An array of investment codes. Use this for an ad hoc approach to selecting investments, rather than using a list or a search. The investment code format is secid;universe or just secid. For example: ['F00000YOOK;FO','FOUSA00CFV;FO'] or ['F00000YOOK','FOUSA00CFV'].
            * List ID (:obj:`str`, `optional`): The unique identifier of the saved investment list from the Workspace module in Morningstar Direct. The format is GUID. For example, 'EBE416A3-03E0-4215-9B83-8D098D2A9C0D'.
            * Search Criteria ID (:obj:`str`, `optional`): The unique identifier of a saved search criteria from Morningstar Direct. The id string is numeric. For example, "9009".
            * Search Criteria Condition (:obj:`dict`, `optional`): The detailed search criteria. The dictionary must include the keys
              `universeId` and `criteria`.
              For example::

                SEARCH_CRITERIA_CONDITION = {"universeId": "cz",
                        "subUniverseId": "",
                        "subUniverseName": "",
                        "securityStatus": "activeonly",
                        "useDefinedPrimary": False,
                        "criteria": [{"relation": "", "field": "HU338", "operator": "=", "value": "1"},
                                        {"relation": "AND", "field": "HU863", "operator": "=", "value": "1"}]}

        benchmark_sec_id (:obj:`str`): The SecId of the security to use as the benchmark.
        start_date (:obj:`str`): The beginning date of a data range for retrieving data. The format is YYYY-MM-DD. For example, "2020-01-01".
        end_date (:obj:`str`, `optional`): The end date of data range for retrieving data. The format is YYYY-MM-DD. For example, "2020-01-01".
        freq (:obj:`Frequency`): Return frequency, the possible enum values are:

         * daily
         * weekly
         * monthly
         * quarterly
         * yearly

        currency (:obj:`str`, `optional`): Three character code for the desired currency of returns.

    Returns:
        DataFrame: A DataFrame object with excess return data. The DataFrame columns include Name and the investment name for each investment id in the investments argument.

    Examples:
        Get monthly return.

    ::

        import morningstar_data as md

        df = md.direct.get_excess_returns(
            investments=["F00000VKPI", "F000014B1Y"],
            benchmark_sec_id="F00000PLYW",
            freq=md.direct.Frequency.daily,
        )
        df

    :Output:
        ==========  =================================  ===================================
        Name Date   (LF) FoF Bal Blnd US Priv Banking  (LF) High Yield A List Priv Banking
        ==========  =================================  ===================================
        2020-01-01  -1150.623143                       -1154.382165
        2020-01-02  -1146.064892                       -1149.928106
        ...
        ==========  =================================  ===================================

    Errors:
        AccessDeniedError: Raised when user lacks authentication.

        BadRequestError: Raised when the user does not provide a properly formatted request.

        ForbiddenError: Triggered when user lacks permission to access a resource.

        InternalServerError: Raised when the server encounters an error it does not know how to handle.

        NetworkExceptionError: Raised when the request fails to reach the server due to a network error.

        ResourceNotFoundError: Raised when the requested resource does not exist in Direct.

    """
    if not isinstance(freq, Frequency):
        warnings.warn(
            "The use of string values for the 'freq' parameter will be deprecated, use Frequency enum values instead",
            FutureWarning,
            stacklevel=2,
        )

    df = get_returns(
        investments=investments,
        start_date=start_date,
        end_date=end_date,
        freq=freq,
        currency=currency,
    )

    if df is None or df.empty:
        raise ResourceNotFoundError(_error_messages.RESOURCE_NOT_FOUND_ERROR_NO_RETURNS_RETRIEVED)

    benchmark_returns = get_returns(
        investments=[benchmark_sec_id],
        start_date=start_date,
        end_date=end_date,
        freq=freq,
        currency=currency,
    )

    if benchmark_returns is None or benchmark_returns.empty:
        raise ResourceNotFoundError(_error_messages.RESOURCE_NOT_FOUND_ERROR_NO_RETURNS_RETRIEVED_FOR_BENCHMARK_ID)

    df["benchmark"] = benchmark_returns.iloc[:, 0]

    df = df.sub(df["benchmark"], axis="rows").drop(columns=["benchmark"])
    return df

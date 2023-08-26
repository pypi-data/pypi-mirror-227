import pandas as pd

from typing import Union
from pydash import set_, merge
from pandas.api.types import is_numeric_dtype


def _create_chart_options(
    kind: str, x: str, y: str, hue: str, options: dict, agg: str = None
) -> dict:
    """
    Prepare all the options to create a chart from user's input.

    Axes labels are automatically set to match the names of the columns drawn
    on the chart. Legend is also modified to match the "hue" argument.

    Args:
        kind (str): The kind of the chart.

        x (str): Column of the dataframe used as datapoints for x Axis.

        y (str): Column of the dataframe used as datapoints for y Axis.

        hue (str, optional): Grouping variable that will produce points with
            different colors. Defaults to None.

        options (dict, optional): All options to configure the chart. This
            dictionary corresponds to the "options" argument of Chart.js.
            Defaults to None.

        agg (str, optional): The aggregator used to gather data (ex:
            'median' or 'mean'). Defaults to None.

    Returns:
        dict: options dictionary ready to be inputted into a Chart class (i.e.
            match ipychart options format).
    """
    agg_label = "" if not agg else " (" + agg + ")"
    radials = ["radar", "pie", "polarArea", "doughnut"]

    if hue:
        title_cb = (
            "function(tooltipItem) {"
            "return '%s = ' + tooltipItem[0].label + ' & ' + '%s = '"
            " + tooltipItem[0].dataset.label;};"
        ) % (x, hue)
    else:
        title_cb = (
            "function(tooltipItem) {"
            "return '%s = ' + tooltipItem[0].label;};"
        ) % x

    suffix_bubble = "" if kind != "bubble" else ".split(',')[1]"
    label_cb = (
        "function(tooltipItem) {"
        "return '%s = ' + tooltipItem.formattedValue%s;};"
    ) % (y + agg_label, suffix_bubble)

    default_options = {
        "plugins": {
            "tooltip": {
                "enabled": True,
                "callbacks": {"title": title_cb, "label": label_cb},
            }
        }
    }

    if kind not in radials:
        scales_opt = {
            "x": {"title": {"display": True, "text": x}},
            "y": {"title": {"display": True, "text": y + agg_label}},
        }
        default_options = set_(default_options, "scales", scales_opt)
    else:
        legend_opt = {"display": True}
        default_options = set_(default_options, "plugins.legend", legend_opt)

    # Set legend prefix if "hue" if activated
    if hue:
        hue_label_cb = (
            "function(chart) {const labels = Chart.defaults.plugins."
            "legend.labels.generateLabels(chart);labels.map(label "
            """=> {label['text'] = "%s" + " = " + label['text']; """
            "return label});return labels;};"
        ) % hue

        default_options = set_(
            default_options,
            "plugins.legend.labels.generateLabels",
            hue_label_cb,
        )

    options = merge(default_options, options)

    return options


def _create_counted_data_dict(
    data: pd.DataFrame,
    x: str,
    dataset_options: dict,
    label: Union[str, None] = None,
) -> dict:
    """
    Prepare an ipychart dataset with counted data from a pandas dataframe.

    Args:
        data (pd.DataFrame): The dataframe used to draw the chart.

        x (str): Column of the dataframe used as datapoints for x Axis.

        dataset_options (dict, optional): These are options related to the
            dataset object (i.e. options concerning your data). Defaults to {}.

        label (str, optional): The label of the dataset. Defaults to None.

    Returns:
        dict: data dictionary ready to be inputted into a Chart class (i.e.
            match ipychart data format).
    """
    if is_numeric_dtype(data[x]):
        dataset = {
            "data": data[x]
            .value_counts(sort=False)
            .sort_index(ascending=True)
            .round(4)
            .tolist(),
            **dataset_options,
        }
    else:
        dataset = {
            "data": data[x]
            .value_counts(ascending=False, sort=True)
            .round(4)
            .tolist(),
            **dataset_options,
        }
    if label:
        dataset["label"] = label

    return dataset


def _create_chart_data_count(
    data: pd.DataFrame,
    x: str,
    hue: Union[str, None] = None,
    dataset_options: Union[dict, list, None] = None,
) -> dict:
    """
    Prepare all the arguments to create a chart from user's input.

    Data are counted before being send to the Chart.

    Args:
        data (pd.DataFrame): The dataframe used to draw the chart.

        x (str): Column of the dataframe used as datapoints for x Axis.

        hue (str, optional): Grouping variable that will produce points with
            different colors. Defaults to None.

        dataset_options ([dict, list], optional): These are options related to
            the dataset object (i.e. options concerning your data). Defaults
            to {}.

    Returns:
        dict: data dictionary ready to be inputted into a Chart class (i.e.
            match ipychart data format).
    """
    assert x in data.columns, f"Column {x} not found in dataframe"

    if hue:
        assert hue in data.columns, f"{hue} not found in dataframe"
        assert data[hue].nunique() <= 20, "Too much values in hue (>20)"

    if dataset_options is None:
        dataset_options = {}

    data_dict = {"datasets": []}

    if is_numeric_dtype(data[x]):
        data_dict["labels"] = (
            data[x]
            .value_counts(sort=False)
            .sort_index(ascending=True)
            .index.tolist()
        )
    else:
        data_dict["labels"] = (
            data[x].value_counts(ascending=False, sort=True).index.tolist()
        )

    if hue:
        # Create one dataset for each unique value of the hue column
        for i, v in enumerate(sorted(data[hue].unique())):
            if isinstance(dataset_options, list):
                data_dict["datasets"].append(
                    _create_counted_data_dict(
                        data=data[data[hue] == v],
                        x=x,
                        dataset_options=dataset_options[i],
                        label=str(v),
                    )
                )

            else:
                data_dict["datasets"].append(
                    _create_counted_data_dict(
                        data=data[data[hue] == v],
                        x=x,
                        dataset_options=dataset_options,
                        label=str(v),
                    )
                )

    else:
        data_dict["datasets"].append(
            _create_counted_data_dict(
                data=data, x=x, dataset_options=dataset_options
            )
        )

    return data_dict


def _create_chart_data_agg(
    data: pd.DataFrame,
    kind: str,
    x: str,
    y: str,
    r: Union[str, None] = None,
    hue: Union[str, None] = None,
    agg: Union[str, None] = None,
    dataset_options: Union[dict, list, None] = None,
) -> dict:
    """
    Prepare all the arguments to create a chart from user's input.

    Data are automatically aggregated using the method specified in the "agg"
    argument before being send to the Chart.

    Args:
        data (pd.DataFrame): The dataframe used to draw the chart.

        kind (str): The kind of the chart.

        x (str): Column of the dataframe used as datapoints for x Axis.

        y (str): Column of the dataframe used as datapoints for y Axis.

        r (str, optional): Column used to define the radius of the bubbles
            (only for bubble chart). Defaults to None.

        hue (str, optional): Grouping variable that will produce points with
            different colors. Defaults to None.

        agg (str, optional): The aggregator used to gather data (ex: 'median'
            or 'mean'). Defaults to None.

        dataset_options ([dict, list], optional): These are options related to
            the dataset object (i.e. options concerning your data). Defaults
            to {}.

    Returns:
        dict: data dictionary ready to be inputted into a Chart class (i.e.
         match ipychart data format).
    """
    assert x in data.columns, f"{x} not found in dataframe"
    assert y in data.columns, f"{y} not found in dataframe"
    assert is_numeric_dtype(data[y]), "y must be a numeric column"

    if dataset_options is None:
        dataset_options = {}

    if hue:
        assert hue in data.columns, f"{hue} not found in dataframe"
        assert data[hue].nunique() <= 20, "Too much values in hue (>20)"

    if len(dataset_options):
        if isinstance(dataset_options, list):
            msg_hue_multiple_ds_options = (
                "For multiple dataset options, you must choose a column "
                "for hue that will create multiple datasets. Each dataset "
                "will corresponds to a unique value of the hue column."
            )

            msg_hue_number_ds_options = (
                "The number of dataset_options elements must be equal to "
                "the number of unique values in the hue column."
            )

            assert hue, msg_hue_multiple_ds_options
            df_options_check = len(dataset_options) == data[hue].nunique()
            assert df_options_check, msg_hue_number_ds_options

    data_dict = {"datasets": []}

    if kind not in ["scatter", "bubble", "radar"]:
        data_dict["labels"] = (
            data[x].value_counts(ascending=True, sort=False).index.tolist()
        )

        if hue:
            # Create one dataset for each unique value of the hue column
            for i, v in enumerate(sorted(data[hue].unique())):
                if isinstance(dataset_options, list):
                    data_dict["datasets"].append(
                        {
                            "data": data[data[hue] == v]
                            .groupby(x)
                            .agg(agg)[y]
                            .round(4)
                            .tolist(),
                            "label": str(v),
                            **dataset_options[i],
                        }
                    )

                else:
                    data_dict["datasets"].append(
                        {
                            "data": data[data[hue] == v]
                            .groupby(x)
                            .agg(agg)[y]
                            .round(4)
                            .tolist(),
                            "label": str(v),
                            **dataset_options,
                        }
                    )
        else:
            data_dict["datasets"] = [
                {
                    "data": data.groupby(x).agg(agg)[y].round(4).tolist(),
                    "label": y,
                    **dataset_options,
                }
            ]

    elif kind == "bubble":
        assert is_numeric_dtype(data[r]), "r must be a numeric column"
        assert is_numeric_dtype(data[x]), "x must be a numeric column"

        data_dict["labels"] = data[x].tolist()

        def row2dictxyr(row):
            return {"x": row[x], "y": row[y], "r": row[r]}

        if hue:
            # Create one dataset for each unique value of the hue column
            for i, v in enumerate(data[hue].unique()):
                mask = data[hue] == v
                if isinstance(dataset_options, list):
                    data_dict["datasets"].append(
                        {
                            "data": data[mask].apply(row2dictxyr, 1).tolist(),
                            "label": str(v),
                            **dataset_options[i],
                        }
                    )

                else:
                    data_dict["datasets"].append(
                        {
                            "data": data[mask].apply(row2dictxyr, 1).tolist(),
                            "label": str(v),
                            **dataset_options,
                        }
                    )
        else:
            data_dict["datasets"] = [
                {
                    "data": data.apply(row2dictxyr, 1).tolist(),
                    **dataset_options,
                }
            ]

    elif kind == "scatter":
        assert is_numeric_dtype(data[x]), "x must be a numeric column"

        data_dict["labels"] = data[x].tolist()

        def row2dictxy(row):
            return {"x": row[x], "y": row[y]}

        if hue:
            # Create one dataset for each unique value of the hue column
            for i, v in enumerate(data[hue].unique()):
                mask = data[hue] == v
                if isinstance(dataset_options, list):
                    data_dict["datasets"].append(
                        {
                            "data": data[mask].apply(row2dictxy, 1).tolist(),
                            "label": str(v),
                            **dataset_options[i],
                        }
                    )

                else:
                    data_dict["datasets"].append(
                        {
                            "data": data[mask].apply(row2dictxy, 1).tolist(),
                            "label": str(v),
                            **dataset_options,
                        }
                    )
        else:
            data_dict["datasets"] = [
                {"data": data.apply(row2dictxy, 1).tolist(), **dataset_options}
            ]

    else:
        agg_label = "" if not agg else " (" + agg + ")"
        data_dict["labels"] = (
            data[x].value_counts(ascending=True, sort=False).index.tolist()
        )

        if hue:
            # Create one dataset for each unique value of the hue column
            for i, v in enumerate(data[hue].unique()):
                mask = data[hue] == v
                if isinstance(dataset_options, list):
                    data_dict["datasets"].append(
                        {
                            "data": data[mask]
                            .groupby(x)
                            .agg(agg)[y]
                            .round(4)
                            .tolist(),
                            "label": str(v),
                            **dataset_options[i],
                        }
                    )

                else:
                    data_dict["datasets"].append(
                        {
                            "data": data[mask]
                            .groupby(x)
                            .agg(agg)[y]
                            .round(4)
                            .tolist(),
                            "label": str(v),
                            **dataset_options,
                        }
                    )
        else:
            data_dict["datasets"] = [
                {
                    "data": data.groupby(x).agg(agg)[y].round(4).tolist(),
                    "label": y + agg_label,
                    **dataset_options,
                }
            ]

    return data_dict

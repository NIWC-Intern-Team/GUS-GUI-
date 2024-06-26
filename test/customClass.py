
from branca.element import Element, Figure, Html, IFrame, JavascriptLink, MacroElement
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Union
from jinja2 import Template

class customClickLatLng(MacroElement):
    """
    When one clicks on a Map that contains a ClickForLatLng,
    the coordinates of the pointer's position are copied to clipboard.

    Parameters
    ==========
    format_str : str, default 'lat + "," + lng'
        The javascript string used to format the text copied to clipboard.
        eg:
        format_str = 'lat + "," + lng'              >> 46.558860,3.397397
        format_str = '"[" + lat + "," + lng + "]"'  >> [46.558860,3.397397]
    alert : bool, default True
        Whether there should be an alert when something has been copied to clipboard.
    """

    _template = Template(
        """
            {% macro script(this, kwargs) %}
                function getLatLng(e){
                    var lat = e.latlng.lat.toFixed(6),
                        lng = e.latlng.lng.toFixed(6);
                    var txt = {{this.format_str}};
                    navigator.clipboard.writeText(txt);
                    {% if this.alert %}alert("Copied to clipboard : \\n    " + txt);{% endif %}
                    };
                {{this._parent.get_name()}}.on('click', getLatLng);
            {% endmacro %}
            """
    )  # noqa

    def __init__(self, format_str: Optional[str] = None, alert: bool = True):
        super().__init__()
        self._name = "ClickForLatLng"
        self.format_str = format_str or 'lat + "," + lng'
        self.alert = alert


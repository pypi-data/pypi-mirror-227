# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ChatSimple(Component):
    """A ChatSimple component.
Simple chat component

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- autofocus (boolean; optional):
    The element should be automatically focused after the page loaded.

- avatarOutgoing (string; optional):
    Indicates whether the outgoing message avatar should be displayed.

- avatarReceived (string; default ''):
    Indicates whether the recieved message avatar should be displayed.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- debounce (boolean; default False):
    If True, changes to input will be sent back to the Dash server
    only on enter or when losing focus. If it's False, it will sent
    the value back on every change.

- disabled (boolean; optional):
    Indicates whether the user can interact with the element.

- maxlength (number; optional):
    Defines the maximum number of characters allowed in the input
    element.

- messages (list of dicts; optional):
    Messages list.

    `messages` is a list of dicts with keys:

    - avatar (string; required):
        Avatar.

    - content (string; required):
        Content of the message.

    - direction (string; required):
        Direction of the mssage: received or outgoing.

    - timestamp (number; required):
        Time.

- n_submit (number; default 0):
    An integer that represents the number of times that the Enter key
    was pressed while the input area had focus or submit button has
    been clicked on.

- n_submit_timestamp (number; default -1):
    An integer that represents the time (in ms since 1970) at which
    n_submit changed.

- persisted_props (list of strings; default ["value"]):
    Properties whose user interactions will persist after refreshing
    the component or the page. Since only `value` is allowed this prop
    can normally be ignored.

- persistence (string | number; optional):
    Used to allow user interactions in this component to be persisted
    when the component - or the page - is refreshed. If `persisted` is
    truthy and hasn't changed from its previous value, a `value` that
    the user has changed while using the app will keep that change, as
    long as the new `value` also matches what was given originally.
    Used in conjunction with `persistence_type`.

- persistence_type (a value equal to: 'local', 'session', 'memory'; default 'local'):
    Where persisted user changes will be stored: memory: only kept in
    memory, reset on page refresh. local: window.localStorage, data is
    kept after the browser quit. session: window.sessionStorage, data
    is cleared once the browser quit.

- placeholder (string; optional):
    Provides a hint to the user of what can be entered in the field.

- rows (number; optional):
    Defines the number of rows in a text input area.

- style (boolean | number | string | dict | list; optional):
    Defines CSS styles which will override styles previously set.

- timestampDisplay (boolean; default True):
    Indicates whether the message timestamp should be displayed.

- value (string; default ''):
    Input value for controlled component.

- value_on_submit (string; default ''):
    Input value for controlled component after submit."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_chat_components'
    _type = 'ChatSimple'
    @_explicitize_args
    def __init__(self, messages=Component.UNDEFINED, avatarReceived=Component.UNDEFINED, avatarOutgoing=Component.UNDEFINED, timestampDisplay=Component.UNDEFINED, autofocus=Component.UNDEFINED, debounce=Component.UNDEFINED, disabled=Component.UNDEFINED, maxlength=Component.UNDEFINED, n_submit=Component.UNDEFINED, n_submit_timestamp=Component.UNDEFINED, placeholder=Component.UNDEFINED, rows=Component.UNDEFINED, value=Component.UNDEFINED, value_on_submit=Component.UNDEFINED, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'autofocus', 'avatarOutgoing', 'avatarReceived', 'className', 'debounce', 'disabled', 'maxlength', 'messages', 'n_submit', 'n_submit_timestamp', 'persisted_props', 'persistence', 'persistence_type', 'placeholder', 'rows', 'style', 'timestampDisplay', 'value', 'value_on_submit']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'autofocus', 'avatarOutgoing', 'avatarReceived', 'className', 'debounce', 'disabled', 'maxlength', 'messages', 'n_submit', 'n_submit_timestamp', 'persisted_props', 'persistence', 'persistence_type', 'placeholder', 'rows', 'style', 'timestampDisplay', 'value', 'value_on_submit']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(ChatSimple, self).__init__(**args)

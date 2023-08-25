import os
import streamlit.components.v1 as components


_RELEASE = False

if not _RELEASE:
    component_func = components.declare_component(
        "card",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    component_func = components.declare_component("card", path=build_dir)


def card(title, content, tags, url, key=None):
    """Create a new instance of "my_component".
    """
    return component_func(title=title, content=content, tags=tags, url=url, key=key)


if not _RELEASE:
    result = card(
        title="I am a big title",
        content="blah blah blah",
        tags={"ticker": "VOD"},
	url='http://fake.com'
    )

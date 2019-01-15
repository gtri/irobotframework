# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

import re

from jinja2 import Template


def anchorify(text):
    """ robot uses the id hack, but lab strips it out. rebuild anchors.
    """
    return re.sub(
        r"(<h\d\s*[^>]*>)\s*(.*?)\s*(</h\d>)", r"""<a name="\2"></a>\1\2\3""", text
    )


def dollarify(text):
    """ robot uses lots of dollars, but they usually aren't LaTeX. Escape.
    """
    return re.sub(r"\$", "<span>$</span>", text)


def with_twenty(match):
    """ Do some stuff with escaped whitespace
    """
    return f"""<a href="{match.group(2).replace("%20", " ")}" """.replace("%23", "#")


def twentify(text):
    """ some of the libraries escape spaces in hrefs. Don't.
    """
    return re.sub(r"""(<a href=")([^"]+)(")""", with_twenty, text)


# extra context for jinja
DOC_CONTEXT = {"dollarify": dollarify, "anchorify": anchorify}

# HTML fragment for keywords
KW_FRAG = """
<a name="{{ kw.name }}"></a>

<div class="jp-Robot-Docs-keyword">
    <div class="jp-Robot-Docs-spec">
        <table><tr><td>
        <h3>{%- if is_init -%}
                Library&nbsp;&nbsp;&nbsp;&nbsp;{{ libdoc.name }}
            {%- else -%}
                {%- if show_libname %}<em>{{ libdoc.name }}.</em>{% endif -%}
                    <strong>{{ kw.name }}</strong>
            {%- endif -%}
                &nbsp;&nbsp;&nbsp;&nbsp;
                {%- for arg in kw.args -%}
                    <code>&nbsp;&nbsp;&nbsp;&nbsp;
                    {%- if "=" in arg or "*" in arg -%}
                        <em>{{ arg }}</em>
                    {%- else -%}
                        {{ arg }}
                    {%- endif -%}
                    </code>
                {% endfor %}
        </h3>
        </td></tr></table>
    </div>

    <div class="jp-Robot-Docs-html">
        <blockquote>{{ dollarify(kw.doc) }}</blockquote>
    </div>
</div>
"""

# HTML template for library docs
LIB_TEMPLATE = Template(
    "".join(
        [
            """
{% set show_libname = False %}
{% set is_init = False %}

<div class="jp-Robot-Docs">
    <div class="jp-Robot-Docs-header">
        <table>
            <thead>
                <tr>
                    <th>version</th>
                    <th>scope</th>
                    <th>named<br/>arguments</th>
                    <th>tags</th>
                    <th>inits</th>
                    <th>keywords</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{{ libdoc.version }}</td>
                    <td>{{ libdoc.scope }}</td>
                    <td>{% if named_args %}yes{% else %}no{% endif %}</td>
                    <td>
                        {% for tag in libdoc.tags %}
                        <code>{{ tag }}</code>
                        {% else %}
                        -
                        {% endfor %}
                    </td>
                    <td>
                        {% if libdoc.inits %}
                            <a href="#Importing">{{ libdoc.inits | count }}</a>
                        {% else %}
                            no
                        {% endif %}
                    </td>
                    <td>
                        {% if libdoc.keywords %}
                            <a href="#Keywords">{{ libdoc.keywords | count }}</a>
                        {% else %}
                            no
                        {% endif %}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <h1>{{ libdoc.name }}</h1>

    <div class="jp-Robot-Docs-html">
        <blockquote>{{ dollarify(anchorify(libdoc.doc)) }}</blockquote>
    </div>

    {% if libdoc.inits %}
        {% set is_init = True %}
        <a name="Importing"></a><h1>Importing</h1>
        {% for kw in libdoc.inits %}
            """,
            KW_FRAG,
            """
        {% endfor %}
    {% endif %}

    {% set is_init = False %}
    <a name="Keywords"></a><h1>Keywords</h1>

    {% for kw in libdoc.keywords %}
    """,
            KW_FRAG,
            """
    {% endfor %}
</div>
""",
        ]
    )
)

# template for keywords
KW_TEMPLATE = Template(
    "".join(
        [
            """
{% set show_libname = True %}
{% set is_init = False %}

<div class="jp-Robot-Docs">
    {% set kw = libdoc.keywords[0] %}
""",
            KW_FRAG,
            """
</div>
""",
        ]
    )
)

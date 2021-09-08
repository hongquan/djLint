"""Djlint tests specific to pyproject.toml configuration.

run::

   pytest tests/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config.py::test_custom_tags --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from click.testing import CliRunner

from src.djlint import main as djlint


def test_custom_tags(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/config_custom_tags/html.html", "--check"])

    assert (
        """-{% example stuff %}<p>this is a long paragraph</p>{% endexample %}
+{% example stuff %}
+    <p>
+        this is a long paragraph
+    </p>
+{% endexample %}
"""
        in result.output
    )
    assert result.exit_code == 1


def test_extension(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/config_extension", "--check"])
    assert """Checking""" in result.output
    assert """1/1""" in result.output
    assert """0 files would be updated.""" in result.output
    assert result.exit_code == 0


def test_ignores(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/config_ignores"])
    assert """Linted 1 file, found 0 errors.""" in result.output
    assert result.exit_code == 0


def test_indent(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/config_indent", "--check"])

    assert (
        """-<section><p><div><span></span></div></p></section>
+<section>
+  <p>
+    <div>
+      <span></span>
+    </div>
+  </p>
+</section>"""
        in result.output
    )
    assert result.exit_code == 1
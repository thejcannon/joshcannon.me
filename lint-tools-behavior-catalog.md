# Lint Tools Behavior Catalog

This is a space for me to dump a catalog of lint tool's behaviors,
as seen through the eyes of [`hk`](https://github.com/jdx/hk).

<table>
  <tr>
    <th></th>
    <th>Tool</th>
    <th>List Files Exit Code</th>
    <th>Diff Exit Code</th>
    <th>Fix Exit Code (unfixed/fixed)</th>
  </tr>
  <tr>
    <th rowspan=3>Python</th>
    <td><code><a href="https://docs.astral.sh/ruff/linter/">ruff check</a></code></td>
    <td>(N/A)</td>
    <td>1</td>
    <td>0 (all fixed)</br>1 (violations remain)</td>
  </tr>
  <tr>
    <td><code><a href="https://docs.astral.sh/ruff/formatter/">ruff format</a></code></td>
    <td> (N/A) </td>
    <td> 1 </td>
    <td> 0 </td>
  </tr>
  <tr>
    <td><code><a href="https://black.readthedocs.io/en/stable/index.html">black</a></code></td>
    <td></td>
    <td>1</td>
    <td>0</td>
  </tr>  
</table>

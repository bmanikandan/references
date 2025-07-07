<!DOCTYPE html>
<html>
<head>
  <title>Cytoscape.js Example</title>
  <script src="https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"></script>
  <style>
    #cy {
      width: 800px;
      height: 600px;
      border: 1px solid #ccc;
      display: block;
      margin: 0 auto;
    }
  </style>
</head>
<body>

<h2 style="text-align: center;">Simple Graph Using Cytoscape.js</h2>
<div id="cy"></div>

<script>
  const cy = cytoscape({
    container: document.getElementById('cy'),

    elements: [
      // nodes
      { data: { id: 'a', label: 'Node A' } },
      { data: { id: 'b', label: 'Node B' } },
      { data: { id: 'c', label: 'Node C' } },

      // edges
      { data: { id: 'ab', source: 'a', target: 'b', label: 'Edge A-B' } },
      { data: { id: 'bc', source: 'b', target: 'c', label: 'Edge B-C' } }
    ],

    style: [
      {
        selector: 'node',
        style: {
          'label': 'data(label)',
          'background-color': '#0074D9',
          'color': '#fff',
          'text-valign': 'center',
          'text-halign': 'center'
        }
      },
      {
        selector: 'edge',
        style: {
          'label': 'data(label)',
          'width': 3,
          'line-color': '#aaa',
          'target-arrow-color': '#aaa',
          'target-arrow-shape': 'triangle',
          'curve-style': 'bezier'
        }
      }
    ],

    layout: {
      name: 'grid',
      rows: 1
    }
  });
</script>

</body>
</html>
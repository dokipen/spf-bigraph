function mklinks(data) {
  var nodeMap = {};
  for (var i in data) {
    nodeMap[data[i].name] = Number(i);
  }

  var links = []
  for (var i in data) {
    var node = data[i]
    for (var j in node.children) {
      var child = node.children[j];
      links.push({source: nodeMap[node.name], target: nodeMap[child]})
    }
  }

  return links;
}

function mknodes(data) {
  var nodes = [];
  for (var i in data) {
    var node = data[i];
    nodes.push({name: node.name, x: 0, y: 0});
  }
  return nodes;
}

function run(data) {
  $('svg').remove();
  var width = 800;
  var height = 600;
  var distance = 200;
  var verydark = '#622';
  var dark = '#a88';
  var light = '#daa';
  var head = '#ada';
  var charge = -600;
  var gravity = 0.05;
  var r = 50; // radius
  var sw = 3; // stroke-width

  var svg = d3.select('body')
              .append('svg').attr({
                width: width,
                height: height
              });
  svg.append('defs').append('marker').attr({
    'id': 'head',
    orient: 'auto',
    markerWidth: 8,
    markerHeight: 8,
    refX: 21,
    refY: 4,
  }).append('path').attr({
    d: 'M0,0 V8 L4,4 Z',
    fill: dark
  });

  var nodes = mknodes(data);
  var links = mklinks(data);

  var force = d3.layout.force()
                .size([width, height])
                .nodes(nodes)
                .links(links)
                .charge(charge)
                .gravity(gravity)
                .linkDistance(distance);

  var link = svg.selectAll('.link')
    .data(links)
    .enter()
    .append('path')
    .attr({ 'class': 'link', });

  var node = svg.selectAll('.node')
    .data(nodes)
    .enter()
    .append('g')
    .call(force.drag)
    .attr('class', 'node');

  node.append('ellipse')
       .attr({
         'class': function(_, i) {
           return i == 0 && 'head';
         }
       });

  node.append('text')
       .attr({
         x:r,
         y:r
       })
       .text(function(d) { return d.name });

  force.on('tick', function() {
    svg.selectAll('.link').attr({
      d: function(d) {
        var x1 = d.source.x + r;
        var y1 = d.source.y + r;
        var x2 = d.target.x + r;
        var y2 = d.target.y + r;
        return "M"+x1+","+y1+" "+x2+","+y2;
      },
    });
    svg.selectAll('.node').attr({
      transform: function(d) {
        return "translate("+d.x+","+d.y+")"
      }
    });
  });

  force.start();
}

function load(domain) {
  d3.json("../data/"+domain+".json", function(e, data) {
    run(data);
  });
}

jQuery(function($) {
  domains = domains.sort();
  $('body').append($("<div>").addClass('menu'));
  domains.forEach(function(d) {
    var item = $('<p>'+d+'</p>').addClass('item').click(function() {
      load(d);
      $('.menu .item').removeClass('selected');
      $(this).addClass('selected');
    });
    item.append('<a class="link pdf" href="docs/'+d+'.pdf" download>pdf</a>');
    item.append('<a class="link png" href="images/'+d+'.png" download>png</a>');
    $('.menu').append(item);
  });
  $('.menu .item').first().addClass('selected');
  load(domains[0]);
});

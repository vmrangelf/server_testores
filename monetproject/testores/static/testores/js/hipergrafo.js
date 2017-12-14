//Variables de configuracion
var width_graph = 1200,
    height_graph = 600;//tamaño del los svg

var radius = [20,12,5]; //tamaño del radio.
var max_radius= 25; //tamaño del radio al hacer over
var tiempo_animacion=200;//Tiempo de la animacion del crecimiento del nodo.
var posicion_texto_inicial=[23,15,7];
var posicion_texto_animacion=28;

var color_blanco = "#FFF";
var color_negro ="#333";
var color_gris = "#D0D0D0";
var tamanio_borde_svg=2;

var tipos_relacion=["direct","indirect"];
var graph_nodes;
var path;
var info;

function draw_graph(data,id_graph) {

  var size = 1;

  var zoom = d3.behavior.zoom()
        .scaleExtent([-10, 10])
        .on("zoom", zoomed);

  var svg = d3.select(id_graph).append("svg")
      //.attr("id",id)
      .attr("width", width_graph)
      .attr("height", height_graph)
      .call(zoom)
      .style("cursor","all-scroll")
      ;

  function zoomed() {
        container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
      }

    //carga de la informacion de json
    var links = data.links;
    var hyperedges = data.hyperedges;
    info = data.nodes;

    hyperedges.forEach(function(hyperedge){
        info[hyperedge].color = randomColor({luminosity: 'dark'});
    });

    var container = svg.append("g");

    //se crean los enlaces entre los nodos
    links.forEach(function(link) {
      link.source = info[link.parent];
      link.target = info[link.child];
    });

    //Agregar el id_graph al que pertenece cada nodo, necesario para multiples graficas en una misma ventana
    for (var nodo in info)
    {
        info[nodo].id_graph=id_graph;
        info[nodo].graph_size=size;
    }


    var force = d3.layout.force()
        .nodes(d3.values(info))//se seleccionan los nodos
        .links(links)//se seleccionan las aristas
        .size([width_graph, height_graph])
        .linkDistance(function(d){
            if(d.source.level==1)
            {
                return (Math.floor((Math.random() * 100) + 20));
            }
            return (100);
        })
        .charge(-500);

    //agrega las listas y las aristas
    path = container.append("g").selectAll("path")
        .data(force.links())
        .enter().append("path")
        .attr("fill","none")
        .style("stroke", function(d) { if(d.source.level==2 && d.target.level==3){return d.source.color;}else if(d.source.level==1 && d.target.level==3) {return color_negro;} return d.target.color;})
        .style("stroke-width","2.5px");

    //se define el nodo
    graph_nodes = container.selectAll(".node")
        .data(force.nodes())
      .enter().append("g")
        .style("cursor","default")
        .on("mouseover", mouseover)
        .on("mouseout", mouseout);

    //se agrega el nodo
    graph_nodes.append("circle")
        .attr("r", function(d){return radius[d.level-1];})
        .style("fill", function(d){if(d.level == 1){return color_blanco;} else if(d.level == 2){return color_gris;} return color_negro;})
        .style("stroke",color_negro)
        .style("stroke-width", function(d){if(d.level == 1){return 4;} return 1.5;});

    //se agrega el texto
    graph_nodes.append("text")
        .attr("x", function(d) { return posicion_texto_inicial[d.level-1]; })
        .attr("dy", ".35em")
        .style("fill", "black")
        .style("stroke", "none")
        .style("font", "14px sans-serif")
        .text(function(d) { return d.word; });

    graph_nodes.each(function(node){
        node.nodosIncidentes = path
            .filter(function(arista) {
                return info[arista.parent] === node ||
                       info[arista.child] === node;
            });
    });

   graph_nodes.each(function(node){
     node.adyacentes = graph_nodes.filter(function(otroNodo){
             var esAdjacente = false;
             if (otroNodo !== node) {
                 node.nodosIncidentes.each(function(arista){
                     otroNodo.nodosIncidentes.each(function(otraArista){
                         if (arista === otraArista) {
                             esAdjacente = true;
                         }
                     });
                 });
             }
             return esAdjacente;
         });
   });

    // la funcion que dibuja los elementos del grafico
    function tick() {
      path.attr("d", arista_derecho); //se dibuja la arista
      graph_nodes.attr("transform", transform);//se dibuja el nodo
    }

    //funcion para dibujar la arista recto
    function arista_derecho(d) {
      var dx = d.target.x - d.source.x,
          dy = d.target.y - d.source.y,
          dr = Math.sqrt(dx * dx + dy * dy);
      return "M" + d.source.x + "," + d.source.y + " " + d.target.x + "," + d.target.y;
    }

    function transform(d) {
      return "translate(" + d.x + "," + d.y + ")";
    }

    function mouseover(node) {

      // Oculto todos los nodos
      graph_nodes.selectAll('circle')
                .transition()
                .duration(tiempo_animacion)
                .style("fill", color_gris)
                .style("stroke",color_gris);

      graph_nodes .selectAll('text')
                .transition()
                .duration(tiempo_animacion)
                .style("fill", color_gris);

      // Selecciono todos los nodos adyacentes y los muestro
      node.adyacentes.selectAll('circle')
          .transition()
          .duration(tiempo_animacion)
          .style("fill", function(d){if(d.level == 1){return color_blanco;} else if(d.level == 2){return color_gris;} return color_negro;})
          .style("stroke",color_negro);

      node.adyacentes.selectAll('text')
          .transition()
          .duration(tiempo_animacion)
          .style("fill", "black");

      // Selecciono el nodo que elegi y lo muestro
      d3.select(this).select("circle")
        .transition()
        .duration(tiempo_animacion)
        .style("fill", function(d){if(d.level == 1){return color_blanco;} else if(d.level == 2){return color_gris;} return color_negro;})
        .style("stroke",color_negro);

      d3.select(this).select("text").transition()
          .duration(tiempo_animacion)
          .style("font", "20px sans-serif")
          .text(function(d) { return d.word; });

      // Seleccionar solo las aristas que sean adyacentes al nodo consultado
      path.transition()
          .duration(tiempo_animacion)
          .style("stroke",color_gris);

      node.nodosIncidentes
          .transition()
          .duration(tiempo_animacion)
          .style("stroke", function(d) { if(d.source.level==2 && d.target.level==3){return d.source.color;}else if(d.source.level==1 && d.target.level==3) {return color_negro;} return d.target.color;})

    }

    this.mouseoverTest = function(node) {

      // Oculto todos los nodos
      graph_nodes.selectAll('circle')
                .transition()
                .duration(tiempo_animacion)
                .style("fill", color_gris)
                .style("stroke",color_gris);

      graph_nodes .selectAll('text')
                .transition()
                .duration(tiempo_animacion)
                .style("fill", color_gris);

      // Selecciono todos los nodos adyacentes y los muestro
      node.adyacentes.selectAll('circle')
          .transition()
          .duration(tiempo_animacion)
          .style("fill", function(d){if(d.level == 1){return color_blanco;} else if(d.level == 2){return color_gris;} return color_negro;})
          .style("stroke",color_negro);

      node.adyacentes.selectAll('text')
          .transition()
          .duration(tiempo_animacion)
          .style("fill", "black");

      // Selecciono el nodo que elegi y lo muestro
      d3.select(this).select("circle")
        .transition()
        .duration(tiempo_animacion)
        .style("fill", function(d){if(d.level == 1){return color_blanco;} else if(d.level == 2){return color_gris;} return color_negro;})
        .style("stroke",color_negro);

      d3.select(this).select("text").transition()
          .duration(tiempo_animacion)
          .style("font", "20px sans-serif")
          .text(function(d) { return d.word; });

      // Seleccionar solo las aristas que sean adyacentes al nodo consultado
      path.transition()
          .duration(tiempo_animacion)
          .style("stroke",color_gris);

      node.nodosIncidentes
          .transition()
          .duration(tiempo_animacion)
          .style("stroke", function(d) { if(d.source.level==2 && d.target.level==3){return d.source.color;}else if(d.source.level==1 && d.target.level==3) {return color_negro;} return d.target.color;})

    }

    function mouseout() {

      d3.select(this).select("text").transition()
          .duration(tiempo_animacion)
          .style("font", "14px sans-serif")
          .text(function(d) { return d.word; });

      graph_nodes.selectAll('circle')
                .transition()
                .duration(tiempo_animacion)
                .style("fill", function(d){if(d.level == 1){return color_blanco;} else if(d.level == 2){return color_gris;} return color_negro;})
                .style("stroke",color_negro)
                .style("stroke-width", function(d){if(d.level == 1){return 4;} return 1.5;});

      graph_nodes.selectAll('text')
                .transition()
                .duration(tiempo_animacion)
                .style("fill", "black")
                .style("font", "14px sans-serif")
                .text(function(d) { return d.word; });

      path.transition()
          .duration(tiempo_animacion)
          .style("stroke", function(d) { if(d.source.level==2 && d.target.level==3){return d.source.color;}else if(d.source.level==1 && d.target.level==3) {return color_negro;} return d.target.color;})

    }

    //acomodo del grafo
    force.on("tick", tick);
    force.start();

};

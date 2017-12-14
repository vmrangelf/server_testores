matrizBasicaResultante = "";
matrizBasicaResultanteH = "";
function seleccionarMatriz() {
	var selectMatriz = document.getElementById("selectMatriz");
    var selectedValue = selectMatriz.options[selectMatriz.selectedIndex].value;
	$.ajax({
		url: '/testores/ajax/obtenerMatriz/',
        data: {'selectedValue': selectedValue},
        dataType: 'json',
        success: function (response) {
			var matriz = JSON.parse(response)	
			var matrizTestores = crearTablaTestor(matriz.tt);
			var matrizBasica = crearTablaMatriz(matriz.mat);
        	var tblRow = "<tr id=\"fil\">" + "<td>" + selectedValue + "</td>" + "<td>" + matrizBasica + "</td>" +
        	"<td>" + matrizTestores + "</td>" + "<td>" + matriz.ref + "</td>" + "</tr>";
        	$("#fil").remove();
        	$(tblRow).appendTo($("#matrixData"));		
        	obtenerHipergrafoCatalogo();
        	$("#divHyperCat").attr( "style", "visibility: visible;" );
		},
		error: function(error) {
			console.log(error);
		}
	});
}

function obtenerHipergrafoCatalogo() {
	var selectMatriz = document.getElementById("selectMatriz");
    var selectedValue = selectMatriz.options[selectMatriz.selectedIndex].value;
    var centro = 'False';
    var repeticion = 'True'; 
    if ($("#centroRadio").is(":checked")){
    	centro = 'True';
    	repeticion = 'False';
	}else if ($("#repRadio").is(":checked")) {
		centro = 'False';
		repeticion = 'True';
	}
	$.ajax({
		url: '/testores/ajax/obtenerHipergrafoCatalogo/',
        data: {'selectedValue': selectedValue,
    			'centro': centro,
    			'repeticion': repeticion,},
        dataType: 'json',
        success: function (response) {
			var jsonResp = JSON.parse(response);
			$('#hipergrafoCatalogo').empty();
      		draw_graph(jsonResp,"#hipergrafoCatalogo");							
		},
		error: function(error) {
			console.log(error);
		}
	});
}

function operacionPhi(){
	var selectMatriz = document.getElementById("selectMatrizPhi");
	var selectedValue = selectMatriz.options[selectMatriz.selectedIndex].value;
	var exp = $("#expPhi").val();
	$.ajax({
		url: '/testores/ajax/operacionPhi/',
        data: {'selectedValue': selectedValue,
			   'exp': exp,
			  },
        dataType: 'json',
        success: function (response) {
			var resp = JSON.parse(response)	
			var matrizTestores = crearTablaTestor(resp.testoresTipicos);
			var matrizBasica = crearTablaMatriz(resp.matrizBasica);
        	var tblRow = "<tr> <th>Testores tipicos</th><th>Matriz Basica</th></tr>" +
				"<tr>" + "<td>" + matrizTestores+ "</td>" +
        		"<td valign=\"top\">" + matrizBasica+ "</td>" + "</tr>";
        	$(tblRow).appendTo($("#phiResult"));				
		},
		error: function(error) {
			console.log(error);
		}
	});
}

function obtenerHipergrafoResultante() {
	var matrizBasica = matrizBasicaResultanteH;
	var centro = 'False';
    var repeticion = 'True'; 
    if ($("#centroRadioR").is(":checked")){
    	centro = 'True';
    	repeticion = 'False';
	}else if ($("#repRadioR").is(":checked")) {
		centro = 'False';
		repeticion = 'True';
	}
	var dataP = JSON.stringify({'data': matrizBasica,});
	$.ajax({
		url: '/testores/ajax/obtenerHipergrafoResultante/',
        data: {'matrizBasica': dataP,
    			'centro': centro,
    			'repeticion': repeticion,},
        dataType: 'json',
        success: function (response) {
			var jsonResp = JSON.parse(response);
			$('#hipergrafoResultante').empty();
      		draw_graph(jsonResp,"#hipergrafoResultante");								
		},
		error: function(error) {
			console.log(error);
		}
	});
}

function errorExp(){
	$('#errorModal').modal('show');
}

function calcularMB(){
	var exp = $("#expresion").val();
	var jsonProc = analizarExp(exp);
	//console.log(jsonProc);
	var jsonPrueba = "{\"p1\": \"1\"}";
	$.ajax({
		contentType: "application/json",
		url: '/testores/ajax/calcularMB/',
        data: {'content': jsonProc,},
        //data: jsonProc,
        dataType: 'json',
        success: function (response) {
			var matriz = JSON.parse(response)	
			try{
				var matrizTestores = crearTablaTestor(matriz.tt);
				var matrizBasica = crearTablaMatriz(matriz.mat);
        		var tblRow = "<tr id=\"filMR\">" + "<td>" + matriz.ref + "</td>" + "<td>" + matrizBasica + "</td>" +
        		"<td>" + matrizTestores + "</td>" + "<td>" + exp + "</td>" + "</tr>";
        		$("#filMR").remove();
        		$(tblRow).appendTo($("#mbResult"));
        		matrizBasicaResultante = JSON.stringify(matriz);
        		matrizBasicaResultanteH = matriz.mat;
        		document.getElementById("save-btn").disabled = false; 
        		obtenerHipergrafoResultante();
        		$("#divHyperRec").attr( "style", "visibility: visible;" );	
        	}catch(err) {
				errorExp();
			}					
		},
		error: function(error) {
			console.log(error);
		}
	});
}

function crearTablaMatriz(matriz){
	var result = "<table class= \"table table-bordered\" id = \"mBasica\" border=0>";
	result += "<thead>"
	for(var h = 0; h < matriz[0].length; h++){
		result += "<th class=\"active\">" + (h + 1) + "</th>";
	}
	result += "</thead><tbody>" 
    for(var i = 0; i < matriz.length; i++) {
        result += "<tr>";
        for(var j = 0; j < matriz[i].length; j++){
            result += "<td>" + matriz[i][j] + "</td>";
        }
        result += "</tr>";
    }
    result += "</tbody></table>";
	return result;
}

function crearTablaTestor(testores){
	var result = "<table id = \"mTestTip\" border=0 >";
	result += "<tbody>" 
    for(var i = 0; i < testores.length; i++) {
        result += "<tr><td onclick=\"resaltarTestor(this)\" name=\""+ testores[i] +"\" >" 
        			+ testores[i] + "</td></tr>";
    }
    result += "</tbody></table>";
	return result;
}

function saveMatrix(){
	var blob = new Blob([matrizBasicaResultante], {type: "text/plain;charset=utf-8"});
	saveAs(blob, "matrizResultante.txt");
}

function resaltarTestor(test){
	var nodeList = [];
	var thisflist = [];
	var rasgos = (test.textContent).split(",");
	var nomVert = "v"+rasgos[0];
	nodeList[0] = info[nomVert];
	thisflist[0] =  buscarThisf(nomVert);
	nomVert = "v"+rasgos[1];
	nodeList[1] = info[nomVert];
	thisflist[1] =  buscarThisf(nomVert);
	mouseoverP(thisflist, nodeList);
	console.log("hyperg");
}
function buscarThisf(vert){
	for (var i = 0; i < (graph_nodes[0]).length; i++) {
		if (graph_nodes[0][i].textContent == vert){
			return graph_nodes[0][i];
		}
	}
}

function mouseoverP (thisflist, nodeList) {
	var node;
	var thisf;
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
    for (var i = 0; i < nodeList.length; i++){
    	node = nodeList[i];
      	thisf = thisflist[i];

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
      d3.select(thisf).select("circle")
        .transition()
        .duration(tiempo_animacion)
        .style("fill", function(d){if(d.level == 1){return color_blanco;} else if(d.level == 2){return color_gris;} return color_negro;})
        .style("stroke",color_negro);

      d3.select(thisf).select("text").transition()
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
}
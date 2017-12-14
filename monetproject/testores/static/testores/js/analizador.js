const OPERADORES = ["P", "T", "G", "p", "t", "g"];
const SIMBOLOS = [")", "(", ","];

const lex = str => str.split(' ').map(s => s.trim()).filter(s => s.length);

const Op = Symbol('op');
const Num = Symbol('num');
const Mat = Symbol('mat');

function esOperador(caracter){
	var x;
	for (x in OPERADORES) {
    	if (OPERADORES[x] == caracter) return true;
	}
	return false
}
function esSimbolo(caracter){
	var x;
	for (x in SIMBOLOS) {
    	if (SIMBOLOS[x] == caracter) return true;
	}
	return false
}

const parse = tokens => {
  let c = 0;
	
	const peek = function(){return tokens[c];};
	const consume = function(){return tokens[c++];};
	
	const parseNum = function(){
		return {val: parseInt(consume()), type: Num, tipo: "Num"};
	};
	
	const parseMat = function(){
		return {val: consume(), type: Mat, tipo: "Mat"};
	};

  const parseOp = function() {
    const node = { val: consume(), type: Op, tipo:"Op", expr: [] };
    while (peek()){
		node.expr.push(parseExpr());
		var l = node.expr.length;
		if(l==2){
			return node;
		}		
	}
    return node;
  };
	
  const parseExpr = function(){
	  if(esOperador(peek())){
		  return parseOp();
	  }else if(/^\d+$/.test(peek())){
		  return parseNum();
	  }else{
		  return parseMat();
	  }
  };

  return parseExpr();
};

function errorExp(){
	//alert("Error en la expresión");
	$('#errorModal').modal('show');
}

function analizarExp(exp){
	var ch, error = false;
	//console.log(exp);
	try{
	if(((exp.match(/\(/g)).length == (exp.match(/\)/g)).length) 
		&& esOperador(exp[0]) && (")" == exp[exp.length -1])){
		var exp1 = (exp.trim()).replace(/\s/g,"");
		//console.log(exp1);
		for (ch = 0; ch < exp1.length; ch++) {
			if (exp1[ch] == "(") {
				if (!esOperador(exp1[ch-1]) || /^\d+$/.test(exp1[ch+1])
					|| esSimbolo(exp1[ch+1])){
					errorExp();
					error = true;
				}
			}else if(exp1[ch] == ")"){
        		if(esOperador(exp1[ch-1])){
					errorExp();
					error = true;					
				}
			}else if (exp1[ch] == ","){
				if(esOperador(exp1[ch-1]) || ("," == exp1[ch-1]) || ("(" == exp1[ch-1]) ||
				   esSimbolo(exp1[ch+1])){
					errorExp();
					error = true;					
				}
			} 
		}
		if(!error){
			var expAn = exp1.replace(/\(/g," ").replace(/\)/g, " ").replace(/\,/g, " ");
			//console.log(expAn);
			//console.log(lex(expAn));
			var expParse = parse(lex(expAn));
			return JSON.stringify(expParse);
			//console.log(expParse);
			//console.log(jsonParse)
		}		
	}else{
		errorExp();
	}
	}
	catch(err) {
		errorExp();
	}
}
// Foundation JavaScript
// Documentation can be found at: http://foundation.zurb.com/docs
$(document).foundation();

function previewTable(){
    var data = $('textarea[name=table_data]').val();
	var rows = data.split("\n");
	var table = $('<table />');
	var rowCellCount =0;
	var columnCount = rows[0].split("\t").length;
	for(var y in rows) {
		var cells = rows[y].split("\t");
		var row = $('<tr />');
		for(var x in cells) {
			row.append('<td>'+cells[x]+'</td>');
		}
		table.append(row);
	}

	// Insert into DOM
	$('#preview-header').html("<h2>Preview</h2><p>This is what your table will look like:</p>");
	$('#table_preview').html(table);

}


// function previewTable(){

//     var data = $('textarea[name=excel_data]').val();
// 	var rows = data.split("\n");
// 	var table = $('<table />');
// 	var rowCellCount =0;
// 	var columnCount = rows[0].split("\t").length;
// 	var row = $('<tr />');
// 	for(var y in rows) {
// 		// var row = $('<tr />');
// 		// for(var x in cells) {
// 		// 	row.append('<td>'+cells[x]+'</td>');
// 		// }
// 		// table.append(row);
	
// 		if (cells[0].length > 0){
// 			rowCellCount += cells.length;
// 		}
// 		//check if number of cells equals number of columns
// 		if (rowCellCount==columnCount){
// 			for(var z in cells){
// 				statement += "'" + cells[z] + "'";
// 				if (z<cells.length-1){
// 					statement+=", ";

// 				}
// 				else{
// 					console.log(y + " "+ rows.length);
// 					if (y<rows.length-1){
// 						statement+="), (";
// 					}
// 				}
// 			}
// 			//reset cellcount
// 			rowCellCount = 0;
// 		}
// 		//incomplete row detected
// 		else{
// 			//loop through all cells in the incomplete row
// 			for(var i in cells){

// 				// if the current cell has any contents
// 				if (cells[i].length > 0){
// 					statement += "'" + cells[i] + "'";
// 					console.log(rowCellCount);
// 					if (rowCellCount==columnCount){
// 						// console.log(cells + " " + cells.length + "///rcc: " +rowCellCount);
// 						statement+=")";
// 						rowCellCount = 0;
// 					}
// 					else{
// 						statement+=", ";
// 					}

// 				}
// 			}
// 		}

// 	}
// 	// Insert into DOM
// 	$('#excel_table').html(table);
// }

function generateCreate(){
	var statement = "CREATE TABLE " + $('input[name=table_name]').val() +" (";
    var data = $('textarea[name=table_data]').val();
	var rows = data.split("\n");
	
	var headers = rows[0].split("\t");
	for (var x in headers){
		statement += headers[x];
		console.log(headers[x]);
		statement += " varchar(150)";
		if (x<headers.length-1){
			statement+=", ";
		}
	}
	statement +=");";

	$('#create_statement').html(statement);
}

function generateInsert(){
	var statement = "INSERT INTO " + $('input[name=table_name]').val() +" (";
    var data = $('textarea[name=table_data]').val();
	var rows = data.split("\n");
	var rowCellCount =0;
	var columnCount = rows[0].split("\t").length;

	for (var y in rows){
		//find column names
		if (y<1){
			var headers = rows[y].split("\t");
			for (var x in headers){
				statement += headers[x];
				if (x<headers.length-1){
					statement+=", ";
				}
				else {
					statement+=") VALUES (";
				}
			}
		}
		//start breaking down rows to insert

		else {
			var cells = rows[y].split("\t");
			if (cells[0].length > 0){
				rowCellCount += cells.length;
			}

			//check if number of cells equals number of columns
			if (rowCellCount==columnCount){
				for(var z in cells){
					statement += "'" + cells[z] + "'";
					if (z<cells.length-1){
						statement+=", ";

					}
					else{
						console.log(y + " "+ rows.length);
						if (y<rows.length-1){
							statement+="), (";
						}
					}
				}
				//reset cellcount
				rowCellCount = 0;
			}
			//incomplete row detected
			else{
				//loop through all cells in the incomplete row
				for(var i in cells){

					// if the current cell has any contents
					if (cells[i].length > 0){
						statement += "'" + cells[i] + "'";
						console.log(rowCellCount);
						if (rowCellCount==columnCount){
							// console.log(cells + " " + cells.length + "///rcc: " +rowCellCount);
							statement+=")";
							rowCellCount = 0;
						}
						else{
							statement+=", ";
						}

					}
				}

			}
		}
	}
	statement +=");";
	$('#insert_statement').html(statement);
	// $('#excel_table').html(statement);
}
// Foundation JavaScript
// Documentation can be found at: http://foundation.zurb.com/docs
$(document).foundation();
console.log("Hello! Thanks for using SQL Butler");
$("#table_data").on("input", function() {
    previewTable4();
});

function previewTable4(){
    var data = $('textarea[name=table_data]').val();
	var rows = data.split("\n");
	var table = $('<table />');
	var rowCellCount =0;
	var columnCount = rows[0].split("\t").length;
	//for each line in the graph
	for(var y in rows) {
		var cells = rows[y].split("\t");
		var row = $('<tr />');
		var incomplete_row = $('<tr />');
		var incomplete_row_bool = false;
		rowCellCount+=cells.length;
		//if the row is complete
		if (rowCellCount>=columnCount){
			//for each cell in each line
			if (incomplete_row_bool===false){
				for(var x in cells) {
					row.append('<td>'+cells[x].split(' ').join('_')+'</td>');
					rowCellCount=0;
				}
				table.append(row);
			}
			else{
				for(var xprime in cells) {
					incomplete_row.append('<td>'+cells[xprime].split(' ').join('_')+'</td>');
				}
				table.append(row);
				incomplete_row_bool=false;
			}
		}
		//if the row is not complete
		else{
			for(var z in cells){
				rowCellCount+=1;
				incomplete_row.append('<td>'+cells[z].split(' ').join('_')+'</td>');
				incomplete_row_bool=true;
				console.log(cells[z]);
			}
		}
	}

	// Insert into DOM
	$('#preview-header').html("<h2>Preview</h2><p>This is what your table will look like:</p>");
	$('#table_preview').html(table);

}

function previewTable(){
    var data = $('textarea[name=table_data]').val();
	var rows = data.split("\n");
	var table = $('<table />');
	for(var y in rows) {
		var cells = rows[y].split("\t");
		var row = $('<tr />');
		for(var x in cells) {
			row.append('<td>'+cells[x].split(' ').join('_')+'</td>');
		}
		table.append(row);
	}

	// Insert into DOM
	$('#preview-header').html("<h2>Preview</h2><p>This is what your table will look like:</p>");
	$('#table_preview').html(table);

}

function previewTable2(){
    var data = $('textarea[name=table_data]').val();
	var rows = data.split("\n");
	var table = $('<table />');
	var rowCellCount =0;
	var columnCount = rows[0].split("\t").length;
	var count =0;
	for(var i in rows) {
		console.log(count +" "+ columnCount);
		var headers = rows[i].split("\t");
		var row_html = $('<tr />');
		for (var header in headers){
			if (count<columnCount){
				row_html.append('<td>'+headers[header].split(' ').join('_')+'</td>');
				count+=1;
			}
			if (count>=columnCount){
				table.append(row_html);
			}
		}

	// Insert into DOM
	$('#preview-header').html("<h2>Preview</h2><p>This is what your table will look like:</p>");
	$('#table_preview').html(table);
	}
}

function previewTable1(){
    var data = $('textarea[name=table_data]').val();
	var rows = data.split("\n");
	var table = $('<table />');
	var rowCellCount =0;
	var columnCount = rows[0].split("\t").length;
	var row_html = $('<tr />');
	
	for(var row in rows) {
		if (row<1){
			var headers = rows[row].split("\t");
			for (var header in headers){
				row_html.append('<td>'+headers[header].split(' ').join('_')+'</td>');
			}
			table.append(row_html);
		}

		else{
			var cells = rows[row].split("\t");
			if (cells[0].length > 0){
				rowCellCount += cells.length;
			}
			console.log("row "+row +" rcc "+rowCellCount + " cc " +columnCount);

			//check if number of cells equals number of columns
			if (rowCellCount==columnCount){
				for(var cell in cells){
					row_html.append('<td>'+cells[cell].split(' ').join('_')+'</td>');
					if (cell>=cells.length-1){
						table.append(row_html);
					}
				}
				//reset cellcount
				rowCellCount = 0;
			}
			//incomplete row detected
			else{
				//loop through all cells in the incomplete row
				for(var cel in cells){
					// if the current cell has any contents
					if (cells[cel].length > 0){
						row_html.append('<td>'+cells[cel].split(' ').join('_')+'</td>');
						if (rowCellCount==columnCount){
							// console.log(cells + " " + cells.length + "///rcc: " +rowCellCount);
							table.append(row_html);
							rowCellCount = 0;
						}
					}
				}

			}
		}
		table.append(row);
	}
	

	// Insert into DOM
	$('#preview-header').html("<h2>Preview</h2><p>This is what your table will look like:</p>");
	$('#table_preview').html(table);


}

function generateCreate(){
	var statement = "<span class='kwd'>CREATE TABLE </span>" + $('input[name=table_name]').val().split(' ').join('_') +" (";
    var data = $('textarea[name=table_data]').val();
	var rows = data.split("\n");
	
	var headers = rows[0].split("\t");
	for (var header in headers){
		statement += headers[header].split(' ').join('_');
		statement += " varchar(150)";
		if (header<headers.length-1){
			statement+=", ";
		}
	}
	statement +=");";

	$('#create_statement').html("<p>Results:</p><div class='panel'>" + statement+"</div>");
}







function generateInsert(){
	var statement = "<span class='kwd'>INSERT INTO </span>" + $('input[name=table_name]').val() +" (";
    var data = $('textarea[name=table_data]').val();
	var rows = data.split("\n");
	var rowCellCount =0;
	var columnCount = rows[0].split("\t").length;

	for (var row in rows){
		//find column names
		if (row<1){
			var headers = rows[row].split("\t");
			for (var header in headers){
				statement += headers[header].split(' ').join('_');
				if (header<headers.length-1){
					statement+=", ";
				}
				else {
					statement+=") <span class='kwd'>VALUES </span>(";
				}
			}
		}
		//start breaking down rows to insert
		else {
			var cells = rows[row].split("\t");
			if (cells[0].length > 0){
				rowCellCount += cells.length;
			}

			//check if number of cells equals number of columns
			if (rowCellCount==columnCount){
				for(var cell in cells){
					statement += "<span class='str'>'" + cells[cell] + "'</span>";
					if (cell<cells.length-1){
						statement+=", ";

					}
					else{
						if (row<rows.length-1){
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
				for(var cel in cells){
					// if the current cell has any contents
					if (cells[cel].length > 0){
						statement += "<span class='str'>'" + cells[cel] + "'</span>";
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
	$('#insert_statement').html("<div class='panel'>" + statement+"</div>");
}
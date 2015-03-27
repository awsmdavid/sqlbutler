// Foundation JavaScript
// Documentation can be found at: http://foundation.zurb.com/docs
$(document).foundation();
$('.toggle-expand').click(function(){
	$(this).siblings(".word-metadata").toggle(200, function() {
		if ($(this).siblings(".toggle-expand").html() == "[+]"){
			$(this).siblings(".toggle-expand").html("[-]");
		}
		else{
			$(this).siblings(".toggle-expand").html("[+]");
		}
	});
});
	// .css( "display", "inline" );
// $('.home').click(function() {
	// $(this).css('background-image', 'url(images/tabs3.png)');
// });

// document.getElementById("toggle-expand").onclick = function () { $(this).css('color','red'); };
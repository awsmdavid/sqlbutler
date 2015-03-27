// Foundation JavaScript
// Documentation can be found at: http://foundation.zurb.com/docs
$(document).foundation();
$('.toggle-expand').click(function(){
	$(this).siblings(".word-metadata").toggle(200, function() {
		word = $(this).siblings(".word").html();
		open_tag = '<span class="highlighted-text">';
		close_tag = "</span>";


		if ($(this).siblings(".toggle-expand").html() == "[+]"){
			$(this).siblings(".toggle-expand").html("[-]");
			//highlight word
			// var word_regex = new RegExp('^' + word + '$', 'g');
			var word_regex = new RegExp(word, 'gi');
			$('#original-text').html($('#original-text').html().replace(word_regex, open_tag+word+close_tag));
			// $("#masthead").html("yo");
		}
		//todo: undo capitalization somehow, word is always all caps
		else{
			var highlighted_text_regex = new RegExp(open_tag + word + close_tag, 'gi');
			$(this).siblings(".toggle-expand").html("[+]");
			$('#original-text').html($('#original-text').html().replace(highlighted_text_regex, word));
		}
	});
});
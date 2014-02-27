$(document).ready(function() {
// Handler for .ready() called.

	
	
// Add fancybox class to anchored images
    //$(document).find('a').has('img').addClass('fancybox');
// Attach fancyBox
		
        
    $(".fancybox").fancybox();
        
	$("img.lazy").show().lazyload();



});



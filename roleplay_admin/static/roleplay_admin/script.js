$(document).ready(function() {
// Handler for .ready() called.

	$('.datepicker').datepicker({"format": "dd.mm.yyyy"}).on('changeDate', 
		function(ev) {
			$(this).datepicker('hide');
		});
	

});



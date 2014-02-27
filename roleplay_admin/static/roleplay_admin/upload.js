$('#dnd').fileapi({
   url: upload_to,
   paramName: 'image',
   data: {	"csrfmiddlewaretoken": csrftoken,
   			"game": game_id,
			"location": location_id,
			"event": event_id,
   },
   autoUpload: true,
   duplicate: false,
   elements: {
      list: '.js-files',
      file: {
         tpl: '.js-file-tpl',
         preview: {
            el: '.b-thumb__preview',
            width: 80,
            height: 80
         },
         upload: { show: '.progress' },
         complete: { hide: '.progress' },
         progress: '.progress .bar'
      },
      dnd: {
         el: '.b-upload__dnd',
         hover: 'b-upload__dnd_hover',
         fallback: '.b-upload__dnd-not-supported'
      }
   },
	filterFn: function (file, info){ 
		//console.log(info.width);
		//console.log(info.height);
		
		if (info.width < 320 || info.height < 240) {
			alert("Выберите изображение размером не меньше 320x240");
			return false;
		}
		if (info.width > 3840 || info.height > 2160) {
			alert("Выберите изображение размером не больше 3840x2160");
			return false;
		}
		
		//return /^image/.test(file.type) && info.width > 320;
		return /^image/.test(file.type);
		
	},
	onComplete: function(evt, uiEvt){
	    var error = uiEvt.error;
	    var result = uiEvt.result; // server response
		//console.log(result);
	    
	    if (result.status == "error") {
	    	alert(result.err_messages);
		}
	    	
	},
	/*
	onFileComplete: function(evt, uiEvt){
	    var error = uiEvt.error;
	    var result = uiEvt.result; // server response
		console.log(result);
	    
	    if (result.status == "error") {
	    	alert(result.err_messages);
	    }
	},
   */
   
   
   
   
   
   
   
   
   
   
});
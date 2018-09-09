function submit(){
	$(document).ready(function(){
	    $("button").click(function(){
	       $.ajax({
			  type: "POST",
			  url: '/workflow',
			  data: "nunce",
			  success: function(){
			  	alert('success');
			  },
			  error: function(){
			  	alert('error');
			  }
			});
	    });
	});
}
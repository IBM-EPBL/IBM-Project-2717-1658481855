$(document).ready(function() {
	
	
	$('#submit').click(function () {		
		
		
		var name = $('input[name=name]');
		var email = $('input[name=email]');
		var regx = /^([a-z0-9_\-\.])+\@([a-z0-9_\-\.])+\.([a-z]{2,4})$/i;
		var comment = $('textarea[name=comment]');
		var returnError = false;
		
		
		if (name.val()=='') {
			name.addClass('error');
			returnError = true;
		} else name.removeClass('error');
		
		if (email.val()=='') {
			email.addClass('error');
			returnError = true;
		} else email.removeClass('error');		
		
		if(!regx.test(email.val())){
          email.addClass('error');
          returnError = true;
		} else email.removeClass('error');
		
		
		if (comment.val()=='') {
			comment.addClass('error');
			returnError = true;
		} else comment.removeClass('error');
		
	
		if(returnError == true){
			return false;	
		}
		
		
		
		var data = 'name=' + name.val() + '&email=' + email.val() + '&comment='  + encodeURIComponent(comment.val());

		
		$('.text').attr('disabled','true');
		
		
		$('.loading').show();
		
		
		$.ajax({
			
			url: "contact.php",	
			
			
			type: "GET",

						
			data: data,		
			
			
			cache: false,
			
			
			success: function (html) {				
				//if contact.php returned 1/true (send mail success)
				if (html==1) {
				
					
					$('.done').fadeIn('slow');
					
					$(".form").find('input[type=text], textarea').val("");
					
				
				} else alert('Sorry, unexpected error. Please try again later.');				
			}		
		});
		
		
		return false;
	});	
});	

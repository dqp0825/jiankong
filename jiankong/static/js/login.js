function checkSubmit(username,password,verify_code){    
		// alert(username)
        if(username == ''){
        	
            showErrorMsg('用户名不能为空!');
            return false;
        }
        if(password == ''){
            showErrorMsg('密码不能为空!');
            return false;
        }
        if(verify_code == ''){
            showErrorMsg('验证码不能为空!');
            return false;
        }
        return true
   }
 function showErrorMsg(msg){
        alert(msg)
    }
$(function(){
	$('#btn_login').on('click',function(){
		var username = $.trim($('#username').val());
        var password = $.trim($('#password').val());
        var csrf = $('input').val();
        // alert(csrf)
		if(!checkSubmit(username,password)){
			return;
		}
		$.ajax({
			type:"post",
			url:"/login/",
			async:true,
			data:{
				'username':username,
				'password':password,
                'csrfmiddlewaretoken':csrf,
			},
			success:function(res){
			    // alert(res.errcode)
				if(res.errcode == 1){
                    window.location.href = res.url;
                }else{
                    showErrorMsg(res.msg);
                    verify();
                }
			},
            // error:function(XMLHttpRequest, textStatus, errorThrown) {
            //     showErrorMsg('网络失败，请刷新页面后重试');
            // }
		});
	})
})

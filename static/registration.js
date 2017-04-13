
$('#usertype').on('change',function(){
        if($(this).val()==="cityofficial"){
        $("#otherparams").hide();
        }
        else{
        $("#otherparams").show();
        }
});

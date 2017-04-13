$('#usertype').on('change',function(){
        if( $(this).val()==="City Scientist"){
        $("#city").show();
        $("#state").show();
        $("#title").show();
        }
        else{
        $("#city").hide();
        $("#state").hide();
        $("#title").hide();
        }
});
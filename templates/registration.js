<script type="text/javascript"
    src="jquery-ui-1.10.0/tests/jquery-1.9.0.js"></script>
<script src="jquery-ui-1.10.0/ui/jquery-ui.js"></script>
<script>
$('#usertype').on('change',function(){
        if( $(this).val()==="cityscientist"){
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
</script>
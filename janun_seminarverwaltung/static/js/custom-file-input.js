$('.custom-file-input').on('change',function(){
  var fileName = $(this).val().replace(/C:\\fakepath\\/i, '');
  $(this).next('.custom-file-label').addClass("selected").html(fileName);
})

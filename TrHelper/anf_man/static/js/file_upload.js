$(function () {
  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-file").click(function () {
    article_pk = $(this).attr("article_pk");
    console.log(article_pk)
    $("#fileupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#fileupload").fileupload({
    dataType: 'json',
    done: function (data) {
      console.log(data)  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      $('.download_result#' + article_pk).html('Загружено! '+ data['content']);
    }
  });

});

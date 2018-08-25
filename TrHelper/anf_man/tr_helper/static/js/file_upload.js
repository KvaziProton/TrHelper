// var article_pk;
//
// $(function () {
//   /* 1. OPEN THE FILE EXPLORER WINDOW */
//   $(".js-upload-file").click(function () {
//
//     article_pk = $(this).attr("article_pk");
//     $("#fileupload").click();
//   });
//
//   /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
//   $("#fileupload").fileupload({
//     dataType: 'json',
//     done: function (e, data) {
//       console.log(data.result)
//       $('#' + article_pk).html(data.result.content);
//     }
//   });
//
// });

$('#take').click(function(){
  var article_pk;
  article_pk = $(this).attr("article_pk");
  $.ajax({
        url: '/ajax/button_actions/',
        data: {
          'article_pk': article_pk,
          'take': 'action',
        },
        dataType: 'json',
        success: function (data) {
          if (data.translator == user) {
            console.log("you take");
          };
        }
      });
});

// setInterval(function() {
//     $.ajax({
//         type: "GET",
//         url: {% url 'article_flow' %},
//     })
//     .done(function(response) {
//         $('#flow').prepend(response);
//     });
// }, 10000)

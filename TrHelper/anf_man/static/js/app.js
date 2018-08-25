$('#take').click(function(){
  var article_pk;
  article_pk = $(this).attr("article_pk");

  $.ajax({
        url: 'ajax/button_actions/',
        data: {
          'article_pk': article_pk,
          'take': 'action',
        },
        dataType: 'json',
        success: function (data) {
          pk = String(article_pk);
          console.log(pk);
          $('#' + article_pk).html(data['content']);
        }
      });
});

$('.parse').click(function(){
  console.log('in parse')
  var article_pk;
  article_pk = $(this).attr("article_pk");
  console.log(article_pk)

  $.ajax({
        url: 'ajax/button_actions/',
        data: {
          'article_pk': article_pk,
          'parse': 'action',
        },
        dataType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        // success: function (data) {
        //   pk = String(article_pk);
        //   console.log(pk);
        //   $('#' + article_pk).html(data['content']);
        // }
      });
});


//
// Notification.requestPermission().then(function(result) {
//   console.log(result);
// });
//
// function spawnNotification(body, icon, title) {
//   var options = {
//       body: body,
//       icon: icon
//   };
//   var n = new Notification(title, options);
// }
//
// setInterval(function() {
//     $.ajax({
//         method: "GET",
//         url: '',
//     })
//     .success: (function(data) {
//       success: function (data) {
//         console.log(data['content']);
//         $('body').html(data['content']);
//       }
//       // if data[status]==200:
//       // spawnNotification()
//       // $('#flow').prepend(data['new']);
//     });
// }, 1000)

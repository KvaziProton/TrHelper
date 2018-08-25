$('.take').click(function(){
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
          console.log(data);
          $('#' + article_pk).html(data.content);
        }
      });
});

// $('.parse').click(function(){
//   console.log('in parse')
//   var article_pk;
//   article_pk = $(this).attr("article_pk");
//   console.log(article_pk)
//
//   $.ajax({
//         url: 'ajax/button_actions/',
//         data: {
//           'article_pk': article_pk,
//           'parse': 'action',
//         },
//         dataType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
//         // success: function (data) {
//         //   pk = String(article_pk);
//         //   console.log(pk);
//         //   $('#' + article_pk).html(data['content']);
//         // }
//       });
// });



Notification.requestPermission().then(function(result) {
  console.log(result);
});

function spawnNotification(body) {
  var options = {
      body: body,
      // icon: icon
  };
  var n = new Notification('New article!', options);
}

setInterval(function() {
    $.ajax({
        method: "GET",
        url: '/main/ajax_refresh/',
    // })
      success: function (data) {
        $('#flow').html(data.content);
        console.log(data);
        var body = data.new.title
        spawnNotification(body);
      }
      // if data[status]==200:
      // spawnNotification()
      // $('#flow').prepend(data['new']);
    });
}, 30000)


// console.log(data);
// $('#flow').html(data.content);
// if (data.new==true){
//   var body = data.new.title + data.new.symbols_amount;
//   spawnNotification(body);

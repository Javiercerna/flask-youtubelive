function sendCommand(command)
{
  $.ajax({
    url: '/commands/',
    data: {command:command},
    type: 'POST'
  }).done(function(response) {
    console.log(response);
  });
}

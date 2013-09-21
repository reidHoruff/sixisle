function init_datepicker() {
  var options = {
    'format': 'yyyy-mm-dd',
  };
  
  $('input.datepicker').datepicker(options);
}

function on_dom_manip() {
  init_datepicker();
}

on_dom_manip();

$sniper.registerPostHandleCallback(function() {
  on_dom_manip();
});


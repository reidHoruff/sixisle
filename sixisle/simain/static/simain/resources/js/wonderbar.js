function WonderBar() {
  this.shown = false;
  this.timeout = null;
  /* yea all this timing code is kind of a clusterfuck and technically is flawed but it works */

  this.showMessage = function(html, theme, autohide) {
    if (this.timeout) {
      clearTimeout(this.timeout);
      this.timeout = null;
    }
    var hide_delay = 0;
    var show_delay = autohide;

    if (this.shown) {
      hide_delay = 300;
      this.hide();
    }

    setTimeout(function() {
      $("#wonderbar").attr('class', theme);
      $('#wonderbar-content').html(html);
      $('#wonderbar').slideDown();
      $('#wonderbar-offset').slideDown();
      this.shown = true;

      if (show_delay > 0) {
        this.timeout = setTimeout(function() {
          this.hide();
          return false;
        }.bind(this), show_delay);
      }

      return false;
    }.bind(this),
    hide_delay);
  }

  this.hide = function() {
    $('#wonderbar').slideUp();
    $('#wonderbar-offset').slideUp();
    this.shown = false;
  }
}

function SniperWonderBarHandler() {
  this.ident = '__wonder_bar_show';
  this.handle = function(source, kwargs) {
    var html = kwargs.html;
    var theme = kwargs.theme;
    var autohide = kwargs.autohide;
    $wonder.showMessage(html, theme, autohide);
  }
}

var $wonder = new WonderBar();

function foo() {
  $wonder.showMessage("foobar");
}

$sniper.registerHandler(new SniperWonderBarHandler());

$.ajaxSetup({
  error: function(a, b, c){
    console.log(a, b, c);
    var lines = a.responseText.split("\n"); 
    var found = false;
    var output = "";

    for (var i in lines) {
      if (lines[i].indexOf('Traceback') == 0) { 
        found = true;
      }
      if (found) {
        output += lines[i] + "\n";
      }
      if (output.length > 1000) {
        output += "\n...";
        break;
      }
    }

    if (found) {
      alert(output);
    } else {
      alert("oops, looks like an error occured :(");
    }
  },
});

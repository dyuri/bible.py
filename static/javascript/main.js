
var bible = bible || {};

(function($){
  "use strict";

  bible = {
    appSelector: "[data-component='bible']",
    tmplSelector : "[data-template='true']",
    getQuotes : function(){
      var self = this;

      for(var i=1; i<=6; i++){
      $.ajax({
          url: window.location.origin + window.location.pathname + "?json",
        })
        .done(function(data){
          self.renderQuote(data);
        })
        .fail(function(xhr, status, error){
          console.log("error");
          console.log("status " + status);
          console.log("error " + error);
        });
      }
    },
    renderQuote: function(data){
      $(this.appSelector).append(this.createQuote(data.text, data.bookname, data.chapter, data.line));
    },
    createQuote : function(text, bookname, chapter, line){
      var tmpl = this.quoteTemplate();
      tmpl.find('.text').html(text);
      tmpl.find('.bookname').html(bookname);
      tmpl.find('.chapter').html(chapter);
      tmpl.find('.line').html(line);
      tmpl.attr('id', 'group' + Math.floor(2+(Math.random() * 100)%6));

      return tmpl;
    },
    quoteTemplate : function(){
      return $(this.tmplSelector).children().clone(false);
    }  
  };

  $(function(){
    bible.getQuotes.bind(bible)();
  });
  
})(jQuery);

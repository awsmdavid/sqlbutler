$(document).ready(function() {

//TODO: create toggle function to avoid this horrible crap

  //gender input selector using images
  $('.gender_icon').click(function(){
    var $this = $(this);
    var $gender_icon_class = $('.gender_icon');
    var $this_id = $this.attr('value');

    // alert($this.attr('value'));
    if ($(this).hasClass('off')){
     $this.removeClass('off');
     $this.addClass('on');
     $gender_icon_class.not("#"+$this.attr("id")).removeClass('on').addClass('off');
    }
    //first time any option is selected (nothing has a class)
    else {
     $gender_icon_class.not("#"+$this.attr("id")).addClass('off');
     $this.addClass('on');
    }
    //set value of gender input
    $('#gender_input').val($this.attr('value'));
  });

  //age input selector using images
  $('.age_icon').click(function(){
    var $this = $(this);
    var $age_icon_class = $('.age_icon');
    //if another input is already selected
    if ($(this).hasClass('off')){
     $this.removeClass('off');
     $this.addClass('on');
     $age_icon_class.not("#"+$this.attr("id")).removeClass('on').addClass('off');
    }
    //first time any option is selected (nothing has a class)
    else {
     $age_icon_class.not("#"+$this.attr("id")).addClass('off');
     $this.addClass('on');
    }
    $('#age_input').val($this.attr('value'));
  });

  //price input selector using images
  $('.price_icon').click(function(){
    var $this = $(this);
    var $age_icon_class = $('.price_icon');
    var aSource = $this.data('src');
    var bSource = $this.data('alt-src');
    //if another input is already selected
    if ($(this).hasClass('off')){
      $this.removeClass('off');
      $this.addClass('on');
      $age_icon_class.not("#"+$this.attr("id")).removeClass('on').addClass('off');
    }
    //first time any option is selected (nothing has a class)
    else {
    $age_icon_class.not("#"+$this.attr("id")).addClass('off').attr('src');
      $this.addClass('on');
    }
    $('#price_input').val($this.attr('value'));
  });

  //gift category input selector using images
  $('.category_icon').click(function(){
    var $this = $(this);
    var $category_icon_class = $('.category_icon');
    if ($(this).hasClass('off')) {
      $this.removeClass('off');
      $this.addClass('on');
      $("#"+$this.attr('id')+'_input').val("True");
    }else if ($(this).hasClass('on'))  {
      $(this).removeClass('on').addClass('off');
      $("#"+$this.attr('id')+'_input').val("");
    }
    else {
      $category_icon_class.not("#"+$this.attr("id")).removeClass('on').addClass('off');
      $(this).addClass('on');
      $("#"+$this.attr('id')+'_input').val("True");
    }
  });

  var sourceSwap = function () {
      var $this = $(this);
      var newSource = $this.data('alt-src');
      $this.data('alt-src', $this.attr('src'));
      $this.attr('src', newSource);
  };

  //swap category button images
  $(function() {
      $('img[data-alt-src]').each(function() {
          new Image().src = $(this).data('alt-src');
      }).hover(sourceSwap, sourceSwap);
  });

  //swap input button images
  $(function() {
    $('input[data-alt-src]').each(function() {
        new Image().src = $(this).data('alt-src');
    }).hover(sourceSwap, sourceSwap);
  });

  $('.product_link').click(function(){
    // alert("yo");
    // location.href = '/upvote/{{gift_idea_result.slug}}';
    return false;
  });

  //upvotes
  // $("a.upvote").click(function(){
  //   var curr_elem = $(this) ;
  //   $.get($(this).attr('href'), function(data){
  //       var likecount_div = $(curr_elem).parent().find(".updated-upvote");
  //       likecount_div.text(likecount_div.text()*1+1);
  //   });
  //   $(curr_elem).parent().find(".upvote").hide();
  //   $(curr_elem).parent().find(".upvoted").show();
  //   $(curr_elem).parent().attr('class', 'upvoted-container');
  //   return false;
  // });
});
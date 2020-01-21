/*Check to see if jquery script is loaded 
$(document).ready(function() {
	alert("js is working");
}); 
*/  
/* https://stackoverflow.com/questions/20060467/add-active-navigation-class-based-on-url  */
$(document).ready(function() {

    var CurrentUrl= document.URL;
    console.log(CurrentUrl,"CurrentUrl");
    var CurrentUrlEnd = CurrentUrl.split('/').filter(Boolean).pop();
    console.log(CurrentUrlEnd,"CurrentUrlEnd");
    $( "#navbarMenu ul li a" ).each(function() {
          var ThisUrl = $(this).attr('href');
          var ThisUrlEnd = ThisUrl.split('/').filter(Boolean).pop();
          console.log (ThisUrlEnd, "ThisUrlEnd")
          console.log (CurrentUrlEnd,"CurrentUrlEnd")
          if(ThisUrlEnd == CurrentUrlEnd){
          $(this).closest('li').addClass('active')
          }
    });

});


/* Get current path, find same in href of nav-links and add class (doesn't work, parent?) 
$(document).ready(function() {
	// get current URL path and assign 'active' class
    var pathname = window.location.pathname;
    console.log(pathname);
	$('.navbarMenu > ul > li > a[href="'+pathname+'"]').addClass('active');
})
*/

/* This (w/o the e.preventDefault();) changes the active tab highlight, changes the page, but then the highlight reverts to the original link  
$(document).ready(function () {
    $('.navbar-custom .nav-item .nav-link').click(function(e) {
        alert("click 0"); 
        var myVar = $(this);

        console.log(myVar,"Link was clicked");
        $('.navbar-custom .nav-item .nav-link').removeClass('active');
        $(this).addClass('active');
        console.log(e,"event");
    });
})
*/


/*  Attempt to set active when page loads; did not work
$(function(){
    var current = location.pathname;
    console.log(current);
    $('.navbar-custom .nav-item .nav-link ').each(function(){
        var $this = $(this);
        console.log($this.attr('href').indexOf(current));
        // if the current path is like this link, make it active
        if($this.attr('href').indexOf(current) !== -1){
            $this.parent().addClass('active');  
        }  
    })
})
 */

/* This changes the active tab highlight but does not change the page 
$(document).ready(function () {
    $('.navbar-custom .nav-item .nav-link').click(function(e) {
        alert("click 0");
        $('.navbar-custom .nav-item .nav-link').removeClass('active');
        $(this).addClass('active');
    
        e.preventDefault();
    });
})
*/
/* This ...........................changes the active tab highlight but does not change the page 
$(document).ready(function () {
    $('.navbar-custom .nav-item .nav-link').click(function(e) {
        alert("click 0");
        $('.navbar-custom .nav-item .nav-link').removeClass('active')
        var $this = $(this);
        if (!$this.hasClass('active')) {
            $this.addClass('active');
        }
        e.preventDefault();
    });
})
*/
/* This changes the active tab highlight, changes the page, then highlight returns to the original link 
$(document).ready(function () {
    $('.navbar-custom .nav-item .nav-link').click(function(e) {
        alert("click 0");
        $('.navbar-custom .nav-item .nav-link').removeClass('active')
        var $this = $(this);
        if (!$this.hasClass('active')) {
            $this.addClass('active');
        }
        $('#content').load($(this).find(a).attr('href'));
        
    });
})
*/



/* 
$(function(){
    $('.navbarMenu .navbar-nav .nav-item .nav-link').on("click",function(e){
        alert("Link clicked 1")
        $('.navbar-custom .nat-item .nav-link').removeClass('active');
        $(this).addClass('active');
        }
        e.preventDefault();
    });


/*  -------------------------------------------
$(document).ready((function(){
    $('.navbar-custom .nav-item .nav-link').on("click",function(e){
        alert("link clicked 2");
        $('.navbar-custom .nav-item .nav-link').removeClass('active');
        alert("link clicked 3");
        var $this = $(this);
        if (!$this.hawClass('active')) {
            $this.addClass('active');
        }
        e.preventDefault();
    });
})
*/
/*
$(function(){
    var current = location.pathname;
    $('#nav li a').each(function(){
        var $this = $(this);
        // if the current path is like this link, make it active
        if($this.attr('href').indexOf(current) !== -1){
            $this.addClass('active');
        }
        e.preventDefault();
    })
})
*/

/* $(document).ready(function(){
    $("p").bind("click", function(){
       alert("Click 2 occurred.")
    });
});
*/


/*
jquery(document).ready(function() {
    $("nav-link").on("click",function(){
        alert("nav-link clicked 3");
        $(".nav-link").find(".active").removeClass("active");
        $(this).addClass("active");
    });
})
*/
/*
$(document).ready(function() {
    $('div ul li a').on("click", function() {
        alert(" a link clicked 4");
        $('a.active').removeClass('active');
        $(this).addClass('active');
    });
});
*/

/*
$(document).ready(function(){
    $('.nav li').click(function(event){
        alert("link clicked 5");
        //remove all pre-existing active classes
        $('.active').removeClass('active');

        //add the active class to the link we clicked
        $(this).addClass('active');

        //Load the content
        //e.g.
        //load the page that the link was pointing to
        //$('#content').load($(this).find(a).attr('href'));      

        event.preventDefault();
    });
});
*/

/*
$(document).ready(function(){
    $("a").on("click", function(){
        alert("The paragraph was clicked 6.");
    });
});

$(document).ready(function(){
    $(".nav .nav-link").on("click", function(){
        alert("click 7");
        $(".nav").find(".active").removeClass("active");
        $(this).addClass("active");
    });
});
*/
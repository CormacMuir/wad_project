//put any jscript you want for project in here, i've loaded this file in base.html already - Cormac

//show second image on hover over
var sourceSwap = function () {
    var $this = $(this);
    var newSource = $this.data('alt-src');
    $this.data('alt-src', $this.attr('src'));
    $this.attr('src', newSource);

}
$(function () {
    $('img.card-img-top').hover(sourceSwap, sourceSwap);
});


// dropdown menus scripts
$(".checkbox-menu").on("change", "input[type='radio']", function() {
    $(this).closest("li").toggleClass("active", this.checked);
 });
 
 $(document).on('click', '.allow-focus', function (e) {
   e.stopPropagation();
 });


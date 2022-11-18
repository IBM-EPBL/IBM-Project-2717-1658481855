$(function(){
      
      var $container = $('#portofolio');

      $container.isotope({
        itemSelector : '.category'
      });
      
      
      var $optionSets = $('#options .option-set'),
          $optionLinks = $optionSets.find('a');

      $optionLinks.click(function(){
        var $this = $(this);
        
        if ( $this.hasClass('selected') ) {
          return false;
        }
        var $optionSet = $this.parents('.option-set');
        $optionSet.find('.selected').removeClass('selected');
        $this.addClass('selected');
  
       
        var options = {},
            key = $optionSet.attr('data-option-key'),
            value = $this.attr('data-option-value');
        
        value = value === 'false' ? false : value;
        options[ key ] = value;
        if ( key === 'layoutMode' && typeof changeLayoutMode === 'function' ) {
         
          changeLayoutMode( $this, options )
        } else {
          
          $container.isotope( options );
        }
        
        return false;
      });

      
    });



$(document).ready(function () {
    try {       
        $("a[data-gal^='prettyPhoto']").prettyPhoto({ animation_speed: 'normal', theme: 'dark_rounded', slideshow: 3000, autoplay_slideshow: false, social_tools: false });
    }
    catch (e)
    { }

    try {
        $('.portfolio_showcase').cycle({
            fx: 'fade',
            speed: 'slow',
            timeout: 4000,
            pager: '#number',
            pause: 1
        });
     }
    catch (e)
    { }

});

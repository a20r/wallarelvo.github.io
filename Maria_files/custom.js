var theme = function () {
    function handlePreventEmptyReferences() {
        $('a[href=#]').click(function (event) {
            event.preventDefault();
        });
    }

    function handleHoverClass() {
        var hover = $('.thumbnail');
        hover.hover(    
            function () {
                $(this).addClass('hover');          
            },
            function () {
                $(this).removeClass('hover');                 
            }
        );
    }

    return {
        init: function () {
            handlePreventEmptyReferences();
            handleHoverClass();
        },
        initIsotope: function () {
            $(window).resize(function () {
                // relayout on window resize
                $('.projects .items').isotope('reLayout');
            });
            $(window).load(function () {
                // cache container
                var $container = $('.projects .items');
                // initialize isotope
                $container.isotope({
                    // options...
                    itemSelector: '.item'
                });
                // filter items when filter link is clicked
                $('#filtrable a').click(function () {
                    var selector = $(this).attr('data-filter');
                    $("#filtrable li").removeClass("current");
                    $(this).parent().addClass("current");
                    $container.isotope({ filter: selector });
                    return false;
                });
                $container.isotope('reLayout');
            });
        },
        initParallax: function() {
            $(window).stellar();
        },
        initAnimation: function () {
            var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
            if (isMobile == false) {
                $('*[data-animation]').addClass('animated');
                $('.animated').waypoint(function (down) {
                    var elem = $(this);
                    var animation = elem.data('animation');
                    if (!elem.hasClass('visible')) {
                        var animationDelay = elem.data('animation-delay');
                        if (animationDelay) {
                            setTimeout(function () {
                                elem.addClass(animation + " visible");
                            }, animationDelay);
                        } else {
                            elem.addClass(animation + " visible");
                        }
                    }
                }, {
                    offset: $.waypoints('viewportHeight')
                });
            }
        },
    };
}();



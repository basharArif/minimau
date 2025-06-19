(function($) {
    "use strict";
    /*--
        Commons Variables
    -----------------------------------*/
    var windows = $(window);

    /*--
        Side Header Open & Close Functions
    ----------------------------------------------------------*/
    var sideHeader = $('.side-header');
    var sideHeaderToggle = $('.side-header-toggle');
    var sideHeaderClose = $('.side-header-close');
    var sideHeaderOverlay = $('.side-menu-overlay');

    // Side Header Toggle
    sideHeaderToggle.on('click', function() {
        if ($(this).hasClass('toggle-close')) {
            $(this).removeClass('toggle-close').css('width', '30px');
            sideHeader.removeClass('side-menu-open');
            sideHeaderOverlay.removeClass('overlay-show');
        } else {
            $(this).addClass('toggle-close').css('width', '22px');
            sideHeader.addClass('side-menu-open');
            sideHeaderOverlay.addClass('overlay-show');
        }
    });

    // Side Header Overlay
    sideHeaderOverlay.on('click', function() {
        if (sideHeaderToggle.hasClass('toggle-close')) {
            sideHeaderToggle.removeClass('toggle-close').css('width', '30px');
            sideHeader.removeClass('side-menu-open');
            sideHeaderOverlay.removeClass('overlay-show');
        } else {
            sideHeaderToggle.addClass('toggle-close').css('width', '22px');
            sideHeader.addClass('side-menu-open');
            sideHeaderOverlay.addClass('overlay-show');
        }
    });

    // Side Header Close
    sideHeaderClose.on('click', function() {
        if (sideHeaderToggle.hasClass('toggle-close')) {
            sideHeaderToggle.removeClass('toggle-close').css('width', '30px');
            sideHeader.removeClass('side-menu-open');
            sideHeaderOverlay.removeClass('overlay-show');
        } else {
            sideHeaderToggle.addClass('toggle-close').css('width', '22px');
            sideHeader.addClass('side-menu-open');
            sideHeaderOverlay.addClass('overlay-show');
        }
    });

    /*--
        Side Submenu
    ----------------------------------------------------------*/
    $('.side-menu .menu-item-has-children > a').prepend('<i class="expand menu-expand fa fa-angle-down"></i>');
    $('.side-menu .menu-item-has-children ul').slideUp();

    $('.side-menu').on('click', 'li a, li a .menu-expand', function(e) {
        var $a = $(this).hasClass('menu-expand') ? $(this).parent() : $(this);
        if ($a.parent().hasClass('menu-item-has-children')) {
            if ($a.attr('href') === '#' || $(this).hasClass('menu-expand')) {
                if ($a.siblings('ul:visible').length > 0) {
                    $a.find('.menu-expand').removeClass('fa-angle-up').addClass('fa-angle-down');
                    $a.siblings('ul').slideUp();
                } else {
                    $(this).parents('li').siblings('li').find('.menu-expand').removeClass('fa-angle-up').addClass('fa-angle-down');
                    $(this).parents('li').siblings('li').find('ul:visible').slideUp();
                    $a.find('.menu-expand').removeClass('fa-angle-down').addClass('fa-angle-up');
                    $a.siblings('ul').slideDown();
                }
            }
        }
        if ($(this).hasClass('menu-expand') || $a.attr('href') === '#') {
            e.preventDefault();
            return false;
        }
    });

    /*--
        Full Page
    ----------------------------------------------------------*/
    $('#fullpage').fullpage({
        menu: '.fullpage-menu',
        lockAnchors: false,
        anchors: ['home', 'about', 'service', 'portfolio', 'blog', 'contact'],
        scrollOverflow: true,
        navigation: true,
        verticalCentered: false,
        navigationTooltips: ['Home', 'About', 'Service', 'Portfolio', 'Blog', 'Contact'],
        responsiveWidth: 991,
    });

    // FullPage Navigation Position
    function fpNavPosition() {
        var sideHeaderWidth = $('.side-header').outerWidth();
        var screenSize = windows.width() - sideHeaderWidth;
        var containerSize = $('.container').outerWidth();
        $('#fp-nav.left').css('left', ((screenSize - containerSize) / 4));
        $('#fp-nav.right').css('right', ((screenSize - containerSize) / 4));
    }
    // FullPage Navigation On Mobile
    function fpNavCloseOnClickMobile() {
        if (windows.width() < 992) {
            $('.fullpage-menu').on('click', 'li a', function(e) {
                $('.side-header-toggle').removeClass('toggle-close');
                $('.side-menu-overlay').removeClass('overlay-show');
                $('.side-header').removeClass('side-menu-open');
            });
        }
    }
    fpNavPosition();
    fpNavCloseOnClickMobile();
    windows.resize(function() {
        fpNavPosition();
        fpNavCloseOnClickMobile();
    });

    /*--
        Home Portfolio Slider
    ----------------------------------------------------------*/
    $('.portfolio-slider-5').slick({
        arrows: true,
        autoplay: false,
        autoplaySpeed: 5000,
        dots: false,
        pauseOnFocus: false,
        pauseOnHover: false,
        infinite: true,
        slidesToShow: 5,
        prevArrow: '<button type="button" class="slick-prev">prev</button>',
        nextArrow: '<button type="button" class="slick-next">next</button>',
        appendArrows: '.portfolio-slider-5-nav',
        responsive: [{
                breakpoint: 1200,
                settings: {
                    slidesToShow: 4,
                }
            },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 3,
                    autoplay: true,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2,
                    autoplay: true,
                }
            },
            {
                breakpoint: 576,
                settings: {
                    slidesToShow: 1,
                    autoplay: true,
                }
            },
        ]
    });


    /*--
        Masonry Portfolio
    ----------------------------------------------------------*/
    var masonryGrid = $('.masonry-grid');
    masonryGrid.imagesLoaded(function() {
        masonryGrid.masonry({
            // options
            itemSelector: '.masonry-grid [class*="col-"]',
        });
    });


    /*--
        Custom Scroll Bar
    ----------------------------------------------------------*/
    $('.custom-scroll').each(function() {
        var ps = new PerfectScrollbar($(this)[0]);
        if (windows.width <= 991) {
            ps.destroy();
        }
    });


    /*! jquery.cookie v1.4.1 | MIT */
    ! function(a) { "function" == typeof define && define.amd ? define(["jquery"], a) : "object" == typeof exports ? a(require("jquery")) : a(jQuery) }(function(a) {
        function b(a) { return h.raw ? a : encodeURIComponent(a) }

        function c(a) { return h.raw ? a : decodeURIComponent(a) }

        function d(a) { return b(h.json ? JSON.stringify(a) : String(a)) }

        function e(a) { 0 === a.indexOf('"') && (a = a.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, "\\")); try { return a = decodeURIComponent(a.replace(g, " ")), h.json ? JSON.parse(a) : a } catch (b) {} }

        function f(b, c) { var d = h.raw ? b : e(b); return a.isFunction(c) ? c(d) : d }
        var g = /\+/g,
            h = a.cookie = function(e, g, i) {
                if (void 0 !== g && !a.isFunction(g)) {
                    if (i = a.extend({}, h.defaults, i), "number" == typeof i.expires) {
                        var j = i.expires,
                            k = i.expires = new Date;
                        k.setTime(+k + 864e5 * j)
                    }
                    return document.cookie = [b(e), "=", d(g), i.expires ? "; expires=" + i.expires.toUTCString() : "", i.path ? "; path=" + i.path : "", i.domain ? "; domain=" + i.domain : "", i.secure ? "; secure" : ""].join("")
                }
                for (var l = e ? void 0 : {}, m = document.cookie ? document.cookie.split("; ") : [], n = 0, o = m.length; o > n; n++) {
                    var p = m[n].split("="),
                        q = c(p.shift()),
                        r = p.join("=");
                    if (e && e === q) { l = f(r, g); break }
                    e || void 0 === (r = f(r)) || (l[q] = r)
                }
                return l
            };
        h.defaults = {}, a.removeCookie = function(b, c) { return void 0 === a.cookie(b) ? !1 : (a.cookie(b, "", a.extend({}, c, { expires: -1 })), !a.cookie(b)) }
    });

    var customizerHtml = '<div class="customizer-wrap"> <button class="customizer-toggle"><i class="fa fa-cog"></i></button><div class="customizer-inner"> <h4>Chose Color</h4><ul class="color-setting"> <li data-color="default" style="background-color: #212121"></li><li data-color="color-var-1" style="background-color: #E65B1C"></li><li data-color="color-var-2" style="background-color: #f15445"></li><li data-color="color-var-3" style="background-color: #51becd"></li><li data-color="color-var-4" style="background-color: #e59701"></li></ul></div></div>'
    $('body').prepend(customizerHtml);

    $('.customizer-toggle').on('click', function() {
        $(this).parents('.customizer-wrap').toggleClass('open');
    })

    jQuery(function($) {
        var color = $.cookie('color');
        var colorList = 'color-var-1 color-var-2 color-var-3 color-var-4 color-var-5 color-var-6 color-var-7 color-var-8';
        $('.color-setting li').on('click', function(e) {
            color = $(this).data('color')
            $('body').removeClass(colorList).addClass(color);
            $.cookie('color', color, {
                expires: 365,
                path: '/'
            });
            return false;
        }).filter(function() {
            return $(this).data('color') === color
        }).click()

        var theme = $.cookie('theme');
        $('.theme-setting li').on('click', function(e) {
            theme = $(this).data('theme')
            $('body').removeClass('light-version dark-version').addClass(theme);
            $.cookie('theme', theme, {
                expires: 365,
                path: '/'
            });
            return false;
        }).filter(function() {
            return $(this).data('theme') === theme
        }).click()
    });


})(jQuery);
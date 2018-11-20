'use strict';

/*
 * Redisgn Pluton's template from http://graphberry.com by Kineev Alexey
 * Author: Kineev Alaxey
 * Author URL: https://www.facebook.com/alexey.kineev
 */

 jQuery(document).ready(function ($) {

    var lastId,
    topMenu = $("#top-navigation"),
    topMenuHeight = topMenu.outerHeight(),
        // All list items
        menuItems = topMenu.find("a"),
        // Anchors corresponding to menu items
        scrollItems = menuItems.map(function () {
            var href = $(this).attr("href");
            if(href.indexOf("#") === 0){
                var item = $($(this).attr("href"));
                if (item.length) {
                    return item;
                }
            }
        });

    //Get width of container

    var containerWidth = $('.section .container').width();
    //Resize animated triangle
    $(".triangle").css({
        "border-left": containerWidth / 2 + 'px outset transparent',
        "border-right": containerWidth / 2 + 'px outset transparent'
    });
    $(window).resize(function () {
        containerWidth = $('.container').width();
        $(".triangle").css({
            "border-left": containerWidth / 2 + 'px outset transparent',
            "border-right": containerWidth / 2 + 'px outset transparent'
        });
    });


    //Initialize header slider.

    $('#da-slider').cslider();

    //Initial mixitup, used for animated filtering news.
    $('#news-grid').mixitup({
        'onMixStart': function (config) {
            $('div.toggleDiv').hide();
        }
    });
    
    //Initial Out clients slider in client section
    
    function getMaximumSliders() {
        if ($("body").prop("clientWidth") > 600){
            return 3;
        }
        else{
            return 1;
        }
    }
    
    // Set slideWidth
    function getSlideSettings() {
        var winWidth = $( window ).width();
        if(winWidth >= 968 && winWidth <= 1024){
            return {"slideWidth":300, "slideMargin":20, "maxSlides":3};
        }
        else if (winWidth >= 650 && winWidth < 968){
            return {"slideWidth":300, "slideMargin":20, "maxSlides":2};
        }
        else if(winWidth < 650){
            return {"slideWidth":300, "slideMargin":20, "maxSlides":1};
        }
        else {
            return {"slideWidth":370, "slideMargin":25, "maxSlides":3};
        }
        // switch (winWidth) {
        //     case
        //     case 1024:
        //         return {"slideWidth":300, "slideMargin":20, "maxSlides":3};
        //     default:
        //         return {"slideWidth":370, "slideMargin":25, "maxSlides":3};
        // }
    } 
     
    $('#eth-tarifs-slider').bxSlider({
        pager: false,
        minSlides: 1,
        maxSlides: getSlideSettings()["maxSlides"],
        moveSlides: 1,
        slideWidth: getSlideSettings()["slideWidth"],
        slideMargin: getSlideSettings()["slideMargin"],
        prevSelector: $('#eth-tarifs-prev'),
        nextSelector: $('#eth-tarifs-next'),
        prevText: '<i class="icon-left-open"></i>',
        nextText: '<i class="icon-right-open"></i>'
    });

    $('#adsl-tarifs-slider').bxSlider({
        pager: false,
        minSlides: 1,
        maxSlides: getSlideSettings()["maxSlides"],
        moveSlides: 1,
        slideWidth: getSlideSettings()["slideWidth"],
        slideMargin: getSlideSettings()["slideMargin"],
        prevSelector: $('#adsl-tarifs-prev'),
        nextSelector: $('#adsl-tarifs-next'),
        prevText: '<i class="icon-left-open"></i>',
        nextText: '<i class="icon-right-open"></i>'
    });

    $('input, textarea').placeholder();

    // Bind to scroll

    $(window).scroll(function () {

        //Display or hide scroll to top button 
        if ($(this).scrollTop() > 100) {
            $('.scrollup').fadeIn();
        } else {
            $('.scrollup').fadeOut();
        }

        if ($(this).scrollTop() > 130) {
            $('.navbar').addClass('navbar-fixed-top animated fadeInDown');
        } else {
            $('.navbar').removeClass('navbar-fixed-top animated fadeInDown');
        }

        // Get container scroll position
        var fromTop = $(this).scrollTop() + topMenuHeight + 10;

        // Get id of current scroll item
        var cur = scrollItems.map(function () {
            if ($(this).offset().top < fromTop)
                return this;
        });

        // Get the id of the current element
        cur = cur[cur.length - 1];
        var id = cur && cur.length ? cur[0].id : "";

        if (lastId !== id) {
            lastId = id;
            // Set/remove active class
            menuItems
            .parent().removeClass("active")
            .end().filter("[href=#" + id + "]").parent().addClass("active");
        }
    });

    //Function for scrolling to top

    $('.scrollup').click(function () {
        $("html, body").animate({
            scrollTop: 0
        }, 600);
        return false;
    });


    $(window).load(function () {
        function filterPath(string) {
            return string.replace(/^\//, '').replace(/(index|default).[a-zA-Z]{3,4}$/, '').replace(/\/$/, '');
        }
        $('a[href*=#]').each(function () {
            if (filterPath(location.pathname) == filterPath(this.pathname) && location.hostname == this.hostname && this.hash.replace(/#/, '')) {
                var $targetId = $(this.hash),
                $targetAnchor = $('[name=' + this.hash.slice(1) + ']');
                var $target = $targetId.length ? $targetId : $targetAnchor.length ? $targetAnchor : false;

                if ($target) {

                    $(this).click(function () {

                        //Hack collapse top navigation after clicking
                        topMenu.parent().attr('style', 'height:0px').removeClass('in'); //Close navigation
                        $('.navbar .btn-navbar').addClass('collapsed');

                        var targetOffset = $target.offset().top - 63;
                        $('html, body').animate({
                            scrollTop: targetOffset
                        }, 800);
                        return false;
                    });
                }
            }
        });
    });

    // Set activity nav-pills for tariffs navigate

    //Scroll to contact form and set on this form connect tariff option

    $('#eth-tarifs-slider a').click(function () {
        $('#message-category').val('Подключить услугу');
        var tarif = $(this).attr('id');
        $('#comment').text('Добрый день. Прошу Вас подключить мне услугу доступа в сеть Интернет ' +
        'по технологии Ethernet с тарифным планом ' + tarif);
    });

    $('#adsl-tarifs-slider a').click(function () {
        $('#message-category').val('Подключить услугу');
        var tarif = $(this).attr('id');
        $('#comment').text('Добрый день. Прошу Вас подключить мне услугу доступа в сеть Интернет ' +
        'по технологии ADSL с тарифным планом ' + tarif);
    });

    // Set CSRF token

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Phone tariffs keydown filtering and autocomplete input

    $("#ph-duration").keydown(function (e) {
            var error = false;

            // Allow: backspace, delete, tab, escape, enter and .
            if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
                (e.keyCode === 65 && (e.ctrlKey === true || e.metaKey === true)) ||
                (e.keyCode >= 35 && e.keyCode <= 40)) {
                return;
            }

            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                $('#err-ph-data').show(500);
                e.preventDefault();
            }
            else{
                $('#err-ph-data').hide(500);
            }
        }).autocomplete({
        source: "/calls/",
        select: function (event, ui) {
            AutoCompleteSelectHandler(event, ui)
        },
        minLength: 4
    });

    function AutoCompleteSelectHandler(event, ui) {
        var selectedObj = ui.item;
    }

    // Send phone direction form

     $('#ph-submit').click(function () {
        $.ajax({
            type: 'POST',
            url: '/prices/',

            data: {
                direction: $('#ph-duration').val(),
                // csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            error: function (request, error) {
                $('#err-ph-response').show(500).delay(4000);
                $('#err-ph-response').animate({
                    heigth: 'toggle'
                }, 500, function () {
                });
            },
            success: function (response) {
                if (response !== 'BAD') {
                    $('#success-price').empty();
                    var $sprice = $( "#success-price" ),
                        str = response,
                        html = $.parseHTML( str ),
                        nodeNames = [];
                    $sprice.append( html );
                    $('#success-price').show();
                    // $('#success-price').text(response).show();
                } else {
                    alert("Ошибка отправки данных формы на сервер. Получен BAD ответ от сервера.");
                }
            }
        });

        return false;
    });

    //Send subscribe letter

    $('#subscribe').click(function () {
        var error = false;
        var emailCompare = /^([a-z0-9_.-]+)@([0-9a-z.-]+).([a-z.]{2,6})$/; // Syntax to compare against input
        var email = $('input#nlmail').val().toLowerCase(); // get the value of the input field
        if (email === "" || email === " " || !emailCompare.test(email)) {
            $('#err-subscribe').show(500);
            $('#err-subscribe').delay(4000);
            $('#err-subscribe').animate({
                height: 'toggle'
            }, 500, function () {
                // Animation complete.
            });
            error = true; // change the error state to true
        }

        if (error === false) {
            $.ajax({
                type: 'POST',
                url: '/subscribe/',

                data: {
                    email: $('#nlmail').val()
                },
                error: function (request, error) {
                    alert("Неизвесная ошибка.");
                },
                success: function (response) {
                    if (response === 'OK') {
                        $('#success-subscribe').show();
                        // $('#nlmail').val('')
                    } else {
                        alert("Ошибка отправки данных формы на сервер. Получен BAD ответ от сервера.");
                    }
                }
            });
        }

        return false;
    });

    //Contact form

    $("#send-message").click(function () {

        var name = $('input#name').val(); // get the value of the input field
        var error = false;
        if (name === "" || name === " ") {
            $('#err-name').show(500).delay(4000);
            $('#err-name').animate({
                height: 'toggle'
            }, 500, function () {
                // Animation complete.
            });
            error = true; // change the error state to true
        }
        
        var phone = $('input#tel').val(); // get the value of the input field
        if (phone == "" || phone == " ") {
            $('#err-phone').show(500).delay(4000);
            $('#err-phone').animate({
                height: 'toggle'
            }, 500, function () {
                // Animation complete.
            });
            error = true; // change the error state to true
        }


        var comment = $('textarea#comment').val(); // get the value of the input field
        if (comment == "" || comment == " ") {
            $('#err-comment').show(500).delay(4000);
            $('#err-comment').animate({
                height: 'toggle'
            }, 500, function () {
                // Animation complete.
            });
            error = true; // change the error state to true
        }

        if (error == false) {
            var selectedOption = $( "#message-category option:selected" ).val();
            var dataString = $('#contact-form').serialize() + '&category=' + selectedOption;
            $.ajax({
                type: "POST",
                url: '/feedback/',
                data: dataString,
                timeout: 6000,
                error: function (request, error) {

                },
                success: function (response) {
                    if (response == 'OK') {
                        $('#successSend').show();
                        // $("#name").val('');
                        // $("#tel").val('');
                        // $("#comment").val('');
                    } else {
                        $('#errorSend').show();
                    }
                }
            });
            return false;
        }

        return false; // stops user browser being directed to the php file
    });

    //Function for show or hide news description.

    $.fn.showHide = function (options) {
        var defaults = {
            speed: 1000,
            easing: '',
            changeText: 0,
            showText: 'Show',
            hideText: 'Hide'
        };
        var options = $.extend(defaults, options);
        $(this).click(function () {
            $('.toggleDiv').slideUp(options.speed, options.easing);
            var toggleClick = $(this);
            var toggleDiv = $(this).attr('rel');
            $(toggleDiv).slideToggle(options.speed, options.easing, function () {
                if (options.changeText == 1) {
                    $(toggleDiv).is(":visible") ? toggleClick.text(options.hideText) : toggleClick.text(options.showText);
                }
            });
            return false;
        });
    };

    //Initial Show/Hide news element.

    $('div.toggleDiv').hide();
    $('.show_hide').showHide({
        speed: 500,
        changeText: 0,
        showText: 'View',
        hideText: 'Close'
    });

    //Animate thumbnails

    jQuery('.thumbnail').one('inview', function (event, visible) {
        if (visible == true) {
            jQuery(this).addClass("animated fadeInDown");
        } else {
            jQuery(this).removeClass("animated fadeInDown");
        }
    });

    //Animate triangles

    jQuery('.triangle').bind('inview', function (event, visible) {
        if (visible == true) {
            jQuery(this).addClass("animated fadeInDown");
        } else {
            jQuery(this).removeClass("animated fadeInDown");
        }
    });
    
    //animate first team member

    jQuery('#first-person').bind('inview', function (event, visible) {
        if (visible == true) {
            jQuery('#first-person').addClass("animated pulse");
        } else {
            jQuery('#first-person').removeClass("animated pulse");
        }
    });
    
    //animate sectond team member

    jQuery('#second-person').bind('inview', function (event, visible) {
        if (visible == true) {
            jQuery('#second-person').addClass("animated pulse");
        } else {
            jQuery('#second-person').removeClass("animated pulse");
        }
    });

    //animate thrid team member

    jQuery('#third-person').bind('inview', function (event, visible) {
        if (visible == true) {
            jQuery('#third-person').addClass("animated pulse");
        } else {
            jQuery('#third-person').removeClass("animated pulse");
        }
    });
    
    //Animate price columns

    jQuery('.price-column, .testimonial').bind('inview', function (event, visible) {
        if (visible == true) {
            jQuery(this).addClass("animated fadeInDown");
        } else {
            jQuery(this).removeClass("animated fadeInDown");
        }
    });
    
    //Animate contact form

    jQuery('.contact-form').bind('inview', function (event, visible) {
        if (visible == true) {
            jQuery('.contact-form').addClass("animated bounceIn");
        } else {
            jQuery('.contact-form').removeClass("animated bounceIn");
        }
    });

    //Animate skill bars

    jQuery('.skills > li > span').one('inview', function (event, visible) {
        if (visible == true) {
            jQuery(this).each(function () {
                jQuery(this).animate({
                    width: jQuery(this).attr('data-width')
                }, 3000);
            });
        }
    });
});

//Initialize google map for contact setion with your location.

function initializeMap() {

    var lat = '55.663666'; //Set your latitude.
    var lon = '39.868369'; //Set your longitude.

    var centerLon = lon - 0.0065;

    var myOptions = {
        scrollwheel: false,
        draggable: true,
        disableDefaultUI: true,
        center: new google.maps.LatLng(lat, centerLon),
        zoom: 17,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    //Bind map to elemet with id map-canvas

    var map = new google.maps.Map(document.getElementById('map-canvas'), myOptions);
    var marker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(lat, lon),

    });

    var infowindow = new google.maps.InfoWindow({
        content: "'Альтес-Р' ул. Косякова, д. 13 (2-й этаж)"
    });

    google.maps.event.addListener(marker, 'click', function () {
        infowindow.open(map, marker);
    });

    infowindow.open(map, marker);
}
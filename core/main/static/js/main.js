$(document).ready(function() {
    "use strict";

    $('.menu-toggle > a').on('click', function (e) {
        e.preventDefault();
        $('#responsive-nav').toggleClass('active');
    });

    $('.cart-dropdown').on('click', function (e) {
        e.stopPropagation();
    });

$(document).ready(function() {
    $('.tab-nav a').click(function(e) {
        e.preventDefault();
        $(this).tab('show');
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const leftSlider = document.querySelector('.left-slider .slider');
    const rightSlider = document.querySelector('.right-slider .slider');

    let leftIndex = 0;
    let rightIndex = 0;

    function slideLeft() {
        leftIndex = (leftIndex + 1) % leftSlider.children.length;
        leftSlider.style.transform = `translateX(-${leftIndex * 100}%)`;
    }

    function slideRight() {
        rightIndex = (rightIndex + 1) % rightSlider.children.length;
        rightSlider.style.transform = `translateX(-${rightIndex * 100}%)`;
    }

    setInterval(slideLeft, 3000); 
    setInterval(slideRight, 3000); 
});




    $('.products-slick').each(function() {
        var $this = $(this),
                $nav = $this.attr('data-nav');

        $this.slick({
            slidesToShow: 4,
            slidesToScroll: 1,
            autoplay: true,
            infinite: true,
            speed: 300,
            dots: false,
            arrows: true,
            appendArrows: $nav ? $nav : false,
            responsive: [{
                breakpoint: 991,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                }
            },
            ]
        });
    });

    $('.products-widget-slick').each(function() {
        var $this = $(this),
                $nav = $this.attr('data-nav');

        $this.slick({
            infinite: true,
            autoplay: true,
            speed: 300,
            dots: false,
            arrows: true,
            appendArrows: $nav ? $nav : false,
        });
    });

    $('#product-main-img').slick({
        infinite: true,
        speed: 300,
        dots: false,
        arrows: true,
        fade: true,
        asNavFor: '#product-imgs',
    });

    $('#product-imgs').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        arrows: true,
        centerMode: true,
        focusOnSelect: true,
        centerPadding: 0,
        vertical: true,
        asNavFor: '#product-main-img',
        responsive: [{
            breakpoint: 991,
            settings: {
                vertical: false,
                arrows: false,
                dots: true,
            }
        },
        ]
    });

    var zoomMainProduct = document.getElementById('product-main-img');
    if (zoomMainProduct) {
        $('#product-main-img .product-preview').zoom();
    }

    $('.thumb-image').on('mouseover', function() {
        var imgSrc = $(this).attr('src');
        $('#product-main-img img').attr('src', imgSrc);
    });

    $('.input-number').each(function() {
        var $this = $(this),
        $input = $this.find('input[type="number"]'),
        up = $this.find('.qty-up'),
        down = $this.find('.qty-down');

        down.on('click', function () {
            var value = parseInt($input.val()) - 1;
            value = value < 1 ? 1 : value;
            $input.val(value);
            $input.change();
            updatePriceSlider($this , value);
        });

        up.on('click', function () {
            var value = parseInt($input.val()) + 1;
            $input.val(value);
            $input.change();
            updatePriceSlider($this , value);
        });
    });

    var priceInputMax = document.getElementById('price-max'),
            priceInputMin = document.getElementById('price-min');

    priceInputMax.addEventListener('change', function(){
        updatePriceSlider($(this).parent() , this.value);
    });

    priceInputMin.addEventListener('change', function(){
        updatePriceSlider($(this).parent() , this.value);
    });

    function updatePriceSlider(elem , value) {
        if ( elem.hasClass('price-min') ) {
            priceSlider.noUiSlider.set([value, null]);
        } else if ( elem.hasClass('price-max')) {
            priceSlider.noUiSlider.set([null, value]);
        }
    }

    // Price Slider
    var priceSlider = document.getElementById('price-slider');
    if (priceSlider) {
        noUiSlider.create(priceSlider, {
            start: [1, 999],
            connect: true,
            step: 1,
            range: {
                'min': 1,
                'max': 999
            }
        });

        priceSlider.noUiSlider.on('update', function( values, handle ) {
            var value = values[handle];
            handle ? priceInputMax.value = value : priceInputMin.value = value;
        });
    }

});


const getCookie = (name) => {
    const value = " " + document.cookie;
    console.log("value", `==${value}==`);
    const parts = value.split(" " + name + "=");
    return parts.length < 2 ? undefined : parts.pop().split(";").shift();
  };
  
  const setCookie = function (name, value, expiryDays, domain, path, secure) {
    const exdate = new Date();
    exdate.setHours(
      exdate.getHours() +
        (typeof expiryDays !== "number" ? 365 : expiryDays) * 24
    );
    document.cookie =
      name +
      "=" +
      value +
      ";expires=" +
      exdate.toUTCString() +
      ";path=" +
      (path || "/") +
      (domain ? ";domain=" + domain : "") +
      (secure ? ";secure" : "");
  };



  function acceptCookies() {
    document.querySelector('.cookies-eu-banner').style.display = 'none';
}

function denyCookies() {
    alert('You have denied all cookies. Some features may not work properly.');
}



document.addEventListener("DOMContentLoaded", function() {
    const banner = document.querySelector('.cookies-eu-banner');
    const acceptBtn = document.querySelector('.accept-btn');

    if (acceptBtn && banner) {
        acceptBtn.addEventListener('click', function() {
            banner.style.display = 'none'; 
        });
    }
});




document.addEventListener('DOMContentLoaded', function() {
    const productSlider = document.getElementById('slick-new-products-horizontal');
    const products = productSlider.querySelectorAll('.product-item');
    const totalProducts = products.length;
    let currentIndex = 0;
    const intervalTime = 3000;

    const clones = [];
    const cloneCount = Math.min(3, totalProducts); 
    
    for (let i = 0; i < cloneCount; i++) {
        clones.push(products[i].cloneNode(true));
        clones.unshift(products[totalProducts - 1 - i].cloneNode(true)); 
    }

    clones.forEach(clone => productSlider.appendChild(clone)); 

    const updatedProducts = productSlider.querySelectorAll('.product-item');
    const totalSlides = updatedProducts.length;

    const itemWidth = updatedProducts[0].offsetWidth + 10; // Adjust margin if necessary
    productSlider.style.width = itemWidth * totalSlides + 'px';

    function showNextProduct() {
        currentIndex++;

        const translateValue = -1 * currentIndex * itemWidth;

        productSlider.style.transform = `translateX(${translateValue}px)`;

        if (currentIndex >= totalSlides - (2 * cloneCount)) {
            setTimeout(() => {
                currentIndex = cloneCount - 1;
                productSlider.style.transition = 'none';
                productSlider.style.transform = `translateX(${-1 * currentIndex * itemWidth}px)`;
            }, 400);
        }

        setTimeout(() => {
            productSlider.style.transition = 'transform 0.4s ease-in-out';
        }, 500);
    }

    setInterval(showNextProduct, intervalTime);
});



$(document).ready(function(){
    $('.category-slider .products-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: true,
        dots: false,
        infinite: true,
        autoplay: true,
        autoplaySpeed: 3000 
    });
});


$(document).ready(function() {
    $('.color-swatch').each(function() {
        var color = $(this).data('color');
        if (color) {
            $(this).css('background-color', color);
        }
    });

    function filterProducts() {
        var selectedCategories = [];
        var selectedBrands = $('#brandFilter').val();
        var minPrice = parseFloat($('#minPrice').val()) || 0;
        var maxPrice = parseFloat($('#maxPrice').val()) || Infinity;
        var productName = $('#productName').val().toLowerCase();
        var selectedColors = [];

        $('.color-swatch.selected').each(function() {
            selectedColors.push($(this).data('color'));
        });

        $('.category-filter:checked').each(function() {
            selectedCategories.push($(this).val());
        });

        $('#productList .product-item').each(function() {
            var category = $(this).data('category');
            var price = parseFloat($(this).data('price'));
            var brand = $(this).data('brand');
            var color = $(this).data('color');
            var productNameInItem = $(this).find('.product-name a').text().toLowerCase();

            var categoryMatch = selectedCategories.length === 0 || selectedCategories.includes(category.toString());
            var priceMatch = price >= minPrice && price <= maxPrice;
            var brandMatch = !selectedBrands || selectedBrands === brand;
            var productNameMatch = productName === '' || productNameInItem.includes(productName);
            var colorMatch = selectedColors.length === 0 || selectedColors.includes(color);

            if (categoryMatch && priceMatch && brandMatch && productNameMatch && colorMatch) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }

    $('#price-filter-form, #product-name-filter-form').on('change keyup submit', function(e) {
        e.preventDefault();
        filterProducts();
    });

    $('#brandFilter').on('change', function() {
        filterProducts();
    });

    $('#clearPriceFilter').on('click', function() {
        $('#minPrice').val('');
        $('#maxPrice').val('');
        filterProducts();
    });

    $('#clearBrandFilter').on('click', function() {
        $('#brandFilter').val('');
        filterProducts();
    });

    $('#clearProductNameFilter').on('click', function() {
        $('#productName').val('');
        filterProducts();
    });

    $('.color-swatch').on('click', function(e) {
        e.preventDefault();
        $(this).toggleClass('selected');
        filterProducts(); 
    });

    $('#clearColorFilter').on('click', function() {
        $('.color-swatch').removeClass('selected');

        filterProducts();
    });

    filterProducts();
});


$(document).ready(function() {
    var $thumbsWrapper = $('.thumbs-wrapper');
    var $thumbsContainer = $('.thumbs-container');
    var $thumbs = $('.product-preview');
    var thumbHeight = $thumbs.first().outerHeight(true); 
    var visibleCount = 3;
    var containerHeight = thumbHeight * visibleCount; 
    var maxScrollTop = thumbHeight * ($thumbs.length - visibleCount); 

    $('.scroll-btn.up-btn').on('click', function() {
        var currentScrollTop = $thumbsContainer.scrollTop();
        var newScrollTop = Math.max(currentScrollTop - containerHeight, 0); 
        $thumbsContainer.animate({ scrollTop: newScrollTop }, 300);
    });

    $('.scroll-btn.down-btn').on('click', function() {
        var currentScrollTop = $thumbsContainer.scrollTop();
        var newScrollTop = Math.min(currentScrollTop + containerHeight, maxScrollTop); // Move down
        $thumbsContainer.animate({ scrollTop: newScrollTop }, 300);
    });

    $('#product-imgs').on('click', '.thumb-image', function() {
        var newImageUrl = $(this).data('main-image');
        $('#main-image').attr('src', newImageUrl);
    });
});
$(document).ready(function() {
    var $thumbsWrapper = $('#product-thumbnails .thumbs-wrapper');
    var $thumbsContainer = $('#product-thumbnails .thumbs-container');
    var $thumbs = $('#product-thumbnails .product-preview');
    var thumbHeight = $thumbs.first().outerHeight(true); 
    var visibleCount = 3; 
    var containerHeight = thumbHeight * visibleCount;
    var maxScrollTop = thumbHeight * ($thumbs.length - visibleCount); 

    
    $('#product-thumbnails .scroll-btn.up-btn').on('click', function() {
        var currentScrollTop = $thumbsContainer.scrollTop();
        var newScrollTop = Math.max(currentScrollTop - containerHeight, 0); 
        $thumbsContainer.animate({ scrollTop: newScrollTop }, 300);
    });

    $('#product-thumbnails .scroll-btn.down-btn').on('click', function() {
        var currentScrollTop = $thumbsContainer.scrollTop();
        var newScrollTop = Math.min(currentScrollTop + containerHeight, maxScrollTop); // Move down
        $thumbsContainer.animate({ scrollTop: newScrollTop }, 300);
    });

    $('#product-thumbnails').on('click', '.thumb-image', function() {
        var newImageUrl = $(this).data('main-image');
        $('#main-image').attr('src', newImageUrl);
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var collapseElements = document.querySelectorAll('[data-bs-toggle="collapse"]');
    collapseElements.forEach(function (element) {
        new bootstrap.Collapse(element, {
            toggle: false
        });
    });
    
    document.querySelector('.btn-primary.payment').addEventListener('click', function () {
        alert('Payment button clicked');
    });
});

$(document).ready(function() {
    $('.thumb-image').click(function() {
        var newSrc = $(this).data('main-image');
        $('#main-image').attr('src', newSrc);
    });

    let thumbIndex = 0;
    const thumbImages = $('#product-imgs .product-preview');
    const totalThumbs = thumbImages.length;
    const thumbHeight = thumbImages.first().outerHeight(true); 

    function showThumbnails() {
        $('#product-imgs .thumbs-wrapper').css('transform', `translateY(-${thumbIndex * thumbHeight}px)`);
    }

    function slideThumbnails() {
        thumbIndex = (thumbIndex + 1) % totalThumbs;
        showThumbnails();
    }

    showThumbnails();
    setInterval(slideThumbnails, 3000); 

    $('.scroll-btn.up-btn').click(function() {
        thumbIndex = (thumbIndex - 1 + totalThumbs) % totalThumbs;
        showThumbnails();
    });

    $('.scroll-btn.down-btn').click(function() {
        thumbIndex = (thumbIndex + 1) % totalThumbs; 
        showThumbnails();
    });
});

$(document).ready(function() {
    function updatePrice() {
        var selectedOption = $('#size-select option:selected');
        var newPrice = selectedOption.data('price');
        
        if (newPrice !== undefined && newPrice !== null) {
            $('#product-new-price').text(newPrice + '$');  
            $('#hidden-price').val(newPrice);  
        } else {
            $('#product-new-price').text('Price not available');
            $('#hidden-price').val(''); 
        }
    }

    $('#size-select').change(updatePrice);
    
    updatePrice();  
});




function populateSizes(productId) {
    fetch(`/api/sizes/?product_id=${productId}`)
        .then(response => response.json())
        .then(data => {
            const sizeSelect = document.getElementById('sizeSelect');
            sizeSelect.innerHTML = ''; 
            data.sizes.forEach(size => {
                const option = document.createElement('option');
                option.value = size.id;
                option.textContent = `${size.size} ${size.unit}`;
                sizeSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching sizes:', error));
}







(function($){
    $(document).ready(function(){
        function updateSizes() {
            var productId = $('#id_product').val();
            var sizeField = $('#id_size');
            
            $.ajax({
                url: '{% url "get_sizes" %}',  
                data: {
                    'product_id': productId
                },
                success: function(data) {
                    sizeField.empty();
                    $.each(data.sizes, function(index, size) {
                        sizeField.append($('<option/>', {
                            value: size.id,
                            text: size.size + ' ' + size.unit
                        }));
                    });
                }
            });
        }

        $('#id_product').change(updateSizes);

        updateSizes();
    });
})(django.jQuery);




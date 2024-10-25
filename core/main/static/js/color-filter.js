$(document).ready(function() {
    var firstColorSwatch = $('.color-swatch').first();
    if (firstColorSwatch.length) {
        firstColorSwatch.trigger('click');
    }

    $('.color-swatch').each(function() {
        var colorCode = $(this).data('color');
        if (colorCode) {
            $(this).css('background-color', colorCode);
        }
    });

    $('.color-swatch').click(function(event) {
        event.preventDefault();

        var colorCode = $(this).data('color');
        var mainImageUrl = $(this).data('image-url');
        var thumbImages = $(this).data('thumb-images');

        if (!mainImageUrl || !thumbImages) {
            console.error('Missing image URL or thumbnail images for color option:', $(this));
            return;
        }

        $('#main-image').attr('src', mainImageUrl);

        var thumbsContainer = $('#product-imgs .thumbs-container .thumbs-wrapper');
        thumbsContainer.empty();

        thumbImages.split(',').forEach(function(imageUrl) {
            var thumbHtml = '<div class="product-preview">' +
                               '<img class="thumb-image" src="' + imageUrl + '" data-main-image="' + imageUrl + '" alt="Product Thumbnail">' +
                           '</div>';
            thumbsContainer.append(thumbHtml);
        });

        $('.color-swatch').removeClass('active');
        $(this).addClass('active');
    });
});

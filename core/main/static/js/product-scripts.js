$(document).ready(function() {
    function changeMainImage(imageUrl) {
        $('#main-image').attr('src', imageUrl);
    }

    $('#product-imgs').on('click', '.thumb-image', function() {
        $('.thumb-image').removeClass('selected');
        
        $(this).addClass('selected');
        
        var newImageUrl = $(this).data('main-image');
        if (newImageUrl) {
            changeMainImage(newImageUrl);
        }
    });
});
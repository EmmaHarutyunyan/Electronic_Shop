document.addEventListener('DOMContentLoaded', function() {
    function moveDescription() {
        const descriptionSection = document.querySelector('#tab1');
        const productDetails = document.querySelector('.product-details');

        if (descriptionSection && productDetails) {
            productDetails.parentNode.insertBefore(descriptionSection, productDetails.nextSibling);
        }
    }

    moveDescription();

    const colorPreviews = document.querySelectorAll('.color-preview');

    colorPreviews.forEach(function(preview) {
        var colorCode = preview.getAttribute('data-color-code').trim();
        
        if (colorCode) {
            if (/^#[0-9A-Fa-f]{6}$/.test(colorCode)) {
                preview.style.backgroundColor = colorCode;
            } else {
                console.warn('Invalid color code:', colorCode);
                preview.style.backgroundColor = '#CCCCCC';
            }
        } else {
            console.warn('No color code provided.');
            preview.style.backgroundColor = '#CCCCCC';
        }

        preview.addEventListener('click', function(event) {
            event.preventDefault();

            const productUrl = this.getAttribute('data-product-url');

            if (productUrl) {
                window.location.href = productUrl;
            } else {
                console.error('No product URL found for the selected color.');
            }
        });
    });
});

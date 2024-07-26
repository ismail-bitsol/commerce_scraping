document.addEventListener('DOMContentLoaded', () => {
    const searchButton = document.getElementById('search-btn');
    const searchQuery = document.getElementById('search-query');
    const resultsTable = document.getElementById('results-table').getElementsByTagName('tbody')[0];
    const bestProductDiv = document.getElementById('best-product');
    const loadingDiv = document.getElementById('loading');

    searchButton.addEventListener('click', () => {
        const query = searchQuery.value.trim();
        if (!query) {
            alert('Please enter a product name');
            return;
        }

        loadingDiv.style.display = 'block';
        fetch(`/api/search/?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                loadingDiv.style.display = 'none';
                resultsTable.innerHTML = '';
                bestProductDiv.innerHTML = '';

                if (data.error) {
                    alert('Error: ' + data.error);
                    return;
                }

                if (data.message) {
                    resultsTable.innerHTML = '<tr><td colspan="5">' + data.message + '</td></tr>';
                    return;
                }

                data.products.forEach(product => {
                    const row = resultsTable.insertRow();
                    row.insertCell(0).innerText = product.name;
                    row.insertCell(1).innerText = product.website.name;
                    row.insertCell(2).innerText = product.price;
                    row.insertCell(3).innerText = product.reviews;
                    row.insertCell(4).innerText = product.sentiment_score;
                });

                // Find and display the best product
                const bestProduct = data.best_product;
                if (bestProduct) {
                    bestProductDiv.innerHTML = `
                        <h2>Best Product</h2>
                        <p><strong>Product:</strong> ${bestProduct.name}</p>
                        <p><strong>Website:</strong> ${bestProduct.website.name}</p>
                        <p><strong>Price:</strong> ${bestProduct.price}</p>
                        <p><strong>Reviews:</strong> ${bestProduct.reviews}</p>
                        <p><strong>Sentiment Score:</strong> ${bestProduct.sentiment_score}</p>
                    `;
                }
            })
            .catch(error => {
                loadingDiv.style.display = 'none';
                alert('An error occurred while fetching data. Please try again later.');
                console.error('Error fetching data:', error);
            });
    });
});


// product_hunt/static/product_hunt/scripts.js
$(document).ready(function() {
    $('#search-button').click(function() {
        let query = $('#search-query').val().trim();
        if (query === '') {
            alert('Please enter a product name.');
            return;
        }

        $('#loading').removeClass('hidden');
        $('#product-table').addClass('hidden');
        $('#error-message').addClass('hidden');
        $('#product-table tbody').empty();

        $.ajax({
            url: '/api/products/',
            type: 'GET',
            data: { search: query },
            success: function(response) {
                $('#loading').addClass('hidden');
                if (response.length === 0) {
                    $('#error-message').text('No products found.').removeClass('hidden');
                    return;
                }

                let rows = '';
                response.forEach(product => {
                    rows += `
                        <tr>
                            <td>${product.name}</td>
                            <td>${product.price}</td>
                            <td>${product.reviews}</td>
                            <td>${product.sentiment_score}</td>
                            <td>${product.website}</td>
                        </tr>
                    `;
                });

                $('#product-table tbody').html(rows);
                $('#product-table').removeClass('hidden');
            },
            error: function() {
                $('#loading').addClass('hidden');
                $('#error-message').text('An error occurred while fetching the data.').removeClass('hidden');
            }
        });
    });
});

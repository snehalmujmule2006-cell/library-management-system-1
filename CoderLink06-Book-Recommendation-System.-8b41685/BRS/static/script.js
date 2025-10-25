document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const genreFilter = document.getElementById('genreFilter');
    const yearFrom = document.getElementById('yearFrom');
    const yearTo = document.getElementById('yearTo');
    const ratingFilter = document.getElementById('ratingFilter');
    const booksGrid = document.getElementById('booksGrid');
    const recommendationsSection = document.getElementById('recommendationsSection');
    const recommendationsList = document.getElementById('recommendationsList');

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    async function searchBooks() {
        const query = searchInput.value;
        const filters = {
            genre: genreFilter.value,
            year_from: yearFrom.value ? parseInt(yearFrom.value) : null,
            year_to: yearTo.value ? parseInt(yearTo.value) : null,
            rating_from: ratingFilter.value ? parseFloat(ratingFilter.value) : null
        };

        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query, filters }),
            });

            const books = await response.json();
            displayBooks(books);
        } catch (error) {
            console.error('Error searching books:', error);
        }
    }

    function displayBooks(books) {
        booksGrid.innerHTML = '';
        books.forEach(book => {
            const bookCard = createBookCard(book);
            booksGrid.appendChild(bookCard);
        });
        attachBookCardListeners();
    }

    function createBookCard(book) {
        const bookCard = document.createElement('div');
        bookCard.className = 'book-card';
        bookCard.dataset.title = book.title;
        bookCard.innerHTML = `
            <div class="book-cover">
                <img src="${book.image_url}" alt="${book.title} cover">
                <div class="book-rating">
                    <span class="stars">★</span>
                    ${book.rating.toFixed(1)}
                </div>
            </div>
            <div class="book-info">
                <div class="book-title">${book.title}</div>
                <div class="book-author">by ${book.author}</div>
                <div class="book-genre">${book.genre}</div>
                <div class="book-year">${book.year}</div>
            </div>
        `;
        return bookCard;
    }

    function attachBookCardListeners() {
        const bookCards = document.querySelectorAll('.book-card');
        bookCards.forEach(card => {
            card.addEventListener('click', async () => {
                const selectedBook = card.dataset.title;
                await getRecommendations(selectedBook);
            });
        });
    }

    async function getRecommendations(selectedBook) {
        try {
            const response = await fetch('/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title: selectedBook }),
            });

            const recommendations = await response.json();
            displayRecommendations(recommendations);
        } catch (error) {
            console.error('Error fetching recommendations:', error);
        }
    }

    function displayRecommendations(recommendations) {
        recommendationsList.innerHTML = '';
        recommendations.forEach(book => {
            const bookCard = createBookCard(book);
            recommendationsList.appendChild(bookCard);
        });

        recommendationsSection.style.display = 'block';
        recommendationsSection.scrollIntoView({ behavior: 'smooth' });
        attachBookCardListeners();
    }

    // Event listeners
    const debouncedSearch = debounce(searchBooks, 300);
    searchInput.addEventListener('input', debouncedSearch);
    searchButton.addEventListener('click', searchBooks);
    genreFilter.addEventListener('change', searchBooks);
    yearFrom.addEventListener('change', searchBooks);
    yearTo.addEventListener('change', searchBooks);
    ratingFilter.addEventListener('change', searchBooks);

    // Initial book card listeners
    attachBookCardListeners();
});

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

app = Flask(__name__)

def load_books_data():
    # Popular books data with reliable image URLs
    books_data = [
        # Fantasy Series
        ('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 'Fantasy', 1997, 4.7, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1474154022i/3.jpg'),
        ('Harry Potter and the Chamber of Secrets', 'J.K. Rowling', 'Fantasy', 1998, 4.7, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1474169725i/15881.jpg'),
        ('Harry Potter and the Prisoner of Azkaban', 'J.K. Rowling', 'Fantasy', 1999, 4.8, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1630547330i/5.jpg'),
        ('The Fellowship of the Ring', 'J.R.R. Tolkien', 'Fantasy', 1954, 4.7, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1654215925i/61215351.jpg'),
        ('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 1937, 4.7, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1546071216i/5907.jpg'),
        
        # Young Adult Series
        ('The Hunger Games', 'Suzanne Collins', 'Young Adult', 2008, 4.5, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1586722975i/2767052.jpg'),
        ('Catching Fire', 'Suzanne Collins', 'Young Adult', 2009, 4.5, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1586722941i/6148028.jpg'),
        ('Mockingjay', 'Suzanne Collins', 'Young Adult', 2010, 4.4, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1586722855i/7260188.jpg'),
        
        # Mystery/Thriller
        ('The Da Vinci Code', 'Dan Brown', 'Thriller', 2003, 4.5, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1579621267i/968.jpg'),
        ('Angels & Demons', 'Dan Brown', 'Thriller', 2000, 4.4, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1696691958i/960.jpg'),
        ('Gone Girl', 'Gillian Flynn', 'Thriller', 2012, 4.4, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1554086139i/19288043.jpg'),
        
        # Fantasy Series
        ('A Game of Thrones', 'George R.R. Martin', 'Fantasy', 1996, 4.7, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1273763400i/8189620.jpg'),
        ('A Clash of Kings', 'George R.R. Martin', 'Fantasy', 1998, 4.7, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1567840212i/10572.jpg'),
        ('A Storm of Swords', 'George R.R. Martin', 'Fantasy', 2000, 4.8, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1571318786i/62291.jpg'),
        
        # Percy Jackson Series
        ('The Lightning Thief', 'Rick Riordan', 'Fantasy', 2005, 4.6, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1400602609i/28187.jpg'),
        ('The Sea of Monsters', 'Rick Riordan', 'Fantasy', 2006, 4.5, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1400602647i/28186.jpg'),
        ('The Titan\'s Curse', 'Rick Riordan', 'Fantasy', 2007, 4.5, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1400602668i/561456.jpg'),
        
        # Popular Standalone Books
        ('The Book Thief', 'Markus Zusak', 'Historical Fiction', 2005, 4.7, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1522157426i/19063.jpg'),
        ('The Fault in Our Stars', 'John Green', 'Young Adult', 2012, 4.5, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1660273739i/11870085.jpg'),
        ('The Alchemist', 'Paulo Coelho', 'Fiction', 1988, 4.6, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1654371463i/18144590.jpg'),
        
        # Science Fiction
        ('Dune', 'Frank Herbert', 'Science Fiction', 1965, 4.6, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1555447414i/44767458.jpg'),
        ('Ready Player One', 'Ernest Cline', 'Science Fiction', 2011, 4.5, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1500930947i/9969571.jpg'),
        ('The Martian', 'Andy Weir', 'Science Fiction', 2011, 4.7, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1413706054i/18007564.jpg'),
        
        # Modern Classics
        ('The Kite Runner', 'Khaled Hosseini', 'Fiction', 2003, 4.7, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1579036753i/77203.jpg'),
        ('Life of Pi', 'Yann Martel', 'Adventure', 2001, 4.5, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1631251689i/4214.jpg'),
        ('The Shadow of the Wind', 'Carlos Ruiz Zafón', 'Fiction', 2001, 4.7, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1344545047i/1232.jpg')
    ]
    
    # Create DataFrame from books_data
    titles, authors, genres, years, ratings, images = zip(*books_data)
    descriptions = [f"A compelling {genre} novel by {author}" for genre, author in zip(genres, authors)]
    
    return pd.DataFrame({
        'title': titles,
        'author': authors,
        'genre': genres,
        'description': descriptions,
        'year': years,
        'rating': ratings,
        'image_url': images
    })

# Load books data
books = load_books_data()

def get_genre_recommendations(title, max_recommendations=6):
    # Get the book's genre
    book = books[books['title'] == title].iloc[0]
    book_genre = book['genre']
    
    # Get all books in the same genre, excluding the input book
    genre_books = books[
        (books['genre'] == book_genre) & 
        (books['title'] != title)
    ]
    
    # Sort by rating and get top recommendations
    recommendations = genre_books.nlargest(max_recommendations, 'rating')
    return recommendations.to_dict('records')

def search_books(query, filters=None):
    if filters is None:
        filters = {}
    
    results = books.copy()
    
    # Apply text search
    if query:
        query = query.lower()
        mask = (
            results['title'].str.lower().str.contains(query) |
            results['author'].str.lower().str.contains(query) |
            results['genre'].str.lower().str.contains(query)
        )
        results = results[mask]
    
    # Apply filters
    if 'genre' in filters and filters['genre']:
        results = results[results['genre'] == filters['genre']]
    
    if 'year_from' in filters and filters['year_from']:
        results = results[results['year'] >= filters['year_from']]
    
    if 'year_to' in filters and filters['year_to']:
        results = results[results['year'] <= filters['year_to']]
    
    if 'rating_from' in filters and filters['rating_from']:
        results = results[results['rating'] >= filters['rating_from']]
    
    # Sort by rating by default
    results = results.sort_values('rating', ascending=False)
    
    return results.to_dict('records')

@app.route('/')
def home():
    # Get unique genres for the filter dropdown
    genres = sorted(books['genre'].unique())
    return render_template('index.html', books=books.to_dict('records'), genres=genres)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '')
    filters = data.get('filters', {})
    results = search_books(query, filters)
    return jsonify(results)

@app.route('/recommend', methods=['POST'])
def recommend():
    title = request.json['title']
    recommendations = get_genre_recommendations(title)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)

import pandas as pd
import streamlit as st

# Function to load data
@st.cache(persist=True)
def load_data():
    # Load books data
    books = pd.read_csv('BX_Books.csv', encoding='latin-1', sep=';')
    books.columns = ['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-S', 'Image-URL-M', 'Image-URL-L']

    # Load ratings data
    ratings = pd.read_csv('BX-Book-Ratings.csv', encoding='latin-1', sep=';')
    ratings.columns = ['User-ID', 'ISBN', 'Book-Rating']

    return books, ratings

# Function to get book name based on ISBN
def get_book_name(isbn, books):
    book_name = books.loc[books['ISBN'] == isbn, 'Book-Title'].values
    return book_name[0] if len(book_name) > 0 else "Unknown Title"

# Function to recommend books for a user
def recommend_books_for_user(user_id, ratings, books, num_recommendations=5):
    # Filter ratings for the specified user
    user_ratings = ratings[ratings['User-ID'] == user_id]

    # Get top-rated books by this user
    top_rated_books = user_ratings.sort_values(by='Book-Rating', ascending=False).head(10)

    # Extract ISBNs of top-rated books
    recommended_books_isbn = top_rated_books['ISBN'].tolist()

    # Get book names for recommended ISBNs
    recommended_books_names = [get_book_name(isbn, books) for isbn in recommended_books_isbn]

    return recommended_books_names[:num_recommendations]

# Main function to run the app
def main():
    # Load data
    books, ratings = load_data()

    # Sidebar for user input
    st.sidebar.title('Book Recommendation System')
    st.sidebar.write("Note: Use User ID 500, 300, 900, or 777 for testing purposes.")
    user_id = st.sidebar.text_input('Enter User ID')

    # Convert user_id input to integer
    try:
        user_id = int(user_id)
    except ValueError:
        st.write('Please enter a valid User ID.')
        return

    # Get book recommendations for the user
    recommended_books = recommend_books_for_user(user_id, ratings, books)

    # Display recommended books
    st.title(f'Top Book Recommendations for User {user_id}:')
    if recommended_books:
        for i, book in enumerate(recommended_books):
            st.write(f"{i + 1}: {book}")
    else:
        st.write('No recommendations found for this user.')

# Run the app
if __name__ == '__main__':
    main()

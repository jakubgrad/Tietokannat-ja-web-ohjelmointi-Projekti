# Tietokannat-ja-web-ohjelmointi-Projekti
A repository for the course project in Tietokannat ja web-ohjelmointi taken in the 4th period of academic year 2023-2024 at University of Helsinki.

The goal of the project is to create an online application that supports billingual reading. Billingual reading is a practice of reading the same book in 2 languages. The app would allow users to log in and upload pairs of machine-readable pdfs of the same book in two different languages. The website would process the pdfs, perform sentence tokenization using spacy or similar library, and then upload them to the server. The users would then be able to choose a pair of books that they uploaded and read them side by side. The goal is to make the UI user friendly, so that there is shortcuts for e.g. skipping the page or aligning the text of the two books and leaving bookmarks.

The assumption is that the uploaded books were purchased and used by users only for their own reading. Because of strict rules against intellectual theft, administrators need be able to delete books and users if they violate the Terms of Service or an intellectual right of authors.

The database would need to have at least the following tables:
-a table with users (username as email and password), possibly the same or a separate table with administrators 
-a table for uploaded pdfs that contains names, author, cover image, language, details and ids of books
-and a table that keeps track of settings and progress for individual users reading a particular pair of books. So for instance which sentence was being read from one book of the pair together with which sentence from the other, by whom, and how many sentences at a time.
-a table for named bookmarks, purely out of convenience for the reader
-a table for saved words. I also want to include a search box for translation using trans, a bash script that very quickly translates sentences and individual words that I have hotkeyed on my computer


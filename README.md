# Tietokannat-ja-web-ohjelmointi-Projekti
A repository for the course project in Tietokannat ja web-ohjelmointi taken in the 4th period of academic year 2023-2024 at University of Helsinki.

The goal of the project is to create an online application that supports billingual reading. Billingual reading is a practice of reading the same book in 2 languages. The app would allow users to log in and upload pairs of machine-readable pdfs of the same book in two different languages. The website would process the pdfs, perform sentence tokenization, and upload them to the server. The users would then be able to choose a pair of books that they uploaded and read them side by side. The goal is to make the UI user friendly, so that there is shortcuts for e.g. skipping the page or aligning the text of the two books.

The assumption is that the uploaded books were purchased and used by users only for their own reading. Because of strict rules against intellectual theft, administrators need be able to delete books and users if they violate the Terms of Service or an intellectual right of authors.

The database would need to have at least the following: a table with users (username as email and password), a table with administrators, a table for uploaded pdfs, and a table that keeps track of settings and progress for individual users reading a particular pair of books. 

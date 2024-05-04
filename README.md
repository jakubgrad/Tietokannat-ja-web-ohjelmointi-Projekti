# Tietokannat-ja-web-ohjelmointi-Projekti
A repository for the course project in [Tietokannat ja web-ohjelmointi](https://hy-tsoha.github.io/materiaali/) taken in the 4th period of academic year 2023-2024 at University of Helsinki by a student of Bachelor's Programme in Science.

The goal of the project is to create **an online application that supports billingual reading** in Python using a `Postgres` database. Billingual reading is a practice of reading the same book in 2 languages. The app would allow users to log in and upload pairs of machine-readable pdfs of the same book in two different languages. The website would process the pdfs, perform sentence tokenization using `spacy` or similar library, and then upload them to the server. The users would then be able to choose a pair of books that they uploaded and read them side by side. The goal is to make the UI user friendly, so that there is e.g. the possiblity pf aligning the text of the two books and leaving bookmarks.
<p align="center">
    <img src="https://github.com/jakubgrad/Tietokannat-ja-web-ohjelmointi-Projekti/assets/113715885/52d16808-046b-4268-b40d-c568f68be4ca" width="50%" alt="Description of the image">
</p>


The assumption is that the uploaded books were purchased and used by users only for their own reading. Because of strict rules against intellectual theft, administrators need be able to delete books and users if they violate the Terms of Service or an intellectual right of authors.

Technical details: the project has many dependencies, including `Python Flask`, `Flask SqlAlchemy`, `Psycopg2` and so on. The full list is in the `requirements.txt` document and the installation is for them is outlined below. The project use a virtual environment.
<br>
Tested using [https://vdi.helsinki.fi/](https://vdi.helsinki.fi/]), university's online virtual machine running on Cubbli.
<br>

The database would should eventually have the following tables:
```
-a table with users (username as email and password), possibly the same or a separate table with administrators 
-a table for uploaded pdfs that contains names, author, cover image, language, details and ids of books
-a table for pairs of pdfs to read
-and a table that keeps track of settings and progress for individual users reading a particular pair of books. So for instance which sentence was being read from one book of the pair together with which sentence from the other, by whom, and how many sentences at a time.
-a table for named bookmarks, purely out of convenience for the reader
-a table for saved words. I also want to include a search box for translation using trans, a bash script that very quickly translates sentences and individual words that I have hotkeyed on my computer
```

Manual installation instructions created basing on university's Cubbli OS (in production is a single script that could handle installation):<br>
Install postgresql if you haven't already. You can follow the instructions [here](https://github.com/hy-tsoha/local-pg) or do the following at your university computer:
```
cd ~
touch .bashrc #possibly the file existed already
git clone https://github.com/hy-tsoha/local-pg.git
bash local-pg/pg-install.sh install .bashrc
```
To start postgresql database, run:
```
source .bashrc # or reload the terminal or log out and log in
start-pg.sh  
```
The database is necessary for the application to work, but once you're finished using the application, remember to close it with `Ctrl + c`. Now that your database is running, in a separate terminal run:
```
psql -h ~/pgsql/sock/ 
```
If your prompt has changed to `username=#`, that means that psql works correctly. You can exit it by pressing `Ctrl + d`.
Now let's download this repository. The location is actually important here, since if we install in a symlinked directory like Desktop, Downloads, or Documents, we won't be able to start a Python virtual environment later on. For me, installing in my /home/ad/lxhome/g/<username>/Linux directory works the best. So you can simply go over to: 
```
cd /home/ad/lxhome/g/<your_username>/Linux
git clone https://github.com/jakubgrad/Tietokannat-ja-web-ohjelmointi-Projekti.git
```
Now you want to populate the database with tables and some sample data:
```
psql -h ~/pgsql/sock/ < Tietokannat-ja-web-ohjelmointi-Projekti/schema.sql 
```
Go to the repository, install and enter the virtual environment:
```
cd Tietokannat-ja-web-ohjelmointi-Projekti/
python3 -m venv venv #It can take 20 seconds. Also, if you get Errno 95, you need to download the repository somewhere else and run this line inside it
source venv/bin/activate
```
Now your prompt should be preceeded with `(venv)` and you can install the dependencies for the application:
```
pip install -r requirements.txt      
```
Because my project using a pdf parser etc. it can also take a bit to intsall the requierements. After that, declare environment variables:
```
echo -e "DATABASE_URL=postgresql+psycopg2://\nSECRET_KEY="$(python3 -c "import secrets; print(secrets.token_hex(16))") > .env
```
Go to `src` and run the program:
```
cd src/
flask run
```
You should see:
```
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
And you can now head over to localhost:5000 in your browser and see the program in action.<br/>
Because of the nature of pdf parsing, the application will reject a lot of pdfs or else, format them in strange ways. Because of it, the repository contains two pdfs that are ready to use and tested, residing in the `/examples` directory. So when using the application for the first time, I recommend to:
- register
- click on `Upload a pdf`
- In the file explorer window click on home, find the `Tietokannat-ja-web-ohjelmointi-Projekti`, go to examples and *voila*, there is J.K Rowling's Half Blood Prince in English and Finnish. Upload the files one after the other. Then, click on `Create a pair of pdfs for billingual reading`, name the pair, select ids 1 and 2 and `Create a new pair!`. You can read right away. `Next paragraph` and `Previous paragraph` move both of the books back and forth 3 sentences by default. `+` and `-` move either of the books by one sentence, so that whenver the two versions have different number of sentences, you can keep reading.

# Useful commands
See linting report:
```
pylint src/*.py
```
# Troubleshooting
I found that frequently launching and closing university VMs confused web browsers. For a quick fix when none of your browsers want to open, run:
```
rm -rf ~/.config/chromium/Singleton*
rm -rf ~/.config/google-chrome/Singleton*
```
It frees up both chrome and chromium.
# To do
- I want to implement the UI using a bootstrap, thus giving it a nicer look.
- I want to implement all the tables mentioned above
- I want to host the application on my server

[Peer review 1](https://github.com/Karri6/db-and-web-dev/issues/3)
[Peer review 2](https://github.com/rautiais/tohoilykisa/issues/2)

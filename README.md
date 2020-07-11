# fross123 CS50 Web -- 2020
## Project1 - Wiki

### urls.py
- index
- search
- new entry
- random entry
- entry
  - title as variable
- edit
  - title as variable + edit

###  views.py
#### Forms
1. SearchForm
    - form field for search bar
2. createForm
    - Form fields to create new entries
3. EditForm
    - Form fields to edit current entries
    - only difference is that it does not include 'title' as an option

#### views
1. index
2. entry
    - view for a specific entry
    - pass in title
    - if entry does not exist, render error template
3. search
    - searches through entries
    - if a search matches, entry is displayed
    - partial matches are displayed in a list
    - no results display error page
    - invalid search displays error page
4. new
    - renders new entry html page and form
    - when form is submitted:
        - if entry exists, error is shown
        - if not then entry is saved
        - invalid submissions display error
5. edit
    - renders edit entry page
        - current content of entry is populated
    - on form submission:
        - saves the updated content to the same entry
6. random
    - automatically picks an entry from the current list of entries
    - redirects to selected entry

### Templates
1. layout.html
    - html layout for app
2. edit.html
    - for editing current wiki pages
3. new.html
    - for creating new wiki pages
4. entry.html
    - to display entries
5. search.html
    - displays search results
6. index.html
    - homepage for app
    - displays list of all entries
7. error.html
    - used to display various error messages

Static files were not changed from distribution code.

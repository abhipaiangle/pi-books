# Project Book Review

This project has been made using Flask, HTML, Bootstrap4. The default route takes you to the login page which also has the link to register page. 
After you enter the login page with credentials username and password, 
it displays list of books with a search tool where you can type title, author or isbn (fully or partially).
When you click on the book, it displays the specification of books with a review bar where you can write a review
and rate the book out of 5. Review can be written only once per user.
There is an api page also which returns json object having specifications of book with the correct ISBN.

Click on this [link](https://www.youtube.com/watch?v=UL9JXGEUnwA) to see the working of this dynamic website.

Click on this [link](https://app-pibooks.herokuapp.com) to see the deployed application.

DATABASE_URL: postgres://qrftzlljuljfji:06a0ab1de75e0001c0e6c1351af6c9e32c504cce6dd22181f4e9e5f1c98d0292@ec2-52-71-231-180.compute-1.amazonaws.com:5432/db7bjt7tu968e9


Note: The api key from Goodreads after significant amount of requests was corrupted and hence had to renew it. So incase the key is not working please enter a new key in the book() function of application.py


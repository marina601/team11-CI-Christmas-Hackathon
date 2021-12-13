# The WishingTree - Testing details

[Main README.md file](README.md)

[View deployed site here](https://scooter-circle.herokuapp.com/)

# Table of Contents

[**Testing**](#testing)
   - [**Validation Results**](#validation-results)
   - [**Testing User Stories**](#user-stories-testing)
        - [**First Time User**](#first-time-user)
        - [**Returning User**](#returning-user)
        - [**Frequent User**](#frequent-user)
        - [**Business Goals**](#business-goals)
   - [**Further Testing**](#further-testing)
      - [**Device Compatibility Table**](#device-compatibility-table)
      - [**Elements on Every Page**](#elements-on-every-page)
      - [**Home Page**](#home-page)
      - [**Registration Page**](#registration-page)
      - [**Login Page**](#login-page)
      - [**Profile Page**](#profile-page)
      - [**Edit Wish page**](#edit-review)
      - [**Wishing Tree Page**](#products-page)
      - [**Add Group Page**](#add-product) 
      - [**Add Wish Page**](#edit-product) 
      - [**404 Page**](#404-page)
      - [**500 Page**](#500-page)
   - [**Google Lighthouse Testing**](#google-lighthouse-testing)
   - [**Cross Browser Compatibility Table**](#cross-browser-compatibility-table)
   - [**Bugs**](#bugs)

## Validation Results

- The W3C Markup Validator and W3C CSS Validator Services were used to validate every page of the project to ensure there were no syntax errors in the project.

- [PEP8](http://pep8online.com/) has been used to ensure Python code is fully compliant.
    - removed white space, ensured correct indentation is in place, shorted the lines which were too long for visual effect

- [W3C CSS validation](https://jigsaw.w3.org/css-validator/)
  - The file passed without any errors

- [W3C Markup Validation](https://validator.w3.org/)
   - HTML code passed validation without major errors.
   
| Pages    |<strong>HTML Validation</strong>|
|----------|:---------------------:|
| Home     | &check; | 
| Login   | &check; |  
| Register    | &check; | 
| Add Group | &check; | 
| Wishing Tree | &check; |
| Profile | &check; | 
| Add Wish | &check; | 
| Edit Wish | &check; | 
| 404.html | &check; | 
| 500 Page | &check; |

404 and 500 pages had missing alt attributes and were added. Edit wish page had a required attribute that caused issues, but was removed.


- [JSHint](https://jshint.com/) was used to check the js file and validation passed with 2 issues
    - undefined variable M 
    - unused variable 'instance'

 Both variables are coming from Materialize framework and therefore have been ignored.

- [Dr Link Check](https://www.drlinkcheck.com/)
   - Has been user to validate the links on the site
   - No issues has been found 

## Further Testing

### Login Page

- Go to the login page, confirm that the login form is displayed correctly.
- Try to submit the form without entering any details, confirm custom feedback is displayed, which tells the user to enter a valid username.
- Enter the username, but not the password, confirm custom feedback is displayed, telling the user to enter a valid password. The input field also turns red on invalid input.
- Try to login with a username or password which does not exists in the database, confirm the flash message is displayed letting the user know that some of the details entered are incorrect.
- Try to login using the correct username and password, confirm that the input fields change the colour to green on the valid entry.
- Confirm that the logged-in user is redirected to their wishing tree page.
- Log out, then try to log in the using correct username and password, confirm that this is successful.
- Confirm *Register Here* link takes the user to the registration page.
- Above steps have been repeated on mobile and tablet devices. No changes to this page layout across the different screen sizes.
- Confirm the navbar has changed based on user access.
- As a logged-in user, try to access the Login Page by modifying the URL, confirm the user has been redirected to their profile page. Flash message displayed telling the user they are already logged in.

##### back to [content](#table-of-content)

### 404 Page

- Starting at the desktop view, typed some random characters after the URL and custom 404 page is displayed.
- Hover over the logo on the left hand side which leads to the home page.
- Clicked on the logo and the link has diverted the user to the home page. 
- Repeated the following steps for tablet and mobile view. 
- The result was satisfactory across the different size devices and browsers. 

##### back to [content](#table-of-content)


### 500 Page

- Custom server error page has been designed to provide feedback to the user
- The page provides the link for the user to return to the home page in the form of the logo on the left hand side
- To test this page I had to take the following steps
  1. inside the app.py file `from Flask import abort`
  2. add abort(500) before a return or redirect in any route
    - `@app.route("/index")
       def index():
       """
       Route to index template
       """
      abort(500)
      return render_template("home.html")`
  
  - We have used the above code to test our custom 500.html, then removed abort from import in Flask and abort(500) within the route
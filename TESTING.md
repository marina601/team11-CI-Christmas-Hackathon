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
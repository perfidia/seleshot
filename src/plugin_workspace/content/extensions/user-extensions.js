// Generate random text for a variable
// Possible options:
//   length      number indicating how long to make the string (defaults to 8)
//
//   type        string indicating what type of string to create alpha, numeric
//               or alphanumeric (defaults to alphanumeric)
//
//   length|type pipe delimited option list

// from the openqa wiki - http://wiki.openqa.org/display/SIDE/Contributed+Extensions+and+Formats

Selenium.prototype.getTextLength = function(locator, text) {
    return this.getText(locator).length;
};


/*
 * Adds a new option to a dropdown list and selects that option.
 *  locator - locator for the dropdown element to add the option to
 *  text - the option value to set.
 */
Selenium.prototype.doSelectNew = function(locator, text) {
     var element = this.page().findElement(locator);
     if (element.type.match(/select-+/i)) {
         element.options[element.options.length] = new Option(text, text);
         element.options[element.options.length - 1].selected = true;    
     }
}	


// The following examples try to give an indication of how Selenium can be extended with javascript.
function createCookie(doc, name,value, path,days)
{
        if (!path) {
            path = "/";        
        }
    
        if (days)
        {
                var date = new Date();
                date.setTime(date.getTime()+(days*24*60*60*1000));
                var expires = "; expires="+date.toGMTString();
        }
        else var expires = "";
        doc.cookie = name+"="+value+expires+"; path="+path;
}

/*
 * Removes the cookie with the given name.
 *  text - the cookie name
 *  path - the cookie path
 */
Selenium.prototype.doRemoveCookie = function(text, path) {    
    createCookie(this.page().currentDocument, text, "", path, -1);
};	
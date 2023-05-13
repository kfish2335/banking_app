# Alpaca Valley Bank



<h3>Demo:</h3>
<blockquote> http://flask-env.eba-gmwa2ucz.us-east-1.elasticbeanstalk.com/ </blockquote>

</br>

<h3>About:</h3>
This is application is a banking app that allow the user to do the following:

<ul>
 <li>Create an account</li>
 <li>Check account balance</li>
 <li>Withdraw from account</li>
 <li>Add to account</li>
</ul>

The tech stack used:
<ul>
 <li>Pyhton-Flask</li>
 <li>Bootstrap</li>
</ul>


This application has four pages that the user can access.

<ul>
<li>home</li>
<li>login</li>
<li>register</li>
<li>dashboard</li>
</ul>

The Login page is form that allow the user to login into there account. User need to enter a valid username and password to login. WTForm are used for generating form. By using WTForm, we are able to use python to make form inputs in HTML. This allow the our server to validate user input data. Another benefit of WTForms is that it's provides a built-in mechanism to protect against CSRF attacks, which is a common vulnerability in web applications. WTForm is used on all forms throught out the form.

The Register Page is form that User could sign up to our application. The user will have to create a username, password, and amount of money they would like to start with. Using WTForm, the server checks to make sure that username is unquie and raise an error if that username is in use. The password hash value is stored on the server. 

The Dashboard page is portal that user could use to view and update thier current balances. This page is only available if the user is logged in. The user has two buttons that allow User to change thier balanceson thier account. One Button is for increasing funds and the other is for decreasing funds. The applications does not allow user to decrease it funds below zero and will raise an errorto the user.

Possible Future update:
<ul>
 <li>Recording user Transaction</li>
 <li>Display Transaction to users</li>
 <li>Add first and last name fields</li>
 <li>Add catogery field to deposit and tranfer fields</li>
</ul>

<h3>How to run app locally:</h3>
<br/>
<h4>Create a Virtual Environment:</h4>
<br/>
<blockquote>
<code>
pip install virtualenv
<br/>
py -m venv env
</code>
</blockquote>
<br/>
<h4>Activate Virtual Environment:</h4>
<blockquote>
On Windows, run:

<code>tutorial-env\Scripts\activate.bat</code>

On Unix or MacOS, run:<br/>
<code>source tutorial-env/bin/activate</code>
</blockquote>

<h4>Install Dependencies:</h4>
<blockquote>

<code>pip install -r requirements.txt</code>

</blockquote>

<h4>Start app:</h4>
<blockquote>

<code>py application.py</code>

</blockquote>

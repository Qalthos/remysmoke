<%inherit file="local:templates.mobile_master"/>
<%def name="title()">Login Form</%def>
<div id="loginform">
  <form action="${tg.url('/login_handler', params=dict(came_from=came_from.encode('utf-8'), __logins=login_counter.encode('utf-8')))}" method="POST" class="loginfields">
    <h2>Login</h2>
    <span>Username:</span><br />
	<input type="text" id="login" name="login" class="text"></input><br />
    <span>Password:</span><br />
	<input type="password" id="password" name="password" class="text"></input><br />
    <span>remember me</span>
	<input type="checkbox" id="loginremember" name="remember" value="2252000"/>
	<br />
    <input type="submit" id="submit" value="Login" />
</form>
</div>

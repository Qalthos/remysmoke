<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    ${self.meta()}
    <title>${self.title()}</title>
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
</head>
<body class="${self.body_class()}">
  ${self.header()}
  ${self.main_menu()}
  ${self.content_wrapper()}
</body>

<%def name="content_wrapper()">
    <div id="content">
      ${self.body()}
    </div>
</%def>

<%def name="body_class()"> </%def>

<%def name="meta()">
  <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
</%def>

<%def name="title()"> </%def>

<%def name="header()">
  <div id="header">
  	<h1>
  		Welcome to Remysmoke
		<span class="subtitle">The web Python smoking tracker</span>
	</h1>
  </div>
</%def>

<%def name="main_menu()">
  <ul id="mainmenu">
    <li class="first"><a href="${tg.url('/')}" class="${('', 'active')}">Welcome</a></li>
        <li><a href="${tg.url('/week')}" class="${('', 'active')}">Weekly Charts</a></li>
        <li><a href="${tg.url('/month')}" class="${('', 'active')}">Monthly Charts</a></li>
        <li><a href="${tg.url('/year')}" class="${('', 'active')}">Annual Charts</a></li>
        <li><a href="${tg.url('/punch')}" class="${('', 'active')}">Smoking Punchcard</a></li>
        <li><a href="${tg.url('/stats')}" class="${('', 'active')}">Stats</a></li>

    % if tg.auth_stack_enabled:
      <span>
          % if not request.identity:
            <li id="login" class="loginlogout"><a href="${tg.url('/login')}">Login</a></li>
          % else:
            %if 'smoke' in request.identity['permissions']:
              <li id="admin"><a href="${tg.url('/smoke')}">Add Smoke</a></li>
            %elif 'manage' in request.identity['permissions']:
              <li id="admin"><a href="${tg.url('/admin')}">Admin</a></li>
            %endif
            <li id="login" class="loginlogout"><a href="${tg.url('/logout_handler')}">Logout</a></li>
          % endif
      </span>
    % endif
  </ul>
</%def>
</html>

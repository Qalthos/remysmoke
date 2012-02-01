<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    ${self.meta()}
    <title>${self.title()}</title>
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/admin.css')}" />
</head>
<body class="${self.body_class()}">
  ${self.header()}
  ${self.main_menu()}
  ${self.content_wrapper()}
  ${self.footer()}
</body>

<%def name="content_wrapper()">
    <div id="content">
      ${self.body()}
    </div>
</%def>

<%def name="body_class()">
</%def>
<%def name="meta()">
  <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
</%def>

<%def name="title()">  </%def>
<%def name="sidebar_top()">
  <div id="sb_top" class="sidebar">
      <h2>Get Started with TG2</h2>
      <ul class="links">
        <li>
          % if page == 'index':
              <span><a href="${tg.url('/about')}">About this page</a> A quick guide to this TG2 site </span>
          % else:
              <span><a href="${tg.url('/')}">Home</a> Back to your Quickstart Home page </span>
          % endif
        </li>
        <li><a href="http://www.turbogears.org/2.1/docs/">TG2 Documents</a> - Read everything in the Getting Started section</li>
        <li><a href="http://docs.turbogears.org/1.0">TG1 docs</a> (still useful, although a lot has changed for TG2) </li>
        <li><a href="http://groups.google.com/group/turbogears"> Join the TG Mail List</a> for general TG use/topics  </li>
      </ul>
  </div>
</%def>

<%def name="header()">
  <div id="header">
  	<h1>
  		Welcome to TurboGears 2
		<span class="subtitle">The Python web metaframework</span>
	</h1>
  </div>
</%def>
<%def name="footer()">
  <div class="flogo">
    <img src="${tg.url('/images/under_the_hood_blue.png')}" alt="TurboGears" />
    <p><a href="http://www.turbogears.org/">Powered by TurboGears 2</a></p>
  </div>
  <div class="foottext">
    <p>TurboGears is a open source front-to-back web development
      framework written in Python. Copyright (c) 2005-2009 </p>
  </div>
  <div class="clearingdiv"></div>
</div>
</%def>
<%def name="main_menu()">
  <ul id="mainmenu">
    <li class="first"><a href="${tg.url('/')}" class="${('', 'active')}">Welcome</a></li>
        <li><a href="${tg.url('/week')}" class="${('', 'active')}">Weekly Charts</a></li>
        <li><a href="${tg.url('/month')}" class="${('', 'active')}">Monthly Charts</a></li>
        <li><a href="${tg.url('/year')}" class="${('', 'active')}">Annual Charts</a></li>
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

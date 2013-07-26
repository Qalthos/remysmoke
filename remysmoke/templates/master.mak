<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
    % if tg.request.is_mobile:
      <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    % endif
    <title>${self.title()}</title>
    % if tg.request.is_mobile:
      <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/mobile_style.css')}" />
    % else:
      <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
    %endif
    ${self.head()}
  </head>
  <body>
    ${self.header()}
    ${self.main_menu()}
    ${self.content_wrapper()}
  </body>

<%def name="content_wrapper()">
    <div id="content">
      <% flash=tg.flash_obj.render('flash', use_js=False) %>
      % if flash:
        ${flash | n}
      % endif
      ${self.body()}
    </div>
</%def>

<%def name="head()"></%def>

<%def name="title()">Remysmoke: The Web-based Smoke Tracker</%def>

<%def name="header()">
  <div id="header">
    % if tg.request.is_mobile:
      <img src="${tg.url('/images/smoke_face.png')}" />
      <h1>Remysmoke</h1>
    % else:
      <h1>
        Welcome to Remysmoke
        <span class="subtitle">The web Python smoking tracker</span>
      </h1>
    % endif
  </div>
</%def>

<%def name="main_menu()">
  <div id='menudiv'>
    <ul id="mainmenu">
      % if not tg.request.is_mobile:
        <li class="first"><a href="${tg.url('/')}" class="${('', 'active')}">Welcome</a></li>
        <li><a href="${tg.url('/week')}" class="${('', 'active')}">Weekly Charts</a></li>
        <li><a href="${tg.url('/month')}" class="${('', 'active')}">Monthly Charts</a></li>
        <li><a href="${tg.url('/year')}" class="${('', 'active')}">Annual Charts</a></li>
        <li><a href="${tg.url('/punch')}" class="${('', 'active')}">Smoking Punchcard</a></li>
        <li><a href="${tg.url('/stats')}" class="${('', 'active')}">Stats</a></li>
      % endif

      % if tg.auth_stack_enabled:
        <span>
          % if not request.identity:
            <li id="login" class="loginlogout"><a href="${tg.url('/login')}">Login</a></li>
          % else:
            %if 'smoke' in request.identity['permissions']:
              <li id="admin"><a href="${tg.url('/smoke')}">Add Smoke</a></li>
            %endif
            <li id="login" class="loginlogout"><a href="${tg.url('/logout_handler')}">Logout</a></li>
          % endif
        </span>
      % endif
    </ul>
  </div>
</%def>
</html>

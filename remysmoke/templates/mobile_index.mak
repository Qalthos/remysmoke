<%inherit file="local:templates.mobile_master"/>

<%def name="title()">
  Welcome to TurboGears 2.1, standing on the shoulders of giants, since 2007
</%def>

<div id="getting_started">
  <ul id="mainmenu">
    % if tg.auth_stack_enabled:
      % if not request.identity:
        <li id="login"><a href="${tg.url('/m_login')}">Login</a></li>
      % else:
        %if 'smoke' in request.identity['permissions']:
          <li id="admin"><a href="${tg.url('/m_smoke')}">Add Smoke</a></li>
        %endif
        <li id="login"><a href="${tg.url('/logout_handler')}">Logout</a></li>
      % endif
    % endif
  </ul>
</div>

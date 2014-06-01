<%inherit file="local:templates.master"/>
<%def name="title()">Login Form</%def>

<div id='loginform'>
  <form action="${tg.url('user_control')}" class='loginfields'>
    <h2><span>User Control</span></h2>
    % if not request.identity:
      ${h.fbauth.register_button(api_key, text='Register with Facebook', scope=None, remember='')}
      <p> --OR-- </p>
      ${h.fbauth.login_button(api_key, text='Login with Facebook', scope=None, remember='')}
    % elif not request.identity['user'].fbauth:
      ${h.fbauth.connect_button(api_key, text='Connect your Facebook account', scope=None)}
    % else:
      <input type='checkbox' id='public' name='public' class='check' />
      <label for='public'>Make my data public:</label>
      <input type='submit' id='submit' value='Save' />
    % endif
  </form>
</div>

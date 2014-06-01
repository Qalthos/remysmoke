<%inherit file="local:templates.master"/>
<%def name="title()">Login Form</%def>

% if not request.identity:
<div class='fb_contain'>
  ${h.fbauth.register_button(api_key, text='Login with Facebook', scope=None, remember='')}
</div>
<form action="${tg.url('/login_handler', params=dict(came_from=came_from.encode('utf-8'), __logins=login_counter.encode('utf-8')))}" method="POST">
  <h2><span>Existing Login</span></h2>
  <label for="login">Username:</label>
  <input type="text" id="login" name="login" class="text" />

  <label for="password">Password:</label>
  <input type="password" id="password" name="password" class="text" />

  <input type="submit" class="submit" value="Login" />
</form>
% else:
  % if not request.identity['user'].fbauth:
    <div class='fb_contain'>
      ${h.fbauth.connect_button(api_key, text='Connect to Facebook', scope=None)}
    </div>
  % endif
<form action="${tg.url('user_control')}">
  <h2><span>User Control</span></h2>
  <input type='checkbox' id='public' name='public' class='check'
    % if request.identity['user'].public:
      checked=true
    % endif
  />
  <label for='public'>Make my data public:</label>
  <input type='submit' class='submit' value='Save' />
</form>
% endif

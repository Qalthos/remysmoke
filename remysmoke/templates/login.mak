<%inherit file="local:templates.master"/>
<%def name="title()">Login Form</%def>

<form action="${tg.url('user_control')}" class='loginfields'>
  <h2><span>User Control</span></h2>
  % if not request.identity:
    ${h.fbauth.register_button(api_key, text='Login with Facebook', scope=None, remember='')}
  % else:
    <input type='checkbox' id='public' name='public' class='check'
      % if request.identity['user'].public:
        checked=true
      % endif
    />
    <label for='public'>Make my data public:</label>
    <input type='submit' class='submit' value='Save' />
  % endif
</form>

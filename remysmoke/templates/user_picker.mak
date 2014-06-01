<%block name='user_picker'>
  <fieldset class='user'>
    % if public_users:
      <h2><span>Other users</span></h2>
      <label for='user'>User</label>
      <input type='text' id='user' name='user_name' class='text' list='users'
             value='${user.display_name if user else public_users[0].display_name}' />
      <datalist id='users'>
        % for visible_user in public_users:
          <option>${visible_user.display_name}</option>
        % endfor
      </datalist>
    % endif
  </fieldset>
</%block>

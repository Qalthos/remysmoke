<%block name='user_picker'>
  <fieldset class='user'>
    % if public_users:
      <h2><span>Change user</span></h2>
      <label for='user'>User</label>
      <input type='text' id='user' name='user_name' class='text' list='users'
        % if user:
          value='${user.display_name}'
        % elif request.identity:
          value='${request.identity['user'].display_name}'
        % else:
          value='${public_users[0].display_name}'
        % endif
      />
      <datalist id='users'>
        % for visible_user in public_users:
          <option>${visible_user.display_name}</option>
        % endfor
      </datalist>
    % endif
  </fieldset>
</%block>

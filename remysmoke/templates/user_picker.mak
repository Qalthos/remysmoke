<%block name='user_picker'>
  <div>
    % if public_users:
      <form action="${request.url}">
        <h2><span>Other users</span></h2>
        <label for='user'>User</label>
        <input type='text' id='user' name='user_name' class='text' list='users' />
        <datalist id='users'>
          % for visible_user in public_users:
            <option
            % if user and user == visible_user:
              selected=true
            % endif
            >${visible_user.display_name}</option>
          % endfor
        </datalist>
        <input type='submit' id='submit' />
      </form>
    % endif
  </div>
</%block>

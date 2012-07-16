<%inherit file="local:templates.master"/>

%for user in data:
  ${user}'s data:
  <p>
    Smokes per day: ${data[user]['smokes']}<br/>
    Average lifespan of a pack: ${data[user]['lifespan']} days<br/>
    Cost per month: $${data[user]['cost']}<br/>
    Time since last smoke: ${data[user]['now']}<br/>
    Longest time since between smokes: ${data[user]['best']}<br/>
  </p>
  <table style='width: 100%'><tr>
  <td style='width: 30%'>
    <h2>Recent 5 Excuses:</h2>
    %for excuse in data[user]['latest']:
      ${excuse}<br/>
    %endfor
  </td>
  <td style='width: 30%'>
    <h2>Random 5 Excuses:</h2>
    %for excuse in data[user]['random']:
      ${excuse}<br/>
    %endfor
  </td>
  <td style='width: 30%'>
    <h2>Top 5 Excuses:</h2>
    %for count, excuse in data[user]['top']:
      ${excuse} (${count})<br/>
    %endfor
  </td>
  </tr></table>
%endfor

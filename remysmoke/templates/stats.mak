<%inherit file="local:templates.master"/>

%for user in data:
  ${user}'s data:
  <div>
    <div style='width:50%; display:inline-block'>
      Score:<br/>
      <span style='font-size:48px'>${'%.2f' % data[user]['score']}</span>
    </div>
    <div style='width:50%; float:right'>
      Average lifespan of a pack: ${'%.2f' % data[user]['lifespan']} days<br/>
      Cost per month: $${'%.2f' % data[user]['cost']}<br/>
      Time since last smoke: ${data[user]['now']}<br/>
      Longest time since between smokes: ${data[user]['best']}<br/>
    </div>
  </div>
  <table style='width:100%'><tr>
    <th style='width:30%'>
      Recent 5 Excuses:
    </th>
    <th style='width:30%'>
      Random 5 Excuses:
    </th>
    <th style='width:30%'>
      Top 5 Excuses:
    </th>
  </tr><tr>
    <td>
      %for excuse in data[user]['latest']:
        ${excuse[0]} (${excuse[1]})<br/>
      %endfor
    </td>
    <td>
      %for excuse in data[user]['random']:
        ${excuse[0]} (${excuse[1]})<br/>
      %endfor
    </td>
    <td>
      %for count, excuses in data[user]['top']:
        ${', '.join(excuses)} (${count})<br/>
      %endfor
    </td>
  </tr></table>
%endfor

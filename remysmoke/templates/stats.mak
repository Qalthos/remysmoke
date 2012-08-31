<%inherit file="local:templates.master"/>

%for user, udata in data.items():
  ${user}'s data':
  <div>
    <div style='width:50%; float:left'>
      Score:<br/>
      <span style='font-size:48px'>${'%.2f' % udata['score']}</span>
    </div>
    <div style='width:50%; float:left'>
      Average lifespan of a pack: ${'%.2f' % udata['lifespan']} days<br/>
      Cost per month: $${'%.2f' % udata['cost']}<br/>
      Time since last smoke: ${udata['now']}<br/>
      Longest time since between smokes: ${udata['best']}<br/>
    </div>
  </div>
  <table style='width:100%'>
    <tr>
      <th style='width:30%'>
        Recent 5 Excuses:
      </th>
      <th style='width:30%'>
        Random 5 Excuses:
      </th>
      <th style='width:30%'>
        Top 5 Excuses:
      </th>
    </tr>
    %for index, excuse in enumerate(udata['latest']):
      <tr>
        <td>${excuse[0]} (${excuse[1]})</td>
        <td>${udata['random'][index][0]} (${udata['random'][index][1]})</td>
        %if len(udata['top']) > index:
          <td>${', '.join(udata['top'][index][1])} (${udata['top'][index][0]})</td>
        %endif
      </tr>
    %endfor
  </table>
%endfor

<%inherit file="local:templates.master" />

<%include file='local:templates.user_picker' />
% if not data:
  Nothing to show yet...
% else:
  ${user.display_name}'s data':
  <div>
    <div style='width:50%; float:left'>
      Score:<br/>
      <span style='font-size:48px'>${'%.2f' % data['score']}</span>
    </div>
    <div style='width:50%; float:left'>
      Average lifespan of a pack: ${'%.2f' % data['lifespan']} days<br/>
      Cost per month: $${'%.2f' % data['cost']}<br/>
      Time since last smoke: ${data['now']}<br/>
      Longest streak of not smoking: ${data['best'].days} days<br/>
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
    %for index, excuse in enumerate(data['latest']):
      <tr>
        <td>${excuse[0]} (${excuse[1]})</td>
        <td>${data['random'][index][0]} (${data['random'][index][1]})</td>
        %if len(data['top']) > index:
          <td>${', '.join(data['top'][index][1])} (${data['top'][index][0]})</td>
        %endif
      </tr>
    %endfor
  </table>
% endif

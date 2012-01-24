<%inherit file="local:templates.master"/>

%for user in data:
  ${user}'s data:
  <p>
  Smokes per day: ${data[user]['smokes']}<br/>
  Average lifespan of a pack: ${data[user]['lifespan']} days<br/>
  Cost per month: $${data[user]['cost']}
  </p>
%endfor

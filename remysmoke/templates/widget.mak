<%inherit file="local:templates.master"/>

<%def name='head()'>
	<link href="/css/graph.css" media="screen" type="text/css" rel="stylesheet">
</%def>

<div style='height:100px;'>
  <div style='float:left; width:30%;'>
    <p>Cigarettes smoked over time</p>
    <form>
    <input name='weeks' type='range' min=1 max=52 value=${weeks if weeks else 1} />
      <input type='submit' />
    </form>
  </div>
  <div style='float:left; width:30%;'>
    <p>Other</p>
    <a href="${tg.url('/graph?graph=punch')}" class="${('', 'active')}">Smoking Punchcard</a></li>
  </div>
  <div style='float:left; width:40%'>
    <%include file='local:templates.user_picker'/>
  </div>
</div>

<div style='height:230px'>
  ${widget | n}
</div>
